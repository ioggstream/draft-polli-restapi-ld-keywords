import logging
from copy import deepcopy
from typing import Dict

import jsonschema
from typing_extensions import Self

CTX = "@context"

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RefResolver:
    def __init__(self, schema: Dict) -> None:
        self.resolver = jsonschema.RefResolver("/", "")
        self.schema = schema

    def resolve(self, ref):
        return self.resolver.resolve_fragment(self.schema, ref)


class Instance:
    NO_CONTEXT = object()

    def __init__(
        self,
        instance: Dict,
        schema: Dict,
        context: Dict = None,
        parent: Self = None,
    ) -> None:
        self.json_instance = instance
        self.schema = schema
        self.ld = deepcopy(instance) if parent is None else instance
        self.parent = parent
        self.safe_mode = self.parent.safe_mode if self.parent else True
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
            elif CTX in context or ():
                if self.safe_mode:
                    raise ValueError(
                        "Cannot overwrite a @context defined in the super-schema"
                    )
                else:
                    log.warning(
                        "Skipping nested context because it is already defined."
                    )
            elif isinstance(context, dict):
                # Merge in the passed context
                self.subentry_context_ref[CTX] = deepcopy(self.jcontext)
            else:
                raise NotImplementedError("An sub-entry MUST have a context")

    def is_decontext(self):
        return self.subentry_context_ref == Instance.NO_CONTEXT

    @property
    def is_subentry(self):
        return self.parent is not None

    def process_instance(self, resolver: RefResolver):
        properties = self.schema["properties"]
        for k, v in self.ld.items():
            process_keywords = {"@context", "@type"} - set(self.jcontext.get(k) or {})
            property_schema = properties.get(k, {})
            log.debug(f"Looking for {process_keywords} on {k} => {property_schema}")
            if schema_ref := property_schema.get("$ref"):
                property_schema = resolver.resolve(schema_ref.strip("#"))
            if all(
                (property_schema.get("type") in ("object", "array"), process_keywords)
            ):
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
                            subinstance, subschema, context=subcontext, parent=self
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
                    i = Instance(v, subschema, context=subcontext, parent=self)
                    i.process_instance(resolver)
                else:
                    raise NotImplementedError
        if not self.is_subentry:
            self.ld[CTX] = self.subentry_context_ref[CTX]


def process_schema(schema_name, schemas):
    schema = schemas[schema_name]
    example = schema["example"]
    instance = Instance(example, schema)
    instance.safe_mode = False

    resolver = RefResolver(schemas)
    instance.process_instance(resolver=resolver)
    return instance


sample_schema = schema_json = {
    "Person": {
        "description": "Simple cyclic example.",
        "x-jsonld-type": "Person",
        "x-jsonld-context": {
            "email": "@id",
            "@vocab": "https://w3.org/ns/person#",
            "children": {"@container": "@set"},
        },
        "type": "object",
        "properties": {
            "email": {"type": "string"},
            "birthplace": {"$ref": "#/BirthPlace"},
            "children": {"type": "array", "items": {"$ref": "#/Person"}},
        },
        "example": {
            "email": "mailto:a@example",
            "givenName": "Alice",
            "familyName": "Smith",
            "birthplace": {
                "city": "Roma",
                "province": "RM",
                "country": "ITA",
                "interno": "Interno 8",
            },
            "children": [
                {"email": "mailto:dough@example"},
                {"email": "mailto:son@example"},
            ],
        },
    },
    "BirthPlace": {
        "type": "object",
        "additionalProperties": False,
        "required": ["city", "province", "country"],
        "x-jsonld-type": "https://w3id.org/italia/onto/CLV/Feature",
        "x-jsonld-context": {
            "@vocab": "https://w3id.org/italia/onto/CLV/",
            "city": "hasCity",
            "country": {
                "@id": "hasCountry",
                "@type": "@id",
                "@context": {
                    "@base": "http://publications.europa.eu/resource/authority/country/"
                },
            },
            "province": {
                "@id": "hasProvince",
                "@type": "@id",
                "@context": {
                    "@base": "https://w3id.org/italia/data/identifiers/provinces-identifiers/vehicle-code/"
                },
            },
            "interno": None,
        },
        "properties": {
            "city": {
                "type": "string",
                "description": "The city where the person was born.",
                "example": "Roma",
            },
            "province": {
                "type": "string",
                "description": "The province where the person was born.",
                "example": "RM",
            },
            "country": {
                "type": "string",
                "description": "The iso alpha-3 code of the country where the person was born.",
                "example": "ITA",
            },
            "interno": {"type": "string", "maxLength": 32},
        },
        "example": {
            "city": "Roma",
            "province": "RM",
            "country": "ITA",
            "interno": "Interno 8",
        },
    },
}
