import json
import logging
from copy import deepcopy
from pathlib import Path
from typing import Dict

import jsonschema
import yaml

CTX = "@context"


class RefResolver:
    def __init__(self, schema: Dict) -> None:
        self.resolver = jsonschema.RefResolver("/", "")
        self.schema = schema

    def resolve(self, ref):
        return self.resolver.resolve_fragment(self.schema, ref)


class Instance:
    NO_CONTEXT = object()

    def __init__(self, instance, schema, context=None, is_subentry=False) -> None:
        self.json_instance = instance
        self.schema = schema
        self.ld = deepcopy(instance) if not is_subentry else instance
        self.is_subentry = is_subentry
        if jtype := schema.get("x-jsonld-type"):
            self.ld["@type"] = jtype

        self.jcontext = schema.get("x-jsonld-context", {})

        if context is Instance.NO_CONTEXT:
            # Explicitly skipping context merge.
            self.subentry_context_ref = Instance.NO_CONTEXT
            return
        self.subentry_context_ref = context
        if self.jcontext:
            if not self.is_subentry:
                # Initialize.
                self.subentry_context_ref = {CTX: deepcopy(self.jcontext)}
            elif CTX in context:
                raise ValueError(
                    "Cannot overwrite a @context defined in the super-schema"
                )
            elif isinstance(context, dict):
                # Merge in the passed context
                self.subentry_context_ref[CTX] = deepcopy(self.jcontext)
            else:
                raise NotImplementedError("An sub-entry MUST have a context")

    def is_decontext(self):
        return self.subentry_context_ref == Instance.NO_CONTEXT

    def process_instance(self, resolver: RefResolver):
        properties = self.schema["properties"]
        for k, v in self.ld.items():
            process_keywords = {"@context", "@type"} - set(self.jcontext.get(k) or {})
            property_schema = properties.get(k, {})
            log.warn(f"Looking for {process_keywords} on {k} => {property_schema}")
            if schema_ref := property_schema.get("$ref"):
                property_schema = resolver.resolve(schema_ref.strip("#"))
            if all(
                (property_schema.get("type") in ("object", "array"), process_keywords)
            ):
                log.info(k, v)
                if property_schema["type"] == "array":
                    subschema = resolver.resolve(
                        property_schema["items"]["$ref"].strip("#")
                    )
                    subcontext = (
                        Instance.NO_CONTEXT
                        if self.is_decontext()
                        else self.subentry_context_ref[CTX][k]
                    )
                    for idx, subinstance in enumerate(v):
                        log.debug(f"Integrating context id {id(subcontext)}")
                        i = Instance(
                            subinstance, subschema, context=subcontext, is_subentry=True
                        )
                        i.process_instance(resolver)
                        # Only merge context for the first processing entry.
                        # This can be somewhat limitative because the traversing process
                        # depends on the subinstance properties and not on the ones
                        # of the schema.
                        subcontext = Instance.NO_CONTEXT
                elif property_schema["type"] == "object":
                    subschema = property_schema
                    subcontext = self.subentry_context_ref[CTX].setdefault(k, {})
                    # if k == "spouse": import pdb; pdb.set_trace()
                    i = Instance(v, subschema, context=subcontext, is_subentry=True)
                    i.process_instance(resolver)
                else:
                    raise NotImplementedError
        if not self.is_subentry:
            self.ld[CTX] = self.subentry_context_ref[CTX]


import pytest


@pytest.fixture
def resolver(schema_yaml):
    return RefResolver(schema_yaml)


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def schema_yaml():
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
            {},
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
                is_subentry=True,
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
                is_subentry=True,
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
        if i.is_subentry
        else i.subentry_context_ref.get("@context")
    )
    assert res == expected


def test_person(resolver, schema_yaml):
    schema = schema_yaml["Person"]
    instance = harn_schema(schema, resolver)
    json.dump(instance.ld, fp=open("tmp.person.json", "w"), indent=2)


def test_granny(resolver, schema_yaml):
    schema = schema_yaml["Granny"]
    instance = harn_schema(schema, resolver)
    json.dump(instance.ld, fp=open("tmp.granny.json", "w"), indent=2)


def test_spouse(resolver, schema_yaml):
    schema = schema_yaml["Spouse"]
    instance = harn_schema(schema, resolver)
    json.dump(instance.ld, fp=open("tmp.spouse.json", "w"), indent=2)


@pytest.mark.parametrize("schema_name", ["EducationLevel", "BirthPlace", "Citizen"])
def test_edu(resolver, schema_yaml, schema_name):
    schema = schema_yaml[schema_name]
    instance = harn_schema(schema, resolver)
    json.dump(instance.ld, fp=open(f"tmp.{schema_name}.json", "w"), indent=2)


def harn_schema(schema, resolver):
    example = schema["example"]
    instance = Instance(example, schema)
    instance.process_instance(resolver=resolver)
    log.info("\n" + json.dumps(instance.ld))
    return instance
