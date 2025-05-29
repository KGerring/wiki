"""Converts simple YAML to SKOS"""
import argparse
import os
import sys
import skosify
import rdflib
import rfc3987
import yaml

DEFAULT_LANGUAGE = "en"

SKOS = rdflib.namespace.SKOS
DCT = rdflib.namespace.DCTERMS
RDF = rdflib.namespace.RDF

SKOS_LITERALS = {
    "l": SKOS.prefLabel,
    "alt": SKOS.altLabel,
    "hidden": SKOS.hiddenLabel,
    "def": SKOS.definition,
    "note": SKOS.note,
    "scope": SKOS.scopeNote,
    "example": SKOS.example,
    "history": SKOS.historyNote,
    "editorial": SKOS.editorialNote,
    "change": SKOS.changeNote,
    "notation": SKOS.notation,
}

SKOS_RELATIONS = [
    "broader",
    "narrower",
    "related",
    "exactMatch",
    "closeMatch",
    "broadMatch",
    "narrowMatch",
    "relatedMatch",
]


def check_overwrite(filepath, overwrite=False):
    """asks the user if a given file should be overwritten. Always True if overwrite is set to True."""
    if overwrite:
        return True
    inp = ""
    while inp not in ("y", "n"):
        inp = eval(input(f"'{filepath}' already exists. Overwrite? (y/n) "))
    if inp == "y":
        return True
    return False


def is_namespaced(string):
    """Checks if a string is a namespaced reference or a literal. Kinda wonky."""
    if ":" in string:
        ind = string.index(":")
        if ind and string[ind - 1] != "\\" and not " " in string[:ind]:
            return True
    return False


def split_namespace(raw):
    """Reads a reference and returns the namespace and concept separatly."""
    namespace = "_default"
    concept = raw
    if is_namespaced(raw):
        new_namespace, new_concept = raw.split(":", 1)
        if not " " in new_namespace:
            namespace, concept = new_namespace, new_concept
    return namespace, concept


def add_literal(skos_graph, subject, predicate, literal_info):
    """Adds a literal to the skos graph, with the respective language."""
    lang = DEFAULT_LANGUAGE
    literal = literal_info
    if "@" in literal_info:
        literal, lang = literal_info.rsplit("@", 1)
    if "\\:" in literal:
        literal = literal.replace("\\:", ":")
    skos_graph.add((subject, predicate, rdflib.Literal(literal, lang=lang)))


def add_relation(skos_graph, subject, predicate, object_info, namespace_info):
    """Adds a single relation to the skos graph."""
    namespace, concept = split_namespace(object_info)
    skos_graph.add((subject, predicate, namespace_info[namespace][concept]))


def add_relations(skos_graph, this, detail, relation_type, tax_ns, concept_scheme):
    """Adds relations to other concepts, that may be either references or inline definitions."""
    if isinstance(detail[relation_type], str):
        add_relation(
            skos_graph, this, SKOS[relation_type], detail[relation_type], tax_ns
        )
    else:
        for concept in detail[relation_type]:
            if isinstance(concept, str):
                add_relation(skos_graph, this, SKOS[relation_type], concept, tax_ns)
            elif isinstance(concept, dict):
                skos_graph.add(
                    (
                        this,
                        SKOS[relation_type],
                        eval_concept(
                            *list(concept.items())[0],
                            skos_graph,
                            tax_ns,
                            concept_scheme,
                        ),
                    )
                )


def eval_concept(concept, value, skos_graph, tax_ns, concept_scheme):
    """Reads the definition of a concept and adds it to the graph."""
    namespace, concept = split_namespace(concept)
    this = tax_ns[namespace][concept]
    skos_graph.add((this, RDF.type, SKOS.Concept))
    skos_graph.add((this, SKOS.inScheme, concept_scheme))
    if value is None:
        return this
    if isinstance(value, str):
        skos_graph.add((this, SKOS.prefLabel, rdflib.Literal(value, lang="en")))
        return this
    if not isinstance(value, list):
        print(f"Warning: unexpected content for concept '{concept}'")
        return this
    for detail in value:
        for key in detail:
            if key in SKOS_LITERALS:
                add_literal(skos_graph, this, SKOS_LITERALS[key], detail[key])
            elif key in SKOS_RELATIONS:
                add_relations(skos_graph, this, detail, key, tax_ns, concept_scheme)
            elif is_namespaced(key):
                key_ns, key_elem = split_namespace(key)
                if is_namespaced(detail[key]):
                    value_ns, value_elem = split_namespace(detail_key)
                    skos_graph.add(
                        (this, tax_ns[key_ns][key_elem], tax_ns[value_ns][value_elem])
                    )
                else:
                    add_literal(skos_graph, this, tax_ns[key_ns][key_elem], detail[key])
            else:
                print(f"Warning: unexpected detail '{key}' with value '{detail[key]}'")
    #        if "l" in detail:
    #            add_literal(skos_graph, this, SKOS.prefLabel, detail["l"])
    #        if "def" in detail:
    #            add_literal(skos_graph, this, SKOS.definition, detail["def"])
    #        if "alt" in detail:
    #            add_literal(skos_graph, this, SKOS.altLabel, detail["alt"])
    #        if "narrower" in detail:
    #            add_relations(skos_graph, this, detail, "narrower", tax_ns, concept_scheme)
    #        if "broader" in detail:
    #            add_relations(skos_graph, this, detail, "broader", tax_ns, concept_scheme)
    #        if "related" in detail:
    #            add_relations(skos_graph, this, detail, "related", tax_ns, concept_scheme)
    return this


def load_namespaces(doc):
    """populates a dictionary with the namespaces defined in the document's 'namespaces' section."""
    tax_ns = {"_default": rdflib.Namespace(doc["meta"]["uri"])}
    for namespace, uri in list(doc["meta"].get("namespaces", {}).items()):
        if namespace == "_default":
            print("Warning: '_default' is used internally, skipped")
            continue
        tax_ns[namespace] = rdflib.Namespace(uri)
    return tax_ns


def parse_dcterms(doc, skos_graph, tax_ns, concept_scheme):
    """Loads all dcterms meta-data from the document and adds it to skos graph."""
    if "title" in doc["meta"]:
        add_literal(skos_graph, concept_scheme, DCT.title, doc["meta"]["title"])

    for thing in doc["meta"]["dcterms"]:
        if len(thing) != 1:
            print(
                "Warning: every list entry in meta.dcterms must contain exactly 1 key with 1 "
                "value, skipped"
            )
            continue
        for key, value in list(thing.items()):
            is_iri = False
            try:
                iri = rfc3987.parse(value, rule="IRI")
                if iri:
                    is_iri = True
            except ValueError:
                pass
            if is_iri:
                skos_graph.add((concept_scheme, DCT[key], rdflib.URIRef(value)))
                continue
            if is_namespaced(value):
                add_relation(skos_graph, concept_scheme, DCT[key], value, tax_ns)
                continue
            add_literal(skos_graph, concept_scheme, DCT[key], value)


def parse_collections(doc, skos_graph, tax_ns):
    """loads all (unordered) collections from the document and adds them to skos graph"""
    for collection, value in list(doc.get("collections", {}).items()):
        namespace, collection = split_namespace(collection)
        this = tax_ns[namespace][collection]
        skos_graph.add((this, RDF.type, SKOS.Collection))
        for detail in value:
            if isinstance(detail, dict) and "l" in detail:
                add_literal(skos_graph, this, SKOS.prefLabel, detail["l"])
                continue
            if "member" in detail:
                add_relation(skos_graph, this, SKOS.member, detail["member"], tax_ns)


def parse_ordered_collections(doc, 
skos_graph:rdflib.Graph, 
tax_ns:dict):
    """loads all ordered collections from the document and adds them to skos graph"""
    for collection, value in list(doc.get("ordered-collections", {}).items()):
        namespace, collection = split_namespace(collection)
        this = tax_ns[namespace][collection]
        skos_graph.add((this, RDF.type, SKOS.OrderedCollection))
        members = []
        for detail in value:
            if isinstance(detail, dict) and "l" in detail:
                add_literal(skos_graph, this, SKOS.prefLabel, detail["l"])
                continue
            members.append(detail)
        nodes = [rdflib.BNode() for member in members]
        for index, (member, node) in enumerate(zip(members, nodes)):
            namespace, member = split_namespace(member)
            skos_graph.add((node, RDF.first, tax_ns[namespace][member]))
            if not index:
                skos_graph.add((this, SKOS.memberList, node))
            if index < len(members) - 1:
                skos_graph.add((node, RDF.rest, nodes[index + 1]))


def convert_to_skos(doc, default_language="en"):
    """Converts a dictionary with the correct structure to a SKOS graph"""

    global DEFAULT_LANGUAGE
    DEFAULT_LANGUAGE = default_language

    if (
        "meta" not in doc
        or "id" not in doc["meta"]
        or "uri" not in doc["meta"]
        or "concepts" not in doc
    ):
        raise ValueError("Error, missing required information!")

    skos_graph = rdflib.Graph()

    skos_graph.bind("skos", SKOS)
    tax_ns = load_namespaces(doc)

    concept_scheme = tax_ns["_default"][doc["meta"]["id"]]
    skos_graph.add((concept_scheme, RDF.type, SKOS.ConceptScheme))

    if "dcterms" in doc["meta"] or "title" in doc["meta"]:
        parse_dcterms(doc, skos_graph, tax_ns, concept_scheme)

    for concept, value in list(doc["concepts"].items()):
        eval_concept(concept, value, skos_graph, tax_ns, concept_scheme)

    if "collections" in doc:
        parse_collections(doc, skos_graph, tax_ns)

    if "ordered-collections" in doc:
        parse_ordered_collections(doc, skos_graph, tax_ns)

    voc = skosify.skosify(skos_graph)
    return voc


def argparser():
    """Builds the argparse parser and reads the command line parameters."""
    parser = argparse.ArgumentParser(description="converts simple YAML to SKOS")
    parser.add_argument("in_file", metavar="SOURCE", type=str, help="YAML file to read")
    parser.add_argument(
        "out_file", metavar="OUTPUT", type=str, help="SKOS file to write"
    )
    parser.add_argument(
        "--overwrite",
        dest="overwrite_existing",
        action="store_true",
        help="If this is set, then any existing output file that already exists "
        "will be overwritten without the manual check.",
    )
    parser.add_argument(
        "--lang",
        dest="default_language",
        type=str,
        default="en",
        help="default language to use for RDF Literals, defaults to 'en'",
    )
    parser.add_argument(
        "-f",
        dest="output_format",
        default="xml",
        help="Output format. Defaults to 'xml'. Can be any format that rdflib can "
        "serialize to.",
    )
    return parser.parse_args()


def main():
    """For commandline usage only. Use --help for usage information."""

    args = argparser()

    if os.path.exists(args.out_file):
        if not check_overwrite(args.out_file, args.overwrite_existing):
            print("Not overwritten")
            sys.exit(0)
        print(f"Overwriting {args.out_file}...")

    doc = {}
    with open(args.in_file) as yaml_file:
        doc = yaml.safe_load(yaml_file.read())

    try:
        voc = convert_to_skos(doc, args.default_language)
    except ValueError:
        print(
            "Error: The document must contain both a 'meta' and a 'concepts' section! "
            "The 'meta' section must also contain an 'id' and an 'uri' key!"
        )
        sys.exit(1)

    with open(args.out_file, "w+") as out_file:
        out_file.write(voc.serialize(format=args.output_format))
    print("Done")

__all__ = sorted(
    [
        getattr(v, "__name__", k)
        for k, v in list(globals().items())  # export
        if (
            (
                callable(v)
                and getattr(v, "__module__", "")
                == __name__  # callables from this module
                or k.isupper()
            )
            and not str(getattr(v, "__name__", k)).startswith("__")  # or CONSTANTS
        )
    ]
)  # neither marked internal


if __name__ == "__main__":
    main()


