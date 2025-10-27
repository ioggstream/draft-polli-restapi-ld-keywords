---
title: REST API Linked Data Keywords
abbrev:
docname: draft-polli-restapi-ld-keywords-latest
category: info

ipr: trust200902
area: General
workgroup:
keyword: Internet-Draft

stand_alone: yes
pi: [toc, tocindent, sortrefs, symrefs, strict, compact, comments, inline, docmapping]

venue:
  home: https://github.com/ioggstream/draft-polli-restapi-ld-keywords
  repo: https://github.com/ioggstream/draft-polli-restapi-ld-keywords/issues
# mail: robipolli@gmail.com

# github-issue-label: editorial

author:
 -
    ins: R. Polli
    name: Roberto Polli
    org: Digital Transformation Department, Italian Government
    email: robipolli@gmail.com
    country: Italy

normative:
  YAML:
    title: YAML Ain't Markup Language Version 1.2
    date: 2021-10-01
    author:
    - ins: Oren Ben-Kiki
    - ins: Clark Evans
    - ins: Ingy dot Net
    - ins: Tina Müller
    - ins: Pantelis Antoniou
    - ins: Eemeli Aro
    - ins: Thomas Smith
    target: https://yaml.org/spec/1.2.2/
  OAS:
    title: OpenAPI Specification 3.0.0
    date: 2017-07-26
    author:
    - ins: Darrel Miller
    - ins: Jeremy Whitlock
    - ins: Marsh Gardiner
    - ins: Mike Ralphson
    - ins: Ron Ratovsky
    - ins: Uri Sarid
  JSON-LD-11:
    title: JSON-LD 1.1
    target: https://www.w3.org/TR/json-ld11/
    authors:
    - ins: Gregg Kellogg
    - ins: Pierre-Antoine Champin
    - ins: Dave Longley
  JSONSCHEMA:
    title: JSON Schema
    target: https://json-schema.org/specification.html
  JSON: RFC8259
  HTTP: RFC9110
  URI: RFC3986
  RDF:
    title: RDF Concepts and Abstract Syntax
    target: https://www.w3.org/TR/rdf11-concepts/
  RDFS:
    title: RDF Schema 1.1
    target: https://www.w3.org/TR/rdf-schema/
  YAML-IANA:
    title: The application/yaml Media Type
    target: https://www.iana.org/assignments/media-types/application/yaml

informative:
  I-D.ietf-jsonpath-base:
  JSON-POINTER: RFC6901
  JSONLD-11-API:
    target: https://www.w3.org/TR/json-ld11-api/
    title: JSON-LD 1.1 Processing Algorithms and API
  JSON-SCHEMA-RDF:
    target: https://www.w3.org/2019/wot/json-schema/
    title: JSON Schema in RDF
  SHACL:
    title: Shapes Constraint Language (SHACL)
    target: https://www.w3.org/TR/shacl/
    date: 2017-07-20
  OWL:
    title: OWL 2 Web Ontology Language Document Overview
    target: https://www.w3.org/TR/owl2-overview/
  XS:
    title: XML Schema
    target: https://www.w3.org/2001/XMLSchema
--- abstract

This document defines two
keywords to provide semantic information in
OpenAPI Specification and JSON Schema documents,
and support contract-first semantic schema design.

--- middle

# Introduction

API providers usually specify semantic information in text or out-of-band documents;
at best, this information is described in prose into specific sections of interface definition documents (see {{prosaic-semantics}}).

This is because API providers do not always value machine-readable semantics,
or because they have no knowledge of semantic technologies -
that are perceived as unnecessarily complex.

A full-semantic approach (e.g. writing RDF oriented APIs) has not become widespread
because
transferring and processing the semantics on every message
significantly increases data transfer and computation requirements.

Moreover the semantic landscape do not provide easy ways of defining / constraining
the syntax of an object:
tools like [SHACL] and [OWL] restrictions are considered
computationally intensive to process and complex to use
from web and mobile developers.

This document provides a simple mechanism
to attach semantic information to REST APIs
that rely on different dialects of [JSONSCHEMA],
thus supporting a contract-first schema design.

For example, the OpenAPI Specifications (see [OAS])
allow to describe REST APIs
interactions and capabilities using a machine-readable format
based on [JSON] or [YAML].
OAS 3.0 is based on JSON Schema draft-4
while OAS 3.1 relies on the latest JSON Schema draft.

## Goals and Design Choices

This document has the following goals:

- describe in a single specification document backed by [JSONSCHEMA]
  (e.g. an OpenAPI document)
  both the syntax and semantics of JSON objects.
  This information can be either be provided
  editing the document by hand or via automated tools;
- easy for non-semantic experts and with reduced complexity;
- support for OAS 3.0 / JSON Schema Draft4;

while it is not intended to:

- integrate the syntax defined using [JSONSCHEMA];
- infer semantic information where it is not provided;
- convert [JSONSCHEMA] documents to RDF Schema (see [RDFS]) or XML Schema.

Thus, the following design choices have been made:

- the semantic context of a JSON object will be described
  using [JSON-LD-11] and its keywords;
- property names are limited to characters that can be used in variable
  names (e.g. excluding `:` and `.`)
  to avoid interoperability issues with code-generation tools;
- privilege a deterministic behavior over automation and composability;
- interoperable with the mechanisms described in Section 6.1 of [JSON-LD-11]
  for conveying semantic context in REST APIs.

## Prosaic semantics {#prosaic-semantics}

[JSONSCHEMA] allows to define the structure of the exchanged data using specific keywords.
Properties' semantics can be expressed in prose via the `description` keyword.

~~~ yaml
Person:
  description: A Person.
  type: object
  properties:
    givenName:
      description: The given name of a Person.
      type: string
    familyName:
      description: The family name, or surname, of a Person.
      type: string
  example:
    givenName: John
    familyName: Doe
~~~
{: title="Example of JSON Schema model that provides semantic prose." #ex-semantic-prose}

[JSON-LD-11] defines a way to interpret a JSON object as JSON-LD:
the example schema instance (a JSON document conformant to a given schema)
provided in the above "Person" schema can be integrated with
semantic information adding the `@type` and `@context` properties.

~~~ json

{
  "@context": {
    "@vocab": "https://w3.org/ns/person#"
  },
  "@type": "Person",
  "givenName": "John",
  "familyName": "Doe"
}
~~~
{: title="Example of a schema instance transformed in a JSON-LD object." #ex-json-ld}

This document shows how
to integrate into a JSON Schema document
information that can be used
to add the `@context` and `@type`
properties to the associated JSON Schema instances.

## Notational Conventions

{::boilerplate bcp14+}

The terms  "content", "content negotiation", "resource",
and "user agent"
in this document are to be interpreted as in [HTTP].

The terms "fragment" and "fragment identifier"
in this document are to be interpreted as in [URI].

The terms "node", "alias node", "anchor" and "named anchor"
in this document are to be intepreded as in [YAML].

The terms "schema" and "schema instance"
in this document are to be intepreded as in [JSONSCHEMA]
draft-4 and higher.

The terms "JSON object", "JSON document", "member", "member name"
in this document are to be intepreded as in [JSON].
The term "property" - when referred to a JSON document
such as a schema instance -
is a synonym of "member name",
and the term "property value" is a synonym of "member value".

The terms "@context", "@type", "@id", "@value" and "@language" are to be interpreted as JSON-LD keywords in [JSON-LD-11],
whereas the term "context" is to be interpreted as a JSON-LD Context
defined in the same document.

Since JSON-LD is a serialization format for RDF,
the document can use JSON-LD and RDF interchangeably
when it refers to the semantic interpretation of a resource.

The JSON Schema keywords defined in {{keywords}}
are collectively named "semantic keywords".

# JSON Schema keywords {#keywords}

A schema (see [JSONSCHEMA]) MAY
use the following JSON Schema keywords,
collectively named "semantic keywords"
to provide semantic information
for all related schema instances.

x-jsonld-type:
: This keyword conveys an RDF type (see [RDF])
   for the JSON schema instances described by the associate
   schema. It is defined in {{keywords-type}}.

x-jsonld-context:
: This keyword conveys a JSON-LD context
   for the JSON schema instances described by the associate
   schema. It is defined in {{keywords-context}}.

This specification MAY be used to:

- populate the `@type` property along the schema instance objects;
- compose an "instance context" to populate the `@context`
  property at the root of the schema instance.

The schema MUST be of type "object".
This is because [JSON-LD-11] does not define a way
to provide semantic information on JSON values that
are not JSON objects.

The schema MUST NOT describe a JSON-LD
(e.g. of `application/ld+json` media type)
or conflicts will arise, such as
which is the correct `@context` or `@type`
(see {{sec-conflicts}}).

Both JSON Schema keywords defined in this document
might contain URI references.
Those references MUST NOT be dereferenced automatically,
since there is no guarantee that they point to actual
locations.
Moreover they could reference unsecured resources
(e.g. using the "http://" URI scheme [HTTP]).

{{ex}} provides various examples of integrating
semantic information in schema instances.

## The x-jsonld-type JSON Schema keyword {#keywords-type}

The x-jsonld-type value
provides information on the RDF type of the associate
schema instances.

This value MUST be valid according to the JSON-LD `@type` keyword
as described in [Section 3.5 of JSON-LD-11](https://www.w3.org/TR/json-ld11/#specifying-the-type);
it is thus related to the information provided via the x-jsonld-context keyword (see {{keywords-context}}).

It SHOULD NOT reference an [RDF Datatype](https://www.w3.org/TR/rdf11-concepts/#section-Datatypes)
because it is not intended to provide
syntax information, but only semantic information.

## The x-jsonld-context JSON Schema keyword {#keywords-context}

The x-jsonld-context value
provides the information required to interpret the associated
schema instances as JSON-LD
according to the specification in [Section 6.1 of JSON-LD-11](https://www.w3.org/TR/json-ld11/#interpreting-json-as-json-ld).

Its value MUST be a valid JSON-LD Context
(see
[Section 9.15 of JSON-LD-11](https://www.w3.org/TR/json-ld11/#context-definitions)
).

When context composition (see {{int-composability}}) is needed,
the context SHOULD be provided in the form of a JSON object;
in fact, if the x-jsonld-context is a URL string,
that URL needs to be dereferenced and processed
to generate the instance context.

~~~ yaml
Place:
  type: object
  x-jsonld-context:
    "@vocab": "https://my.context/location.jsonld"
  properties:
    country: {type: string}

Person:
  x-jsonld-context: https://my.context/person.jsonld
  type: object
  properties:
    birthplace:
      $ref: "#/Place"
~~~
{: title="Composing URL contexts requires dereferencing them." #ex-url-contexts}

## Interpreting schema instances {#interpreting}

This section describes an OPTIONAL workflow
to interpret a schema instance as JSON-LD.

1. ensure that the initial schema instance does not contain
   any `@context` or `@type` property.
   For further information see {{sec-conflicts}};
1. add the `@context` property with the value of x-jsonld-context.
   This will be the initial "instance context": the only one that will be mangled;
1. add the `@type` property with the value of x-jsonld-type;
1. iterate on each instance property like the following:

   - identify the sub-schema associated to the property
     (e.g. resolving $refs)
     and check the presence of semantic keywords;
   - for the x-jsonld-type, add the `@type` property to the sub-instance;
   - for the x-jsonld-context, integrate its information in the instance context
     when they are not already present;
   - iterate this process in case of nested entries.

The specific algorithm
for integrating the values of x-jsonld-context
present in sub-schemas
into the instance context (see {{keywords}})
is an implementation detail.

# Interoperability Considerations {#int}

See the interoperability considerations for the media types
and specifications used, including [YAML-IANA], [JSON], [OAS],
[JSONSCHEMA] and [JSON-LD-11].

Annotating a schema with semantic keywords
containing JSON-LD keywords
(e.g. `@context`, `@type` and `@language`)
may hinder its ability to be interpreted as a JSON-LD document
(e.g. using the [JSON-LD 1.1 context for the JSON Schema vocabulary](https://www.w3.org/2019/wot/json-schema#json-ld11-ctx));
this can be mitigated extending that context and specifying
that Linked Data keywords are JSON Literals.

~~~ json
{ "@context": {
    "x-jsonld-context: { "@type": "@json"},
    "x-jsonld-type: { "@type": "@json"}
  }
}
~~~

This is generally not a problem, since a generic
[JSONSCHEMA] document cannot be reliably interpreted
as JSON-LD using a single context: this is because the same
JSON member keys can have different meanings depending
on their JSON Schema position (see [the notes in the  Interpreting JSON Schema as JSON-LD 1.1](https://www.w3.org/2019/wot/json-schema#interpreting-json-schema-as-json-ld-1-1) section of [JSON-SCHEMA-RDF]).

## Syntax is out of scope {#int-syntax-oos}

This specification is not designed to restrict
the syntax of a JSON value nor to support a conversion
between JSON Schema and XMLSchema
(see {{keywords-type}}).

## Limited expressivity {#int-expressivity}

Not all RDF resources can be expressed as JSON documents
annotated with `@context` and `@type`:
this specification is limited by the possibilities
of [Section 6.1 of JSON-LD-11](https://www.w3.org/TR/json-ld11/#interpreting-json-as-json-ld).
On the other hand, since this approach
delegates almost all the processing to of JSON-LD,
as long as JSON-LD evolves
it will cover further use cases.

## Disjoint with JSON-LD {#int-no-jsonld}

This specification is not designed to pre-process
or mangle JSON-LD documents
(e.g. to add a missing `@type` to a JSON-LD document),
but only to support schemas that do not describe JSON-LD documents.

Applications exchanging JSON-LD documents
need to explicitly populate `@type` and `@context`,
and use a proper media type
since Linked Data processing and interpretation
requires further checks.

If these applications describe messages using [JSONSCHEMA] or [OAS],
they need to
process them with a JSON-LD processor
and declare all required properties
in the schema - like in the example below.

~~~ yaml
PersonLD:
  type: object
  required: [ "@context", "@type", "givenName", "familyName" ]
  properties:
    "@context":
      type: object
      enum:
      - "@vocab": "https://w3.org/ns/person#"
    "@type":
      type: string
      enum:
      - Person
    givenName:
      type: string
    familyName:
      type: string
~~~
{: title="A JSON-Schema describing a JSON-LD document." #ex-jsonld-schema}

## Composability {#int-composability}

Limited composability can be achieved applying the process described
in {{interpreting}}.
Automatic composability is not an explicit goal of this specification
because of its complexity. One of the issue is that
the meaning of a JSON-LD keyword is affected by
its position. For example, the `@type` keyword:

- in a node object, adds an `rdf:type` arc to the RDF graph
  (it also has a few other effects on processing, e.g. by enabling type-scoped contexts);
- in a value object, specifies the datatype of the produced literal;
- in the context, and more precisely in a term definition,
  specifies [type coercion](https://www.w3.org/TR/json-ld11/#type-coercion).
  It only applies when the value of the term is a string.

These issues can be tackled in future versions of this specifications.

Moreover, well-designed schemas do not usually have
more than 3 or 4 nested levels.
This means that, when needed, it is possible
to assemble and optimize an instance context (see {{keywords}})
at design time and use it to valorize x-jsonld-context
(see {{ex-redundant-context}}).

Once a context is assembled, the RDF data can be
generated using the algorithms described in [JSONLD-11-API]
for example through a library.

~~~ python
from pyld import jsonld
...
jsonld_text = jsonld.expand(schema_instance, context)
~~~

# Security Considerations {#sec}

See the interoperability considerations for the media types
and specifications used, including [YAML-IANA], [JSON], [OAS],
[JSONSCHEMA] and [JSON-LD-11].

## Integrity and Authenticity {#sec-integrity}

Adding a semantic context to a JSON document
alters its value and, in an implementation-dependent way,
can lead to reordering of fields.
This process can thus affect the processing of digitally signed content.

## Conflicts {#sec-conflicts}

If an OAS document includes the keywords defined in {{keywords}}
the provider explicitly states that the semantic of the schema instance:

- is defined at contract level;
- is the same for every message;
- and is not conveyed nor specific for each message.

In this case, processing the semantic conveyed in a message
might have security implications.

An application that relies on this specification
might want to define separate processing streams for JSON documents
and RDF graphs, even when RDF graphs are serialized as JSON-LD documents.
For example, it might want to raise an error
when an `application/json` resource contains unexpected properties
impacting on the application logic
like `@type` and `@context`.

# IANA Considerations {#iana}

None

--- back

# Examples {#ex}

## Schema with semantic information

The following example shows a
Person JSON Schema with semantic information
provided by the x-jsonld-type and x-jsonld-context.
Type information is provided as a URI reference.

~~~ example
Person:
  "x-jsonld-type": "https://schema.org/Person"
  "x-jsonld-context":
     "@vocab": "https://schema.org/"
     custom_id: null  # detach this property from the @vocab
     country:
       "@id": addressCountry
       "@language": en
  type: object
  required:
  - given_name
  - family_name
  properties:
    familyName: { type: string, maxLength: 255  }
    givenName:  { type: string, maxLength: 255  }
    country:    { type: string, maxLength: 3, minLength: 3 }
    custom_id:  { type: string, maxLength: 255  }
  example:
    familyName: "Doe"
    givenName: "John"
    country: "FRA"
    custom_id: "12345"
~~~
{: title="A JSON Schema data model with semantic context and type." #ex-base}

The example object is assembled as a JSON-LD object as follows.

~~~ json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "custom_id": null
  },
  "@type": "https://schema.org/Person",
  "familyName": "Doe",
  "givenName": "John",
  "country": "FRA",
  "custom_id": "12345"
}
~~~

The above JSON-LD can be represented as `text/turtle` as follows.

~~~ text
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
@prefix schema: <https://schema.org/>

_:b0 rdf:type schema:Person    ;
     schema:country     "FRA"  ;
     schema:familyName  "Doe"  ;
     schema:givenName   "John" .
~~~

## Schema with semantic and vocabulary information {#ex-semantic-and-vocabulary}

The following example shows a
"Person" schema with semantic information
provided by the x-jsonld-type and x-jsonld-context.

~~~ example
Person:
  "x-jsonld-type": "https://schema.org/Person"
  "x-jsonld-context":
     "@vocab": "https://schema.org/"
     email: "@id"
     custom_id: null  # detach this property from the @vocab
     country:
       "@id": addressCountry
       "@type": "@id"
       "@context":
          "@base": "http://publications.europa.eu/resource/authority/country/"

  type: object
  required:
  - email
  - given_name
  - family_name
  properties:
    email: { type: string, maxLength: 255  }
    familyName: { type: string, maxLength: 255  }
    givenName:  { type: string, maxLength: 255  }
    country:    { type: string, maxLength: 3, minLength: 3 }
    custom_id:  { type: string, maxLength: 255  }
  example:
    familyName: "Doe"
    givenName: "John"
    email: "jon@doe.example"
    country: "FRA"
    custom_id: "12345"
~~~
{: title="A JSON Schema data model with semantic context and type." #ex-complete-example}

The resulting RDF graph is

~~~ text
@prefix schema: <https://schema.org/> .
@prefix country: <http://publications.europa.eu/resource/authority/country/> .

<mailto:jon@doe.example>
  schema:familyName "Doe"          ;
  schema:givenName "John"          ;
  schema:addressCountry country:FRA .
~~~
{: title="An RDF graph with semantic context and type." #ex-rdf-from-json}

## Cyclic schema {#ex-cyclic-schema}

The following schema contains a cyclic reference.
Type information is resolved using the `@vocab` keyword
specified in the x-jsonld-context.

~~~ yaml
Person:
  description: Simple cyclic example.
  x-jsonld-type: Person
  x-jsonld-context:
    "email": "@id"
    "@vocab": "https://w3.org/ns/person#"
    children:
      "@container": "@set"
  type: object
  properties:
    email: { type: string }
    children:
      type: array
      items:
        $ref: '#/Person'
  example:
    email: "mailto:a@example"
    children:
    - email: "mailto:dough@example"
    - email: "mailto:son@example"
~~~

The example schema instance contained in the above schema
results in the following JSON-LD document.

~~~ json
{
  "email": "mailto:a@example",
  "children": [
    {
      "email": "mailto:dough@example",
      "@type": "Person"
    },
    {
      "email": "mailto:son@example",
      "@type": "Person"
    }
  ],
  "@type": "Person",
  "@context": {
    "email": "@id",
    "@vocab": "https://w3.org/ns/person#",
    "children": {
      "@container": "@set"
    }
  }
}
~~~

Applying the workflow described in {{interpreting}}
just recursively copying the x-jsonld-context,
the instance context could have been more complex.

~~~ json
{
  ...
  "@context": {
    "email": "@id",
    "@vocab": "https://w3.org/ns/person#",
    "children": {
      "@container": "@set",
      "@context": {
        "email": "@id",
        "@vocab": "https://w3.org/ns/person#",
        "children": {
          "@container": "@set"
        }
      }
    }
  }
}
~~~
{:title="An instance context containing redundant information" #ex-redundant-context}

## Composite instance context {#ex-instance-context}

In the following schema document,
the "Citizen" schema references the "BirthPlace" schema.

~~~ yaml
BirthPlace:
  x-jsonld-type: https://w3id.org/italia/onto/CLV/Feature
  x-jsonld-context:
    "@vocab": "https://w3id.org/italia/onto/CLV/"
    country:
      "@id": "hasCountry"
      "@type": "@id"
      "@context":
        "@base": "http://publications.europa.eu/resource/authority/country/"
    province:
      "@id": "hasProvince"
      "@type": "@id"
      "@context":
        "@base": "https://w3id.org/italia/data/identifiers/provinces-identifiers/vehicle-code/"
  type: object
  required:
    - province
    - country
  properties:
    province:
      description: The province where the person was born.
      type: string
    country:
      description: The iso alpha-3 code of the country where the person was born.
      type: string
  example:
    province: RM
    country: ITA
Citizen:
  x-jsonld-type: Person
  x-jsonld-context:
    "email": "@id"
    "@vocab": "https://w3.org/ns/person#"
  type: object
  properties:
    email: { type: string }
    birthplace:
      $ref: "#/BirthPlace"
  example:
    email: "mailto:a@example"
    givenName: Roberto
    familyName: Polli
    birthplace:
      province: LT
      country: ITA

~~~
{: title="A schema with object contexts." #ex-object-contexts}

The example schema instance contained in the above schema
results in the following JSON-LD document.
The instance context contains information from both
"Citizen" and "BirthPlace" semantic keywords.

~~~ json
{
  "email": "mailto:a@example",
  "givenName": "Roberto",
  "familyName": "Polli",
  "birthplace": {
    "province": "RM",
    "country": "ITA",
    "@type": "https://w3id.org/italia/onto/CLV/Feature"
  },
  "@type": "Person",
  "@context": {
    "email": "@id",
    "@vocab": "https://w3.org/ns/person#",
    "birthplace": {
      "@context": {
        "@vocab": "https://w3id.org/italia/onto/CLV/",
        "city": "hasCity",
        "country": {
          "@id": "hasCountry",
          "@type": "@id",
          "@context": {
            "@base": "http://publications.europa.eu/resource/authority/country/"
          }
        },
        "province": {
          "@id": "hasProvince",
          "@type": "@id",
          "@context": {
            "@base": "https://w3id.org/italia/data/identifiers/provinces-identifiers/vehicle-code/"
          }
        }
      }
    }
  }
}
~~~
{:title="A @context that includes information from different schemas." #ex-composite-context}

That can be serialized as `text/turtle` as

~~~ text
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix eu: <https://w3.org/ns/person#> .
@prefix itl: <https://w3id.org/italia/onto/CLV/> .

<mailto:a@example>
  rdf:type eu:Person ;
  eu:birthplace _:b0 ;
  eu:familyName "Polli" ;
  eu:givenName  "Roberto"
.
_:b0 rdf:type itl:Feature ;
  itl:hasCountry <http://publications.europa.eu/resource/authority/country/ITA> .
  itl:hasProvince <https://w3id.org/italia/data/identifiers/provinces-identifiers/vehicle-code/RM>
.
~~~
{:title="The above entry in text/turtle" #ex-composite-context-turtle}

## Identifiers and IRI Expansion {#ex-iri-expansions}

IRI expansion expects string identifiers,
so an `@id` that should be expanded in conjunction with a `@base`
can only be assigned to `string` properties.

~~~ yaml

Person:
  type: object
  x-jsonld-type: "Person"
  x-jsonld-context:
    "@vocab": "https://w3id.org/italia/onto/CPV/"
    "@base": "https://example.org/people/"
    taxCode: "@id"  # taxCode is a string property.
  required:
  - taxCode
  properties:
    # Since taxCode is an identifier to be expanded
    #   with @base, it must be a string.
    taxCode:
      type: string
  example:
    taxCode: "RSSMRA85M01H501U"
~~~
{: title="A schema that uses IRI expansion with a string property." #ex-iri-expansion}

# Acknowledgements

Thanks to Giorgia Lodi, Matteo Fortini and Saverio Pulizzi for being the initial contributors of this work.

In addition to the people above, this document owes a lot to the extensive discussion inside
and outside the workgroup.
The following contributors have helped improve this specification by
opening pull requests, reporting bugs, asking smart questions,
drafting or reviewing text, and evaluating open issues:

Pierre-Antoine Champin,
and Vladimir Alexiev.

# FAQ
{: numbered="false" removeinrfc="true"}

Q: Why this document?
:  There's currently no standard way to provide machine-readable semantic
   information in [OAS] / [JSONSCHEMA] to be used at contract time.

Q: Does this document support the exchange of JSON-LD resources?
:  This document is focused on annotating schemas that are used
   at contract/design time, so that application can exchange compact
   JSON object without dereferencing nor interpreting
   external resources at runtime.

   While you can use the provided semantic information to generate
   JSON-LD objects, it is not the primary goal of this specification:
   context information are not expected to be dereferenced at runtime
   (see security considerations in JSON-LD)
   and the semantics of exchanged messages is expected
   to be constrained inside the application.

Q: Why don't use existing [JSONSCHEMA] keywords like `externalDocs` ?
:  We already tried, but this was actually squatting a keyword designed
   for [human readable documents](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#externalDocumentationObject).

Q: Why using `x-` keywords?
:  OpenAPI 3.0 considers invalid unregistered keywords that don't start with `x-`,
   and we want a solution that is valid for all OAS versions >= 3.0.

Q: Why not using a full-semantic approach?
:  This approach allows API providers to attach metadata to their
   specification without modifying their actual services nor their
   implementation, since custom keywords are ignored by OpenAPI toolings
   like Gateways and code generators.

Q: Why not defining a mechanism to attach semantic information to
   non-object schemas (e.g. JSON Strings) like other implementations?
:  This is actually problematic. Look at this example that reuses
   the `TaxCode` schema and semantic in different properties.

Q: Why don't use SHACL or OWL restrictions instead of JSON Schema?
:  Web and mobile developers consider JSON Schema is easier to use than SHACL.
   Moreover, OWL restrictions are about semantics,
   and are not designed to restrict the syntax.

Q: Why don't design for composability first?
:  JSON-LD is a complex specification.
   Consider the following schemas, where `Contract` references `TaxCode`.

~~~ yaml
    TaxCode:
      type: string
      $linkedData:
        "@id": "https://w3id.org/italia/onto/CPV/taxCode"
        "term": "taxCode"
    Contract:
      ...
      properties:
        employer_tax_code:
          # Beware! TaxCode.$linkedData.term == 'taxCode'
          $ref: "#/components/schemas/TaxCode"
        employee_tax_code:
          # Here we are reusing not only the schema,
          #   but even the same term.
          $ref: "#/components/schemas/TaxCode"
~~~

  The result will be that only one of the properties will be correctly annotated.
  For this reason, composability is limited to the object level.

Q: Can the value of `x-jsonld-type` be an `rdf:Property`? Would this allow to reuse the same schema in different objects without modifying the `@context`?
:  Under normal circumstances, i.e. when designing public or financial service APIs,
   you don't want `x-jsonld-type` to be an `rdf:Property`.
   The value of `x-jsonld-type` usually maps to a `owl:Class`, not an `owl:DataTypeProperty`;
   for example a sensible value for `x-jsonld-type` would be `rdfs:Literal` (that is, the `rdfs:range` of `CPV:taxCode`),
   but this would be mostly a syntactic information, which instead is provided by JSON Schema.

~~~ yaml
    TaxCode:
      type: string
      x-jsonld-type: "https://w3id.org/italia/onto/CPV/taxCode"
      description: |-
        This example is ambiguous, because:

        1. it treats a CPV:taxCode as an owl:Class,
           while it's an owl:DataTypeProperty;
        2. the `rdfs:range` for CPV:taxCode is `rdfs:Literal`.
~~~
{: title="The above code is ambiguous, because the rdfs:range of CPV:taxCode is rdfs:Literal" #ex-invalid-x-jsonld-type}

# Change Log
{: numbered="false" removeinrfc="true"}

TBD
