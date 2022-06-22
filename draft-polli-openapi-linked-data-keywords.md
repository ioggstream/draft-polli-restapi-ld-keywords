---
title: OpenAPI Linked Data Keywords
abbrev:
docname: draft-polli-openapi-linked-data-keywords-latest
category: info

ipr: trust200902
area: General
workgroup:
keyword: Internet-Draft

stand_alone: yes
pi: [toc, tocindent, sortrefs, symrefs, strict, compact, comments, inline, docmapping]

venue:
  home: https://github.com/ioggstream/draft-polli-openapi-linked-data-keywords
  repo: https://github.com/ioggstream/draft-polli-openapi-linked-data-keywords/issues
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

informative:
  I-D.ietf-jsonpath-base:
  JSON-POINTER: RFC6901
  JSONLD-11-API:
    target: https://www.w3.org/TR/json-ld11-api/
    title: JSON-LD 1.1 Processing Algorithms and API
  RDF:
    title: RDF Concepts and Abstract Syntax
    target: https://www.w3.org/TR/rdf11/
  SHACL:
    title: Shapes Constraint Language (SHACL)
    target: https://www.w3.org/TR/shacl/
    date: 2017-07-20
  OWL:
    title: OWL 2 Web Ontology Language Document Overview
    target: https://www.w3.org/TR/owl2-overview/

--- abstract

This document defines two OpenAPI Specification
keywords to provide semantic information in
Schema objects.

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

Moreover  the semantic landscape do not provide easy ways of defining / constraining
the syntax of an object:
tools like [SHACL] and [OWL] restrictions are considered
computationally intensive to process and complex to use
from the web and mobile developers.

The goal of this document is to simplify
the work of attaching semantic information to REST APIs
described using OpenAPI Specification [OAS].

[OAS] allows to describe REST APIs
interactions and capabilities using a machine-readable format
based on [JSON] or [YAML].
It relies on different dialects of [JSONSCHEMA] to define the structure of the exchanged data.
Specifically, OAS 3.0 is based on JSON Schema draft-4
while OAS 3.1 relies on the latest JSON Schema draft.

## Goals and Design Choices

This document has the following goals:

- Describe in a single OAS document both the syntax and semantics
   of a JSON object. This information can be either be provided
   editing the document by hand or via automated tools;
- Describe semantically the contents defined in an API spec or in a [JSONSCHEMA] document;
- Support for OAS3.0 / JSON Schema Draft4
- Easy for non-semantic experts and with low implementation complexity

while it does not aim to:

- infer semantic information where it is not provided;
- convert automatically RDF to [JSONSCHEMA] or [OAS] documents.

Thus, the following design choices have been made:

- the semantic context of a JSON object will be described
  using [JSON-LD-11] and its keywords;
- the semantic context can be provided via APIs
  using a "Link" header field according to Section 6.1 of [JSON-LD-11];
- property names are limited to characters that can be used in variable
  names (e.g. excluding `:` and `.`)
  to avoid interoperability issues with code-generation tools.

## Prosaic semantics {#prosaic-semantics}

[JSONSCHEMA] allows to define the structure of the exchanged data using specific keywords.
Property semantic is defined in prose via the `description` keyword.

~~~ yaml
Person:
  $schema: https://json-schema.org/draft/2020-12/schema,
  $id: https://example.com/person.schema.json,
  title: Person,
  description: A Person,
  type: object
  properties:
    givenName:
      description: The given name of a Person
      type: string
    familyName:
      description: The family name, or surname, of a Person
      type: string
  example:
    givenName: John
    familyName: Doe
~~~
{: title="Example of JSON Schema model that provides semantic prose." #ex-semantic-prose}

[JSON-LD-11] defines a way to interpret a JSON object as a JSON-LD document.
The example in the "Person" schema can be integrated with
semantic context information, thus resulting in

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
{: title="Example of JSON-LD object." #ex-json-ld}

This specification only applies to JSON objects,
this means that other JSON types cannot be
integrated with semantic information.

The design described in the following sections aims
at providing the above information of "@context" and "@type"
into a JSON Schema document.

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
in this document are to be intepreded as in [JSONSCHEMA].

The terms "JSON object", "JSON document", "member", "member name"
in this document are to be intepreded as in [JSON].
The term "property" - when referred to a JSON document
such as a schema instance -
is a synonym of "member name",
and the term "property value" is a synonym of "member value".

The terms "@context", "@type", "@id", "@value" and "@language" are to be interpreted as JSON-LD keywords in [JSON-LD-11].

Since JSON-LD is a serialization format for RDF,
the document can use JSON-LD and RDF interchangeably
when it refers to the semantic interpretation of a resource.

# JSON Schema keywords {#keywords}

A [JSONSCHEMA] or [OAS] document MAY
use the following JSON Schema keywords to
attach semantic information to a schema
and represent that those information applies
to all related schema instances.

x-jsonld-context:
: This keyword is used to provide a JSON-LD context
   for the JSON schema instances described by the associate
   schema. It is defined  in {{keywords-context}}.

x-jsonld-type:
: This keyword is used to provide an RDF type
   for the JSON schema instances described by the associate
   schema.

The schema MUST be of type "object".
This is because [JSON-LD-11] does not define a way
to provide semantic information on JSON values that
are not JSON objects.

The schema MUST NOT represent a JSON-LD resource
(e.g. of `application/ld+json` media type).
In this case, conflicts will arise such as
which is the correct "@context" or "@type".
See {{sec-conflicts}}.

Both JSON Schema keywords might contain URI references.
Those references MUST NOT be dereferenced automatically,
since there is no guarantee that they point to actual
locations. Moreover they could reference unsecured resources
(e.g. using the "http://" URI scheme [HTTP]).

## The x-jsonld-context JSON Schema keyword {#keywords-context}

The x-jsonld-context value
provides the information required to interpret the associate
schema instance as a JSON-LD
according to the specification in [Section 6.1 of JSON-LD-11](https://www.w3.org/TR/json-ld11/#interpreting-json-as-json-ld).

Its value MUST be a valid JSON-LD Context (see
[Section 9.15 of JSON-LD-11](https://www.w3.org/TR/json-ld11/#context-definitions)
).

When context composition (see {{int-composability}}) is needed,
the JSON-LD Context SHOULD be provided in the form of a JSON object.

## Interpreting schema instances {#interpreting}

To interpret a schema instance as JSON-LD:

1. ensure that the initial schema instance does not have
   a "@context" and a "@type" property.
   For further information see {{sec-conflicts}};
1. add the "@context" property with the value of x-jsonld-context.
   This will be the "instance context": the only one that will be mangled;
1. add the "@type" property with the value of x-jsonld-type;
1. iterate on each instance property like the following:

   - identify the sub-schema associated to the property (e.g. traversing $refs)
     and check the presence of semantic keywords;
   - for the x-jsonld-type, add the "@type" property to the sub-instance;
   - for the x-jsonld-context, integrate its information in the instance context
     when they are not already present;
   - interate this process in case of nested entries.

The specific algorithm
for integrating the values of x-jsonld-context into the
instance context is an implementation detail.
Note that if the x-jsonld-context is an URL,
an implementation that wants to automatically
generate the instance context needs to dereference
that URL. This is not trivial.

NOTE: not a replacement for xsd/xmlschema in jsonschema.

# Interoperability Considerations {#int}

See the interoperability considerations for the media types
and specifications used, including [YAML], [JSON], [OAS],
[JSONSCHEMA] and [JSON-LD-11].

Since this specification relies on JSON-LD keywords such as
"@context" and "@type", a document of this type cannot be
interpreted as a JSON-LD document.
This is generally not a problem, since it is a document
following the [OAS] and [JSONSCHEMA] specification.

## Limited expressivity {#int-limitations}

Not all RDF resources can be expressed as JSON documents
annotated with "@context" and "@type":
this specifications is limited by the possibilities
of [Section 6.1 of JSON-LD-11](https://www.w3.org/TR/json-ld11/#interpreting-json-as-json-ld).
On the other hand, since this approach
delegates almost all the processing to of JSON-LD,
as long as JSON-LD evolves
it will cover more an more use cases.

## URL contexts {#int-url-contexts}

When a context is expressed by an URL, implementing
an automatic resolution algorithm is not trivial.
In general adopting this specification requires
a proper design of schemas and contexts.

~~~ example
Person:
  x-jsonld-context: https://ctx.example/context.jsonld
  type: object
~~~
{: title="Example of an URL context." #ex-url-context}

## Disjoint with JSON-LD {#int-no-jsonld}

This specification is not designed to pre-process
or mangle JSON-LD documents
(e.g. to add a missing "@type" to a JSON-LD document),
but only schemas that do not describe JSON-LD documents.

Applications exchanging JSON-LD documents
need to explicitly populate "@type" and "@context",
and use a proper media type
since Linked Data processing and interpretation
requires further checks.

If that application describe messages using [JSONSCHEMA] or [OAS],
it needs to
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

## Composability {#int-composability}

Composability can be achieved applying the process described
in {{interpreting}}.
This process is inherently complex and composability
is not one of the explicit goal of this specification.

Well-designed schemas do not usually have
more than 3 or 4 nested levels.
This means that, when needed, it is possible
to assemble and optimize an instance context (see {{interpreting}})
at design time and set the value of x-jsonld-context manually

Once a context is assembled, the RDF data can be
generated using the algoritms described in [JSONLD-11-API]
for example through a library.

~~~ python
from pyld import jsonld
...
jsonld_text = jsonld.expand(schema_instance, context)
~~~

# Security Considerations {#sec}

See the interoperability considerations for the media types
and specifications used, including [YAML], [JSON], [OAS],
[JSONSCHEMA] and [JSON-LD-11].

## Integrity and Authenticity {#sec-integrity}

Adding a semantic context to a JSON document
alters its value and, in an implementation dependant way,
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
like "@type" and "@context".

# IANA Considerations {#iana}

None

--- back

# Examples {#ex}

## Schema with semantic information

The following example shows a
Person JSON Schema with semantic information
provided by the x-jsonld-type and x-jsonld-context.

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
_:b0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Person> .
_:b0 <https://schema.org/country> "FRA" .
_:b0 <https://schema.org/familyName> "Doe" .
_:b0 <https://schema.org/givenName> "John" .
~~~


## Schema with semantic and vocabulary information {#ex-semantic-and-vocabulary}

The following example shows a
Person JSON Schema with semantic information
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

The resulting RDF graph is as follows.

~~~ text
@prefix schema: <https://schema.org/> .
@prefix country: <http://publications.europa.eu/resource/authority/country/> .

<mailto:jon@doe.example>
  schema:addressCountry country:FRA;
  schema:familyName "Doe"          ;
  schema:givenName "John"          .
~~~
{: title="A RDF graph with semantic context and type." #ex-rdf}


## Cyclic schema

The following schema contains a cyclic reference.

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

The example contained in the above schema
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

## Nested schema

The following schema references another schema.

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
  additionalProperties: false
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

The example contained in the above schema
results in the following JSON-LD document.

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
   information in [OAS] / [JSONSCHEMA].

Q: Why don't use existing [JSONSCHEMA] keywords like `externalDocs` ?
:  We already tried, but this was actually squatting a keyword designed
   for [human readable documents](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#externalDocumentationObject).

Q: Why using `x-` keywords?
:  OpenAPI 3.0 does not validate unregistered keywords that don't start with `x-`
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
          #   but even the same semantics.
          $ref: "#/components/schemas/TaxCode"
~~~

    For this reason, composability is limited to the object level.

# Change Log
{: numbered="false" removeinrfc="true"}

RFC EDITOR PLEASE DELETE THIS SECTION.
