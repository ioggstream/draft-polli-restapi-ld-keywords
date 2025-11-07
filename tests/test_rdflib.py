import json

import pytest
from rdflib import Graph


@pytest.mark.skip("Bug in rdflib")
def test_mailto_scheme_should_work_jsonld():
    l = {
        "@context": {
            "@vocab": "https://schema.org/",
            "email": "@id",
            "@base": "mailto:",
        },
        "@type": "https://schema.org/Person",
        "familyName": "Doe",
        "email": "a@b.c",
    }
    g = Graph()
    g.parse(data=json.dumps(l), format="application/ld+json")
    assert list(g)
    ttl = g.serialize(format="text/turtle")
    assert ttl.strip()


@pytest.mark.skip("Bug in rdflib")
def test_mailto_scheme_should_work_n3():
    ttl = """
@prefix schema: <https://schema.org/> .
@base <mailto:> .

<a@b.c> a schema:Person ;
    schema:familyName "Doe" .
"""
    g = Graph()
    g.parse(data=ttl, format="text/turtle")
    assert list(g)
    jsonld = g.serialize(format="application/ld+json")
    assert jsonld.strip()
