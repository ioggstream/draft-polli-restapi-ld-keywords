import json
from pathlib import Path

import jsonschema
import pytest

DATADIR = Path(__file__).parent.parent
VOCAB_DIR = DATADIR / "vocab"
DIALECT_JSON = VOCAB_DIR / "jsonld-dialect.json"
META_JSON = VOCAB_DIR / "jsonld-meta.json"
META_URI = (
    "https://ioggstream.github.io/draft-polli-restapi-ld-keywords/jsonld-meta.json"
)
DIALECT_URI = (
    "https://ioggstream.github.io/draft-polli-restapi-ld-keywords/jsonld-dialect.json"
)

STORE = {
    META_URI: json.loads(META_JSON.read_text()),
    DIALECT_URI: json.loads(DIALECT_JSON.read_text()),
}


@pytest.fixture
def validator():
    """Load the dialect and return a Validator instance that resolves the
    remote meta schema URI to the local `vocab/jsonld-meta.json` when present.
    """
    Validator = jsonschema.validators.validator_for(STORE[DIALECT_URI])
    resolver = jsonschema.RefResolver.from_schema(STORE[DIALECT_URI], store=STORE)
    return Validator(STORE[DIALECT_URI], resolver=resolver)


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
