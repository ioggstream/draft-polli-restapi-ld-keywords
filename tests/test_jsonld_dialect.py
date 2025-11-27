import json
from pathlib import Path

import jsonschema
import pytest

DATADIR = Path(__file__).parent.parent
VOCAB_DIR = DATADIR / "vocab"
DIALECT_JSON = VOCAB_DIR / "jsonld-dialect.json"
META_JSON = VOCAB_DIR / "jsonld-meta.json"
META_URI = "https://ioggstream.github.io/draft-polli-restapi-ld-keywords/vocab/jsonld-meta.json"
DIALECT_URI = "https://ioggstream.github.io/draft-polli-restapi-ld-keywords/vocab/jsonld-dialect.json"

STORE = {
    META_URI: json.loads(META_JSON.read_text()),
    DIALECT_URI: json.loads(DIALECT_JSON.read_text()),
}


@pytest.fixture(params=[True, False], ids=["with_resolver", "without_resolver"])
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
