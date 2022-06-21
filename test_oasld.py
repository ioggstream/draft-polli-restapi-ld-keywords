import json
import logging
from copy import deepcopy
from pathlib import Path
from typing import Dict

import jsonschema
import yaml

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

schema = yaml.safe_load(Path("schemas.yaml").read_text())

person = schema["Person"]
EXAMPLE = schema["Person"]["example"]


class RefResolver:
    def __init__(self, schema: Dict) -> None:
        self.resolver = jsonschema.RefResolver("/", "")
        self.schema = schema

    def resolve(self, ref):
        return self.resolver.resolve_fragment(self.schema, ref)


class Instance:
    def __init__(self, instance, schema, context=None, is_subentry=False) -> None:
        self.json_instance = instance
        self.schema = schema
        self.ld = deepcopy(instance) if not is_subentry else instance
        self.is_subentry = False
        self.subentry_context_ref = context
        self.jcontext = schema.get("x-jsonld-context", {})
        if jtype := schema.get("x-jsonld-type"):
            self.ld["@type"] = jtype
        if self.jcontext:
            if not self.is_subentry:
                self.ld["@context"] = deepcopy(self.jcontext)
            elif self.subentry_context_ref:
                if "@context" in self.subentry_context_ref:
                    raise ValueError(
                        "Cannot overwrite a @context defined in the super-schema"
                    )
                self.subentry_context_ref["@context"] = deepcopy(self.jcontext)
            elif self.subentry_context_ref is None:
                # Explicitly skipping context merge.
                pass
            else:
                raise NotImplementedError("An sub-entry MUST have a context")

    def process_instance(self, resolver: RefResolver):
        properties = self.schema["properties"]
        for k, v in self.ld.items():
            process_keywords = {"@context", "@type"} - set(self.jcontext.get(k, {}))
            log.info(f"Looking for {process_keywords}")
            property_schema = properties.get(k, {})
            if all(
                (property_schema.get("type") in ("object", "array"), process_keywords)
            ):
                log.info(k, v)
                if property_schema["type"] == "array":
                    subschema = resolver.resolve(
                        property_schema["items"]["$ref"].strip("#")
                    )
                    subcontext = self.ld["@context"][k]
                    for subinstance in v:
                        i = Instance(
                            subinstance, subschema, context=subcontext, is_subentry=True
                        )
                        i.process_instance(resolver)
                        # Only merge context for the first processing entry.
                        # This can be somewhat limitative because the traversing process
                        # depends on the subinstance properties and not on the ones
                        # of the schema.
                        subcontext = None
                elif property_schema["type"] == "object":
                    process_object()
                else:
                    raise NotImplementedError


def process_instance(instance, schema, schemas=None, is_subentry=False, context=None):
    schemas = schemas or {}

    schema_resolver = jsonschema.RefResolver("/", "")
    if jtype := schema.get("x-jsonld-type"):
        instance["@type"] = jtype
    if jcontext := schema.get("x-jsonld-context"):
        if not is_subentry:
            instance["@context"] = deepcopy(jcontext)
        elif context:
            if "@context" in context:
                raise ValueError(
                    "Cannot overwrite a @context defined in the super-schema"
                )
            context["@context"] = deepcopy(jcontext)
        elif context is None:
            pass
        else:
            raise NotImplementedError("An sub-entry MUST have a context")

    properties = schema["properties"]
    for k, v in instance.items():
        process_keywords = {"@context", "@type"} - set(jcontext.get(k, {}))
        log.info(f"Looking for {process_keywords}")
        property_schema = properties.get(k, {})
        if all((property_schema.get("type") in ("object", "array"), process_keywords)):
            log.info(k, v)
            if property_schema["type"] == "array":
                subschema = schema_resolver.resolve_fragment(
                    schemas, property_schema["items"]["$ref"].strip("#")
                )
                subcontext = instance["@context"][k]
                for subinstance in v:
                    process_instance(
                        subinstance,
                        subschema,
                        schemas,
                        is_subentry=True,
                        context=subcontext,
                    )
                    # Only merge context for the first processing entry.
                    # This can be somewhat limitative because the traversing process
                    # depends on the subinstance properties and not on the ones
                    # of the schema.
                    subcontext = None
            elif property_schema["type"] == "object":
                process_object()
            else:
                raise NotImplementedError

    return instance


def test_process_array():
    context = {
        "@vocab": "https://w3.org/ns/person#",
        "children": {"@container": "@set"},
        "email": "@id",
    }
    actual = process_instance(
        instance={"email": "a@b.c"},
        schema={
            "properties": {
                "children": {"items": {"$ref": "#/Person"}, "type": "array"},
                "email": {"type": "string"},
            },
            "x-jsonld-context": {
                "@vocab": "https://w3.org/ns/person#",
                "children": {"@container": "@set"},
                "email": "@id",
            },
            "x-jsonld-type": "Person",
        },
        schemas={},
        is_subentry=True,
        context=context["children"],
    )
    assert context["children"]["@context"]["@vocab"]


def test_instance():
    resolver = RefResolver(schema)
    instance = Instance(EXAMPLE, person)
    instance.process_instance(resolver=resolver)
    print(json.dumps(instance.ld))


def test_example():
    example = dict(**EXAMPLE)
    actual = process_instance(example, person, schema)
    print(json.dumps(actual))
    raise NotImplementedError
