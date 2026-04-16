import json
from pathlib import Path
import os

import jsonschema
import pytest
import yaml

DATADIR = Path(__file__).parent.parent
VOCAB_DIR = DATADIR / "vocab"
DIALECT_JSON = VOCAB_DIR / "jsonld-dialect.json"
META_JSON = VOCAB_DIR / "jsonld-meta.json"

# Source files are in YAML.
TABLE_SCHEMA_JSONLD_YAML = VOCAB_DIR / "table-schema-jsonld.yaml"
SEMANTIC_DATA_PACKAGE_YAML = VOCAB_DIR / "semantic-data-package.yaml"

REPO = "https://ioggstream.github.io/draft-polli-restapi-ld-keywords/"
if ref_name := os.getenv("GITHUB_REF_NAME"):
    if ref_name != "main":
        REPO = f"{REPO}/{ref_name}/"

# URIs are in .json, converted at build time.
META_URI = f"{REPO}/vocab/jsonld-meta.json"
DIALECT_URI = f"{REPO}/vocab/jsonld-dialect.json"
TABLE_SCHEMA_JSONLD_URI = f"{REPO}/vocab/table-schema-jsonld.json"
SEMANTIC_DATA_PACKAGE_URI = f"{REPO}/vocab/semantic-data-package.json"

STORE = {
    META_URI: json.loads(META_JSON.read_text()),
    DIALECT_URI: json.loads(DIALECT_JSON.read_text()),
    TABLE_SCHEMA_JSONLD_URI: yaml.safe_load(TABLE_SCHEMA_JSONLD_YAML.read_text()),
    SEMANTIC_DATA_PACKAGE_URI: yaml.safe_load(SEMANTIC_DATA_PACKAGE_YAML.read_text()),
}


@pytest.fixture(
    params=[True, False],
    ids=["with_resolver", "without_resolver"],  # Uncomment when PR is published
)
def validator(request):
    """Return a Validator instance.

    Parametrized to return two variants:
    - with_resolver=True: a validator with a RefResolver that maps the remote
      meta-schema URI to the local `vocab/jsonld-meta.json` (store).
    - with_resolver=False: a validator without the resolver (default instantiation).
    """
    Validator = jsonschema.validators.validator_for(STORE[DIALECT_URI])
    if request.param:
        resolver = jsonschema.RefResolver.from_schema(STORE[DIALECT_URI], store=STORE)
        return Validator(STORE[DIALECT_URI], resolver=resolver)
    return Validator(STORE[DIALECT_URI])


def _sample_schema(x_jsonld_type):
    return {
        "$schema": DIALECT_URI,
        "$vocabulary": {DIALECT_URI: True},
        "type": "object",
        "x-jsonld-type": x_jsonld_type,
        "x-jsonld-context": {"@vocab": "https://example.org/vocab#"},
    }


def test_schema_valid_against_jsonld_dialect(validator):
    """Validate a simple schema that uses the JSON-LD keywords."""
    validator.validate(_sample_schema("Person"))


def test_x_jsonld_type_boolean_invalid(validator):
    """A boolean `x-jsonld-type` must be rejected by the dialect."""
    with pytest.raises(jsonschema.exceptions.ValidationError):
        validator.validate(_sample_schema(True))


# Create a validator with resolver for remote schema references
Validator = jsonschema.Draft202012Validator


def test_frictionless_tableschema_examples():
    """
    When:
      - loading the table-schema-jsonld.yaml
    Then:
        - all examples validate against the schema
    """
    # Load the table schema with JSON-LD extensions
    table_schema_jsonld = yaml.safe_load(TABLE_SCHEMA_JSONLD_YAML.read_text())

    # Create a validator with resolver for the table-schema-jsonld
    resolver = jsonschema.RefResolver.from_schema(table_schema_jsonld, store=STORE)
    validator = Validator(table_schema_jsonld, resolver=resolver)

    # Validate each example's schema
    for example in table_schema_jsonld.get("examples", []):
        # Validate the schema against table-schema-jsonld
        validator.validate(example)


@pytest.mark.parametrize(
    "invalid_example",
    [
        {
            "x-jsonld-type": 123,
            "fields": [
                {
                    "name": "id",
                    "type": "integer",
                }
            ],
        },
        {
            "x-jsonld-type": ["Person", 456],
            "fields": [
                {
                    "name": "name",
                    "type": "string",
                }
            ],
        },
        {  # x-jsonld-context is a number
            "x-jsonld-context": 123,
            "fields": [
                {
                    "name": "age",
                    "type": "integer",
                }
            ],
        },
        {  # x-jsonld-context is a boolean
            "x-jsonld-context": False,
            "fields": [
                {
                    "name": "age",
                    "type": "integer",
                }
            ],
        },
    ],
)
def test_frictionless_tableschema_invalid_example(invalid_example):
    """
    When:
      - loading an invalid example for table-schema-jsonld.yaml
    Then:
        - validation fails
    """
    # Load the table schema with JSON-LD extensions
    table_schema_jsonld = yaml.safe_load(TABLE_SCHEMA_JSONLD_YAML.read_text())

    # Create a validator with resolver for the table-schema-jsonld
    resolver = jsonschema.RefResolver.from_schema(table_schema_jsonld, store=STORE)
    validator = Validator(table_schema_jsonld, resolver=resolver)

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validator.validate(invalid_example)


def test_frictionless_datapackage_examples():
    """
    When:
      - loading the semantic-data-package.yaml
    Then:
        - all examples validate against the schema
    """
    # Load the semantic data package schema
    semantic_data_package = yaml.safe_load(SEMANTIC_DATA_PACKAGE_YAML.read_text())

    resolver = jsonschema.RefResolver.from_schema(semantic_data_package, store=STORE)
    validator = Validator(semantic_data_package, resolver=resolver)

    # Validate each example against the schema
    examples = semantic_data_package.get("examples", [])
    assert len(examples) > 0, "No examples found in semantic-data-package.yaml"

    for idx, example in enumerate(examples):
        try:
            validator.validate(example)
        except jsonschema.exceptions.ValidationError as e:
            pytest.fail(f"Example {idx} failed validation: {e.message}")
