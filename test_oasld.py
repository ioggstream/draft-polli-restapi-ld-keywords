import json
import logging
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from oasld import Instance, RefResolver


@pytest.fixture
def resolver(schema_yaml):
    return RefResolver(schema_yaml)


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def schema_yaml():
    return schemas()


def schemas():
    return yaml.safe_load(Path("schemas.yaml").read_text())


@pytest.mark.parametrize(
    "testcase,expected",
    [
        (
            dict(
                instance={},
                schema={"x-jsonld-context": "http://foo.example", "type": "object"},
                context=Instance.NO_CONTEXT,
            ),
            Instance.NO_CONTEXT,
        ),
        (
            dict(
                instance={},
                schema={"x-jsonld-context": "http://foo.example", "type": "object"},
            ),
            "http://foo.example",
        ),
        (
            dict(
                instance={},
                schema={"x-jsonld-context": "http://foo.example", "type": "object"},
                context={"foo": "bar"},
            ),
            "http://foo.example",
        ),
        (
            dict(
                instance={"givenName": "Mario"},
                schema={"x-jsonld-context": "http://foo.example", "type": "object"},
                context={"@container": "@set"},
                parent=Instance({}, {}),
            ),
            {
                "@container": "@set",
                "@context": "http://foo.example",
            },
        ),
        (
            dict(
                instance={"foo": 1, "biz": 2},
                schema={"x-jsonld-context": {"biz": "pop"}, "type": "object"},
                context={"@container": "@set"},
                parent=Instance({}, {}),
            ),
            {"@container": "@set", "@context": {"biz": "pop"}},
        ),
    ],
)
def test_init(testcase, expected):
    context = testcase.pop("context", None)
    i = Instance(
        **testcase,
        context=deepcopy(context) if context is not Instance.NO_CONTEXT else context,
    )
    res = (
        i.subentry_context_ref
        if i.is_subentry or i.is_decontext()
        else i.subentry_context_ref.get("@context")
    )
    assert res == expected


@pytest.mark.parametrize(
    "schema_name",
    [x for x in schemas()],
)
def test_edu(resolver, schema_yaml, schema_name):
    from pyld import jsonld

    schema = schema_yaml[schema_name]
    instance = harn_schema(schema, resolver)
    with open(f"tmp.{schema_name}.json", "w") as fp:
        json.dump(instance.ld, fp=fp, indent=2)
    with open(f"tmp.{schema_name}.expanded.json", "w") as fp:
        json.dump(jsonld.expand(instance.ld), fp=fp, indent=2)


def harn_schema(schema, resolver):
    example = schema["example"]
    instance = Instance(example, schema)
    instance.safe_mode = False
    instance.process_instance(resolver=resolver)
    log.info("\n" + json.dumps(instance.ld))
    return instance
