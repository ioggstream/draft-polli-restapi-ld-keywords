# REST API LD Keywords JSONSchema Vocabularies

This directory contains JSON-LD vocabularies and dialects for use with JSON Schema validation in REST APIs.
The vocabularies define custom keywords and their semantics, while the dialects specify how these keywords should be interpreted during validation.

Contributing:

- the source files are in YAML format for easier editing and review.
- they are automatically converted to JSON format for use in validation.

## JSON-LD Vocabulary

The JSON-LD vocabularies are used to define custom keywords and their semantics.

## JSON-LD Table Schema Extension

This extension adds JSON-LD capabilities to the Table Schema vocabulary, allowing for richer metadata representation in tabular data based on REST API LD Keywords.

Current version relies on the `x-` prefix for compatibility with
OpenAPI Specification 3.0.

Future versions may switch to an unprefixed approach, that is instead
allowed in JSON Schema 2020-12 and OpenAPI Specification 3.1.

```text
# From https://raw.githubusercontent.com/frictionlessdata/datapackage/refs/heads/main/content/docs/extensions/fiscal-data-package.md
---
title: Semantic Data Package
---

<table>
  <tr>
    <th>Authors</th>
    <td>Roberto Polli</td>
  </tr>
</table>

Semantic Data Package is a lightweight and user-oriented format for publishing and consuming semantic data.
Semantic data packages are made of simple and universal components.

[Semantic Data Package](https://github.com/ioggstream/draft-polli-restapi-ld-keywords)
```
