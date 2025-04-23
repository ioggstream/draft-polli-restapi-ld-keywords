---
title: Designing APIs with REST API Linked Data Keywords
abbrev:
docname: draft-polli-design-process-latest
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
    org: Par-Tec S.p.A.
    email: robipolli@gmail.com
    country: Italy

normative:
  LD-KEYWORDS: I-D.polli-restapi-ld-keywords
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
    target: https://www.w3.org/TR/rdf11/
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

This document provides guidance
for designing schemas using REST API Linked Data keywords.

--- middle

# Introduction

This document provides guidance and examples
for JSON Schema modeling using
and REST API Linked Data keywords.

Since REST API Linked Data keywords only support
JSON-LD compact notation, this document
focuses on JSON objects.

## Goals and Design Choices

TBD

## Notational Conventions

{::boilerplate bcp14+}

All JSON samples are represented in YAML format
for readability and conciseness.

The terms "primitive types" and "structured types",
 are from {{Section 1 of JSON}}.

The terms "JSON document", "JSON object", "JSON array" are from {{JSON}}.

The terms "schema", "schema instance", "keyword" are from {{JSONSCHEMA}};
the term "schema instance" referso to a JSON document
that conforms to a JSON Schema.
Schema instances are conveyed in the `example`
JSON Schema keyword.

Examples can be viewed opening [this link in the schema editor](https://par-tec.github.io/dati-semantic-schema-editor/latest/?url=https://raw.githubusercontent.com/ioggstream/draft-polli-restapi-ld-keywords/refs/heads/main/tests/text-based-entries.oas3.yaml).

# Models based on non-object types

To ensure that the API is extensible and that the data can be easily enriched with additional information,
it is a best practice to only convey JSON objects,
with other types (primitive or array) being used as references (i.e., using the `$ref` keyword).

Moreover:

- non-object values
  cannot be directly mapped to an RDF triple,
  as they require a subject and a predicate.
- JSON-LD only supports JSON objects (compact form)
  and JSON arrays (expanded form).

For this reason, {{LD-KEYWORDS}} does not support
adding `x-jsonld-type` and `x-jsonld-context` to non-object schemas.

For example, the schema instance associated with
the following schema is the string `Diego Maria`.

~~~ yaml
    GivenName:
      type: string
      maxLength: 64
      example: Diego Maria
~~~
{: title="A JSON Schema for a simple text entry." #ex-given-name }

## Simple text values

A modeling strategy for non-object values is to
create reusable syntax blocks (i.e., constraining the length or the character set according to the specifications),
and to defer the semantics to the containing JSON object.

This approach ensures that the same schema can be used in different contexts.

~~~ yaml
    RegistryString:
      type: string
      maxLength: 64
      description: >-
        A string that can be used to represent a givenName, a familyName, a patronymicName, or any other string
        associated with a naming property registry information.
    Person:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
      type: object
      properties:
        givenName:
          $ref: "#/components/schemas/RegistryString"
        familyName:
          $ref: "#/components/schemas/RegistryString"
      example:
        givenName: Diego Maria
        familyName: De La Peña
~~~
{: title="Reusing a syntactic schema with different semantics." #ex-registry-string}

This allows focusing on the semantics of the JSON object,
while isolating the efforts of properly constraining the syntax
according to the requirement of the specific API.

It is possible, in fact, that syntax constraints may change
over time, while the semantics of the object remain the same.

A specific service might require, for example, specific string
constraints such as latinized uppercase.

~~~ yaml
    RegistryStringL:
      type: string
      maxLength: 64
      description: >-
        A latinized string.
      pattern: "^[A-Z ]+$"
    PersonL:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
      type: object
      properties:
        givenName:
          $ref: "#/components/schemas/RegistryStringL"
        familyName:
          $ref: "#/components/schemas/RegistryStringL"
      example:
        givenName: DIEGO MARIA
        familyName: DE LA PENHA
~~~
{: title="A JSON Schema for a latinized string." #ex-latinized-string}

The resulting RDF graph is

~~~ text
@prefix schema: <https://schema.org/> .

_:b0
  a schema:Person ;
  schema:familyName "De La Vega" ;
  schema:givenName "Diego Maria" .
~~~


## Modeling identifiers

Identifiers are a special case of text-based entries,
and isolating syntax from semantics can make things more
readable.

~~~ yaml
    NumericTaxCode:
      description: >-
        Legal persons have a 11-digit tax code.
      type: string
      pattern: "^[0-9]{11}$"
      example: "12345678901"
    StringTaxCode:
      description: >-
        Natural persons have a 16-character tax code.
      type: string
      pattern: "^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$"
      example: RSSMRO99A04H501A
    TaxCode:
      description: >-
        This is a purely syntactic definition, and can
        be used in different semantic contexts.
      oneOf:
        - $ref: "#/components/schemas/NumericTaxCode"
        - $ref: "#/components/schemas/StringTaxCode"
    PersonID:
      description: >-
        The Person identifier is a 16-character string.
      type: string
      pattern: "^[0-9]{16}$"
      example: "1234567890123456"
~~~
{: title="Data models building blocks based on primitive types." #ex-primitive-types}

These schemas can be reused both when using their values
as identifiers or as simple property values.

The following schema uses a tax code as an identifier.

~~~ yaml
    Person:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
        tax_code: "@id"
        "@base": "urn:example:tax:it:"
        given_name: givenName
        family_name: familyName
      type: object
      required: [tax_code]
      properties:
        tax_code:
          $ref: "#/components/schemas/TaxCode"
        given_name:
          $ref: "#/components/schemas/RegistryString"
        family_name:
          $ref: "#/components/schemas/RegistryString"
        children:
          type: array
          items:
            $ref: "#/components/schemas/Person"
      example:
        given_name: Mario
        family_name: Rossi
        tax_code: RSSMRO99A04H501A
        children:
        - tax_code: RSSLCC99A04H501A
~~~

The associated RDF graph is:

~~~ text
urn:example:tax:it:RSSMRO99A04H501A
  a schema:Person ;
  schema:givenName "Mario" ;
  schema:familyName "Rossi" ;
  schema:children
  urn:example:tax:it:RSSLCC99A04H501A
.
~~~

This other schema uses `person_id` property as identifier,
while `tax_code` is a simple property value.

~~~ yaml
    RegisteredPerson:
      x-jsonld-type: RegisteredResidentPerson
      x-jsonld-context:
        "@vocab": "https://schema.org/"
        "@base": "urn:example:anpr.it:"
        person_id: "@id"
        tax_code: taxCode
        given_name: givenName
        family_name: familyName
      type: object
      required: [tax_code]
      properties:
        person_id:
          $ref: "#/components/schemas/PersonID"
        tax_code:
          $ref: "#/components/schemas/TaxCode"
        given_name:
          $ref: "#/components/schemas/RegistryString"
        family_name:
          $ref: "#/components/schemas/RegistryString"
        children:
          type: array
          items:
            $ref: "#/components/schemas/RegisteredPerson"
      example:
        given_name: Mario
        family_name: Rossi
        person_id: "1234567890123456"
        tax_code: RSSMRO99A04H501A
        children:
        - person_id: "2234567890123457"
          tax_code: RSSLCC99A04H501A
~~~

The resulting RDF consists in two, linked nodes,
where the identifier is the `person_id` property.

~~~ text
<urn:example:person:1234567890123456>
  a schema:RegisteredResidentPerson ;
  schema:givenName "Mario" ;
  schema:familyName "Rossi" ;
  schema:taxCode "RSSMRO99A04H501A" ;
  schema:children
  <urn:example:person:2234567890123457>
.
<urn:example:person:2234567890123457>
  a schema:RegisteredResidentPerson ;
  schema:taxCode "RSSLCC99A04H501A"
.
~~~

Note that the changes to the schema instances
were minimal: just the addition of the `person_id` JSON Schema property.

# Modeling an vocabulary-bases entry

There are different ways to model a vocabulary-based entry,
e.g., a list of countries or a list of currencies.

Normally, you would use a JSON Schema (e.g., with an `enum` keyword):

~~~ yaml
    CountryCode:
      type: string
      enum: [ "ITA", "FRA", "DEU" ]
      example: ITA
~~~
{: title="A JSON Schema for a Country enumeration." #ex-country-enum }

The resulting schema instance is a simple string
(e.g. `ITA`).
To be able to represent the entry in JSON-LD,
an enumerated entry can be modeled using
a specific property for the identifier,
and a JSON-LD context.

~~~ yaml
    Country:
      type: object
      properties:
        identifier:
          $ref: "#/components/schemas/CountryCode"
        name:
          type: string
      example:
        identifier: ITA
        name: Italy
~~~

Linked Data keywords provide a context.
Different contexts can lead to different
RDF representations for the same schema instances (i.e. the actual data).

1. A "property-to-property" representation preserves the mapping between JSON object members and RDF properties;
with the only addition of the `@type` keyword if `x-jsonld-type` is present.

The following schema instance

~~~ yaml
    CountryBlankNode:
      x-jsonld-type: Country
      x-jsonld-context:
        "@vocab": "https://schema.org/"
      type: object
      properties:
        identifier:
          "$ref": "#/components/schemas/CountryCode"
        name:
          type: string
      example:
        identifier: ITA
        name: Italy
~~~

results in this RDF graph with a blank node:

~~~ text
@prefix schema: <https://schema.org/> .

_:b0
  schema:identifier "ITA" ;
  schema:name "Italy" .
~~~
{: title="An RDF graph with a blank node." #ex-country-rdf-blank-node}

2. A non-isomorphic representation maps one property to the node name.

Associating a property with the `@id` keyword and a `@base` prefix,
we state that the corresponding value is the name of the node.
This schema

~~~ yaml
    CountryURI:
      x-jsonld-type: Country
      x-jsonld-context:
        "@vocab": "https://schema.org/"
        identifier: "@id"
        "@base": "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3#"
      type: object
      properties:
        identifier:
          $ref: "#/components/schemas/CountryCode"
        name:
          type: string
      example:
        identifier: ITA
        name: Italy
~~~

results in the following RDF graph using a named node:

~~~ text
@prefix schema: <https://schema.org/> .
@prefix iso_3166_3: <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3#> .

iso_3166_3:ITA
  a schema:Country;
  schema:name "Italy"
.
~~~
{: title="An RDF graph with a named node." #ex-country-rdf-named-node}

## Modeling an object with references

When modeling an object with references,
the parent's context will normally provide the context for the child.

The following example models a `Person` object with a `nationality` property
referencing the `CountryCode` schema.
The x-jsonld-context ensures that the `nationality` property will be resolved to an URI,
though there is no space in the schema instance to provide a name for the country.

~~~ yaml
    Person:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
        nationality:
          "@type": "@id"
          "@context":
            "@base": "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3#"
      type: object
      properties:
        givenName:
          type: string
        familyName:
          type: string
        nationality:
          $ref: "#/components/schemas/CountryCode"
      example:
        givenName: John
        familyName: Doe
        nationality: ITA
~~~

results in the following RDF graph:

~~~ text
@prefix schema: <https://schema.org/> .
@prefix iso_3166_3: <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3#> .

_:b0
  a schema:Person ;
  schema:familyName "Doe" ;
  schema:givenName "John" ;
  schema:nationality iso_3166_3:ITA .
~~~
{: title="An RDF graph with a named node." #ex-person-rdf}

To provide a label or other properties for the country, we can use a nested object.

~~~ yaml
    NestedPerson:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
      type: object
      properties:
        givenName:
          type: string
        familyName:
          type: string
        nationality:
          $ref: "#/components/schemas/CountryURI"
      example:
        givenName: John
        familyName: Doe
        nationality:
          identifier: ITA
          name: Italy
~~~

An implementation supporting context composition
will check that the value of `NestedPerson/x-jsonld-context/nationality/@context` is undefined,
and will then integrate the information present in `CountryURI/x-jsonld-context` into the instance context.

results in the following RDF graph:

~~~ text
@prefix schema: <https://schema.org/> .
@prefix iso_3166_3: <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3#> .

_:b0
  a schema:Person ;
  schema:familyName "Doe" ;
  schema:givenName "John" ;
  schema:nationality iso_3166_3:ITA
.
iso_3166_3:ITA
  schema:name "Italy"
.
~~~
{: title="An RDF graph with two nodes." #ex-nested-person-rdf}


## Interpreting schema instances {#interpreting}

# Reusability

## YAML Anchors and Merge Keys {#yaml-anchors}

YAML anchors [YAML] can be used to define reusable components.

~~~ yaml
# A reusable schema component
openapi: 3.0.0
...
components:
  schemas:
    RegistryString:
      type: string
      maxLength: 64 &maxlength
    RegistryStringL:
      type: string
      maxLength: *maxlength
    Person:
      x-jsonld-type: Person
      x-jsonld-context: &Person_context
        "@vocab": "https://schema.org/"
      type: object
      properties:
        givenName:
          $ref: "#/components/schemas/RegistryString"
        familyName:
          $ref: "#/components/schemas/RegistryString"
      example:
        givenName: Diego Maria
        familyName: De La Peña
~~~

YAML 1.1 support merge keys, which can be used to merge multiple mappings into a single mapping.

This feature is not supported by all YAML parsers, but it is useful for reusing schema components.
To increase interoperability, it is possible to post-process the schema to replace merge keys with the corresponding components before releasing it,
similarly to what bundling tools do (see {{bundling}}).

~~~ yaml
openapi: 3.0.0
...
components:
  schemas:
    BasePerson:
      type: object
      properties: &BasePerson_properties
        givenName:
          $ref: "#/components/schemas/RegistryString"
        familyName:
          $ref: "#/components/schemas/RegistryString"
    Person:
      x-jsonld-type: Person
      x-jsonld-context: &Person_context
        "@vocab": "https://schema.org/"
      type: object
      properties:
        <<: *BasePerson_properties
      example:
        givenName: Diego Maria
        familyName: De La Peña
    MedicalCondition:
      ...
    Patient:
      x-jsonld-type: Patient
      x-jsonld-context:
        "@vocab": "https://schema.org/"
      type: object
      properties:
        # Include all the properties of BasePerson..
        <<: *BasePerson_properties
        # .. and add "diagnosis".
        diagnosis:
          $ref: "#/components/schemas/MedicalCondition"
      example:
        givenName: Diego Maria
        familyName: De La Peña
~~~
{: title="Reusing schema components with merge keys." #ex-merge-keys}

## Context propagation and composability

In JSON-LD, context propagates from the parent object.
See [Context Propagation](https://w3c.github.io/json-ld-syntax/#context-propagation) for more information.
For example, the RDF representation of

~~~ yaml
"@context":
  "@vocab": "https://schema.org/"
  email: "@id"
  "@base": "mailto:"
email: homer@exampe.com
children:
- email: lisa@example.com
  givenName: Lisa
~~~

is

~~~ text
@prefix : <https://schema.org/> .
<mailto:homer@example.com> :children <mailto:lisa@example.com> .
<mailto:lisa@example.com> :givenName "Lisa" .
~~~

This means that a child object inherits the context of the parent object even when the `$ref`d schema does not contain a context.

For example, the following schema

~~~ yaml
openapi: 3.0.0
# ...
components:
  schemas:
    Child:
      description: |-
        A generic child, without any specific context.
      type: object
      properties:
        telephone:
          type: string
        email:
          type: string
    Parent:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
        email: "@id"
        "@base": "mailto:"
      type: object
      properties:
        telephone:
          type: string
        email:
          type: string
        children:
          type: array
          items:
            $ref: "#/components/schemas/Child"
      example:
        email: homer@example.com
        children:
        - email: lisa@example.com
          telephone: +1-1234

~~~

produces this RDF graph:

~~~ text
@prefix : <https://schema.org/> .

<mailto:homer@example.com> a schema.org:Person .
<mailto:homer@example.com> :children <mailto:lisa@example.com> .
<mailto:lisa@example.com> :telephone "+1-1234" .
~~~

If this behavior is not desired:

1. it is possible to use the [`@propagate` keyword](https://w3c.github.io/json-ld-syntax/#context-propagation);
2. the context of the child object can be explicitly defined;
3. conflicting keywords should be re-defined in the referenced context.

This is shown in the following example:

~~~ yaml
openapi: 3.0.0
# ...
components:
  schemas:
    Child:
      description: |-
        A generic child, without any specific context.
      x-jsonld-context:
        "@vocab": "https://schema.org/"
        telephone: "@id"
        "@base": "tel:"
      type: object
      properties:
        telephone:
          type: string
        email:
          type: string
    Parent:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
        email: "@id"
        "@base": "mailto:"
      type: object
      properties:
        telephone:
          type: string
        email:
          type: string
        children:
          type: array
          items:
            $ref: "#/components/schemas/Child"
      example:
        email: homer@example.com
        children:
        - email: lisa@example.com
          telephone: +1-1234
~~~

## Bundling {#bundling}

When creating schemas, it is convenient to consolidate reusable components
in separate resources.
This eases maintenance and enables component reuse,
like shown in the following two examples.

~~~ yaml
# A definitions.yaml with reusable components at https://example.com/definitions.yaml
openapi: 3.0.0
...
components:
  schemas:
    NumericTaxCode:
      description: >-
        Legal persons have a 11-digit tax code.
      type: string
      pattern: "^[0-9]{11}$"
      example: "12345678901"
    StringTaxCode:
      description: >-
        Natural persons have a 16-character tax code.
      type: string
      pattern: "^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$"
      example: RSSMRO99A04H501A
    TaxCode:
      description: >-
        This is a purely syntactic definition, and can
        be used in different semantic contexts.
      oneOf:
        - $ref: "#/components/schemas/NumericTaxCode"
        - $ref: "#/components/schemas/StringTaxCode"
~~~
{: title="A definitions.yaml with reusable components." #ex-definitions }

~~~ yaml
openapi: 3.0.0
...
components:
  schemas:
    Person:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
      type: object
      properties:
        tax_code:
          $ref: "https://example.com/definitions.yaml#/components/schemas/TaxCode"
        ...
    ResidentPerson:
      x-jsonld-type: RPO:RegisteredResidentPerson
      x-jsonld-context:
        RPO: https://w3id.org/italia/onto/RPO/
        tax_code: '@id'
        '@base': 'urn:example:tax:it:'
      type: object
      properties:
        tax_code:
          $ref: "https://example.com/definitions.yaml#/components/schemas/TaxCode"
        ...

~~~
{: title="A schema using an external component." #ex-bundled-schema-definitions }

Bundling is the process of combining multiple OpenAPI and JSON schema documents in a single document
in order to distribute a consolidated service specification in a single file.
Bundling ensures that all necessary schema components are contained within a single file,
and avoids the need to resolve external references.

Bundling resolves all remote references,
adds them to the schema,
and replaces the associated `$ref` with a local reference.

~~~ yaml
openapi: 3.0.0
...
components:
  schemas:
    Person:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
      type: object
      properties:
        tax_code:
          $ref: "#/components/schemas/TaxCode"
        ...
    ResidentPerson:
      x-jsonld-type: RPO:RegisteredResidentPerson
      x-jsonld-context:
        RPO: https://w3id.org/italia/onto/RPO/
        tax_code: '@id'
        '@base': 'urn:example:tax:it:'
      type: object
      required:
        - tax_code
      properties:
        tax_code:
          $ref: '#/components/schemas/TaxCode'
        ...
    #
    # The bundler adds the following components to the schema.
    #
    NumericTaxCode:
      description: Legal persons have a 11-digit tax code.
      type: string
      pattern: ^[0-9]{11}$
      example: '12345678901'
    StringTaxCode:
      description: Natural persons have a 16-character tax code.
      type: string
      pattern: ^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$
      example: RSSMRO99A04H501A
    TaxCode:
      description: This is a purely syntactic definition, and can be used in different semantic contexts.
      oneOf:
        - $ref: '#/components/schemas/NumericTaxCode'
        - $ref: '#/components/schemas/StringTaxCode'
~~~
{: title="A bundled schema." #ex-bundled-schema}

Bundling can be done in different ways.
{{ex-bundling-tools}} contains a list of bundling tools.


# Reusability

## Bundling {#bundling}

When creating schemas, it is convenient to consolidate reusable components
in separate resources.
This eases maintenance and enables component reuse,
like shown in the following two examples.

~~~ yaml
# A definitions.yaml with reusable components at https://example.com/definitions.yaml
openapi: 3.0.0
...
components:
  schemas:
    NumericTaxCode:
      description: >-
        Legal persons have a 11-digit tax code.
      type: string
      pattern: "^[0-9]{11}$"
      example: "12345678901"
    StringTaxCode:
      description: >-
        Natural persons have a 16-character tax code.
      type: string
      pattern: "^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$"
      example: RSSMRO99A04H501A
    TaxCode:
      description: >-
        This is a purely syntactic definition, and can
        be used in different semantic contexts.
      oneOf:
        - $ref: "#/components/schemas/NumericTaxCode"
        - $ref: "#/components/schemas/StringTaxCode"
~~~
{: title="A definitions.yaml with reusable components." #ex-definitions }

~~~ yaml
openapi: 3.0.0
...
components:
  schemas:
    Person:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
      type: object
      properties:
        tax_code:
          $ref: "https://example.com/definitions.yaml#/components/schemas/TaxCode"
        ...
    ResidentPerson:
      x-jsonld-type: RPO:RegisteredResidentPerson
      x-jsonld-context:
        RPO: https://w3id.org/italia/onto/RPO/
        tax_code: '@id'
        '@base': 'urn:example:tax:it:'
      type: object
      properties:
        tax_code:
          $ref: "https://example.com/definitions.yaml#/components/schemas/TaxCode"
        ...

~~~
{: title="A schema using an external component." #ex-bundled-schema-definitions }

Bundling is the process of combining multiple OpenAPI and JSON schema documents in a single document
in order to distribute a consolidated service specification in a single file.
Bundling ensures that all necessary schema components are contained within a single file,
and avoids the need to resolve external references.

Bundling resolves all remote references,
adds them to the schema,
and replaces the associated `$ref` with a local reference.

~~~ yaml
openapi: 3.0.0
...
components:
  schemas:
    Person:
      x-jsonld-type: Person
      x-jsonld-context:
        "@vocab": "https://schema.org/"
      type: object
      properties:
        tax_code:
          $ref: "#/components/schemas/TaxCode"
        ...
    ResidentPerson:
      x-jsonld-type: RPO:RegisteredResidentPerson
      x-jsonld-context:
        RPO: https://w3id.org/italia/onto/RPO/
        tax_code: '@id'
        '@base': 'urn:example:tax:it:'
      type: object
      required:
        - tax_code
      properties:
        tax_code:
          $ref: '#/components/schemas/TaxCode'
        ...
    #
    # The bundler adds the following components to the schema.
    #
    NumericTaxCode:
      description: Legal persons have a 11-digit tax code.
      type: string
      pattern: ^[0-9]{11}$
      example: '12345678901'
    StringTaxCode:
      description: Natural persons have a 16-character tax code.
      type: string
      pattern: ^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$
      example: RSSMRO99A04H501A
    TaxCode:
      description: This is a purely syntactic definition, and can be used in different semantic contexts.
      oneOf:
        - $ref: '#/components/schemas/NumericTaxCode'
        - $ref: '#/components/schemas/StringTaxCode'
~~~
{: title="A bundled schema." #ex-bundled-schema}

Bundling can be done in different ways.
{{ex-bundling-tools}} contains a list of bundling tools.

# Interoperability Considerations {#int}

## JSON Schema property names {#int-property-names}

To minimize context information, a common practice is to name
JSON Schema properties after the corresponding RDF predicates.

~~~ yaml
Place:
  x-jsonld-type: Place
  ...
Occupation:
  x-jsonld-type: Occupation
  ...
Person:
  x-jsonld-type: Person
  x-jsonld-context:
    "@vocab": "https://schema.org/"
  type: object
  properties:
    familyName:
      type: string
    givenName:
      type: string
    birthPlace:
      $ref: "#/Place"
    hasOccupation:
      $ref: "#/Occupation"
~~~
{: title="A JSON Schema with properties named after RDF predicates." #ex-rdf-predicates}

As we can see from the above schema,
this practice can lead to inheriting
non uniform naming conventions from the RDF vocabulary:
for example, `birthPlace` and `hasOccupation` both target objects,
while only `hasOccupation` starts with a verb (i.e. `has`).

Another issue is related to the schema instance size
when using very long property or class names such as
https://schema.org/isAccessibleForFree
and
https://schema.org/IPTCDigitalSourceEnumeration.

Mapping JSON Schema properties to RDF predicates in x-jsonld-context
can reduce semantic risks when an ontology changes,
or when there's
a need to switch to a different ontology:
this is because having different names for the property and the predicate
clarifies that the property may well evolve into a different predicate
in time, like shown in the following example.

Instead of using a generic `surname`, this schema uses
the more specific `patronymicName` named after the corresponding RDF predicate.

~~~ yaml
Person:
  x-jsonld-context:
    "@vocab": "http://w3.org/ns/person#"
  properties:
    patronymicName:
      type: string
  example:
    patronymicName: "Ericsson"
  x-rdf: >-
    _:b0 :patronymicName "Ericsson" .
~~~
{: title="Drawbacks of using RDF property names as JSON Schema properties." #ex-inheriting-property-names}

If the service evolves to be more generic (e.g., moving to `foaf:`),
the property name might be mapped
to the `foaf:familyName` predicate, but the schema instance will remain the same
thus retaining the information of a legacy ontology.

A more flexible design would have considered using a generic `surname` property name,
and either map it to `http://w3.org/ns/person#patronymicName` or `foaf:familyName` in the context.

## Composability {#int-composability}

Always prefer explicit context information  over implicit context composition.
Different implementations of context composition may lead to different results,
especially over large schemas with many nested objects.

While composition is useful in the schema design phase,
bundling and validating the composed context in the final
schema definition reduces the risk of interoperability issues.


# Security Considerations {#sec}



## Integrity and Authenticity {#sec-integrity}



## Conflicts {#sec-conflicts}



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

## Bundling tools {#ex-bundling-tools}

The following is a list of some bundling tools:

- https://redocly.com/docs/cli;
- https://www.npmjs.com/package/swagger-cli.

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



# Change Log
{: numbered="false" removeinrfc="true"}

TBD
