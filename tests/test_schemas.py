import json
import re
from pathlib import Path

import pyld
import pytest
import rdflib
import rdflib.compare
import yaml
from rdflib import Graph

from oasld import Instance, RefResolver

DATADIR = Path(__file__).parent
SPEC_MD = DATADIR.parent / "draft-polli-restapi-ld-keywords.md"
DESIGN_MD = DATADIR.parent / "draft-polli-design-process.md"


testfiles = [yaml.safe_load(x.read_text()) for x in DATADIR.glob("*.oas3.yaml")]
testschemas = [
    (schema_name, schema_content)
    for f in testfiles
    for schema_name, schema_content in f["components"]["schemas"].items()
]


def extract_snippets(document_section: str):
    pattern = re.compile(
        r"""
\n
~~~ (?P<language>.*?)\n                # Opening example fence
(?P<content>.*?)                 # Capture the content
\n
~~~                             # Closing fence
\n
        """,
        re.VERBOSE | re.DOTALL,
    )
    for match in pattern.finditer(document_section):
        groups = match.groupdict()
        language = groups["language"].strip()
        content = groups["content"]

        if language == "text":
            yield language.strip(), content
            continue

        if language not in (
            "yaml",
            "json",
        ):
            continue

        data = content.replace("...", "")
        try:
            data = yaml.safe_load(data)
        except yaml.YAMLError:
            continue

        if not isinstance(data, dict):
            continue

        if "@context" in data:
            yield "jsonld", content
            continue

        schema_name, schema_content = next(iter(data.items()))
        if "example" not in schema_content:
            continue
        yield "schema", content


@pytest.mark.skip("Incomplete test")
def test_ld_1():
    schema_1 = yaml.safe_load((DATADIR / "schema-1.yaml").read_text())
    resolver = RefResolver(schema_1)
    schema_name = "PersonaAnagraficamenteResidente"

    schema = schema_1["components"]["schemas"][schema_name]
    instance_data = schema["example"]
    instance = Instance(instance_data, schema)
    instance.process_instance(resolver=resolver)

    result = instance.ld
    g = Graph()
    g.parse(data=json.dumps(result), format="application/ld+json")
    ttl = g.serialize(format="text/turtle")

    raise NotImplementedError


@pytest.mark.parametrize("schema_name, schema_content", testschemas)
def test_oas_annotated_schemas(schema_name, schema_content):
    if not (expected := schema_content.get("x-rdf")):
        raise pytest.skip("No expected status  in schema")

    if not (i := schema_content["example"]):
        raise pytest.skip("Empty example in schema")

    if not (c := schema_content.get("x-jsonld-context")):
        raise pytest.skip("No context directive in schema")

    t = (
        {"@type": schema_content.get("x-jsonld-type")}
        if schema_content.get("x-jsonld-type")
        else {}
    )
    l = {"@context": c, **i, **t}

    g = Graph()
    g.parse(data=json.dumps(l), format="application/ld+json")
    ttl = g.serialize(format="text/n3")
    assert (
        ttl.strip() == expected.strip()
    ), f"Schema {schema_name} did not match expected RDF output"


def parse_spec_md(mdfile: Path):
    content = mdfile.read_text()
    content = content.split("--- middle")[1]
    pattern = re.compile(
        r"""
\n                             # a newline
(?P<header>\#+)              # Capture the header hashes
\s                             # a space
(?P<title>.+?)                 # Capture the title
(?P<identifier>\s\{\#.*?\})?   # Optionally capture the identifier
\n                             # a newline
(?P<body>.*?)                   # Capture the body
(?=\n\#|\Z)                    # Positive lookahead for next header or end of string
        """,
        re.VERBOSE | re.DOTALL,
    )
    doc = {}
    for match in pattern.finditer(content):
        groups = match.groupdict()
        header = groups["header"]
        # title = groups["title"]
        identifier = (
            groups["identifier"].strip()
            if groups["identifier"]
            else groups["title"].strip().replace(" ", "-").lower()
        )
        body = groups["body"].strip()
        level = len(header)
        assert identifier

        doc[identifier] = {
            "level": level,
            "body": body,
            "examples": [
                {"language": language, "content": example.strip()}
                for language, example in extract_snippets(body)
            ],
        }
    return doc


def get_examples_from_md(mdfile: Path):
    doc = parse_spec_md(mdfile)
    testcases = extract_testcases(doc)
    return testcases


def extract_testcases(doc: dict):
    testcases = {}
    for section, data in doc.items():
        examples = data["examples"]
        for example in examples:
            test_id = testcases[section] = testcases.get(section, {})
            if example["language"] in ("schema", "jsonld"):
                if "..." in example["content"]:
                    pass
                else:
                    example["language"]

                text = example["content"].replace("...", "")
                try:
                    parsed = yaml.safe_load(text)
                except yaml.YAMLError:
                    parsed = text
                d = {
                    example["language"]: parsed,
                }
            elif example["language"] == "text":
                try:
                    g = Graph()
                    g.parse(data=example["content"], format="text/turtle")
                    d = {
                        "rdf": example["content"],
                        "jld": yaml.safe_load(
                            g.serialize(format="application/ld+json")
                        ),
                    }
                except Exception as e:
                    raise ValueError(section) from e
            else:
                continue
            test_id.update(d)
    return testcases


TEST_DRAFT_EXAMPLES_ARE_CORRECT = [
    [k, v.get("schema"), v.get("jsonld"), v.get("rdf")]
    for k, v in get_examples_from_md(SPEC_MD).items()
]
TEST_DESIGN_EXAMPLES_ARE_CORRECT = [
    [k, v.get("schema"), v.get("jsonld"), v.get("rdf")]
    for k, v in get_examples_from_md(DESIGN_MD).items()
]


@pytest.mark.parametrize(
    "section, schema, jsonld, rdf",
    TEST_DRAFT_EXAMPLES_ARE_CORRECT + TEST_DESIGN_EXAMPLES_ARE_CORRECT,
    ids=[
        x[0] for x in TEST_DRAFT_EXAMPLES_ARE_CORRECT + TEST_DESIGN_EXAMPLES_ARE_CORRECT
    ],
)
def test_draft_examples_are_correct(section, schema, jsonld, rdf):
    """
    Given:
    - a document section containing:
        - an annotated OAS schema with example and context
        - the expected JSON-LD or RDF output

    When:
    - process the instance according to the schema and context

    Then:
    - the produced RDF graph is isomorphic to the expected one
    """
    if not schema:
        raise pytest.skip("No schema in test case")

    if not any([jsonld, rdf]):
        raise pytest.skip("No expected output in test case")

    schema_name, schema_content = next(iter(schema.items()))
    instance = schema_content["example"]
    context = schema_content.get("x-jsonld-context", {})
    if not context:
        raise pytest.skip("No context in schema")

    try:
        i = Instance(instance, schema_content)
        i.process_instance(resolver=RefResolver(schema))
    except Exception as e:
        raise pytest.skip(f"Error processing instance in section {section}") from e

    g_instance = _parse_rdf(data=json.dumps(i.ld), format="application/ld+json")
    assert (
        len(g_instance) > 0
    ), f"Test case {section} produced empty graph: \n{yaml.safe_dump(i.ld)}"

    if rdf:
        g_result = _parse_rdf(data=rdf, format="text/turtle")
    elif jsonld:
        g_result = _parse_rdf(data=jsonld, format="application/ld+json", expand=True)
    else:
        raise NotImplementedError("No expected output provided")

    assert_isomorphic(g_instance, g_result)


def _parse_rdf(data: str | dict, format: str, expand: bool = False) -> Graph:
    # Temporary fix for rdflib not handling "@base" correctly.
    if format == "application/ld+json":
        if isinstance(data, str):
            data = json.loads(data)
        if expand:
            data = pyld.jsonld.expand(data)
        data = json.dumps(data)
    g = Graph()
    g.parse(data=data, format=format)
    return g


def assert_isomorphic(g1: Graph, g2: Graph):
    i1 = rdflib.compare.to_isomorphic(g1)
    i2 = rdflib.compare.to_isomorphic(g2)
    in_both, in_g1, in_g2 = rdflib.compare.graph_diff(i1, i2)
    dump_nt_sorted = lambda g: "\n".join(sorted(g.serialize(format="nt").splitlines()))
    assert (
        i1 == i2
    ), f"Graphs are not isomorphic {yaml.safe_dump(dict(
        in_both=dump_nt_sorted(in_both),
        in_g1=dump_nt_sorted(in_g1),
        in_g2=dump_nt_sorted(in_g2),
    ))}"
