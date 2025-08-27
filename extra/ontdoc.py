#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename = namespaces
from __future__ import annotations

import logging
import pickle
import re
import shutil
from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, cast

import dominate
import markdown
from dominate.tags import (
    a,
    br,
    code,
    dd,
    div,
    dl,
    dt,
    em,
    h1,
    h2,
    h3,
    h4,
    li,
    link,
    meta,
    p,
    pre,
    script,
    span,
    strong,
    style,
    sup,
    table,
    td,
    th,
    tr,
    ul
)
from dominate.util import raw
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import (
    DC,
    DCTERMS,
    FOAF,
    ORG,
    OWL,
    PROF,
    PROV,
    RDF,
    RDFS,
    SDO,
    SKOS,
    VANN
)
from rdflib.paths import ZeroOrMore



ONTDOC = Namespace("https://w3id.org/profile/ontdoc/")
# metadata properties for OWL Ontology instances
ONT_PROPS = [
		DCTERMS.title,
		DCTERMS.publisher,
		DCTERMS.creator,
		DCTERMS.contributor,
		DCTERMS.created,
		DCTERMS.modified,
		DCTERMS.issued,
		DCTERMS.license,
		DCTERMS.rights,
		OWL.versionIRI,
		OWL.versionInfo,
		OWL.priorVersion,
		VANN.preferredNamespacePrefix,
		VANN.preferredNamespaceUri,
		SKOS.scopeNote,
		DCTERMS.source,
		DCTERMS.provenance,
		SKOS.note,
		DCTERMS.description,
		ONTDOC.restriction,
]

# properties for OWL Class instances
CLASS_PROPS = [
		RDFS.isDefinedBy,
		DCTERMS.title,
		DCTERMS.description,
		SKOS.scopeNote,
		SKOS.example,
		DCTERMS.source,
		DCTERMS.provenance,
		SKOS.note,
		RDFS.subClassOf,
		OWL.equivalentClass,
		# OWL.restriction,
		ONTDOC.inDomainOf,
		ONTDOC.inDomainIncludesOf,
		ONTDOC.inRangeOf,
		ONTDOC.inRangeIncludesOf,
		ONTDOC.restriction,
		ONTDOC.hasInstance,
		ONTDOC.superClassOf,
]

# properties for instances of RDF Property and OWL specialised
# forms, such as ObjectProperty etc.
PROP_PROPS = [
		RDFS.isDefinedBy,
		DCTERMS.title,
		DCTERMS.description,
		SKOS.scopeNote,
		SKOS.example,
		DCTERMS.source,
		DCTERMS.provenance,
		SKOS.note,
		RDFS.subPropertyOf,
		ONTDOC.superPropertyOf,
		RDFS.domain,
		SDO.domainIncludes,
		RDFS.range,
		SDO.rangeIncludes,
]

# properties for Agents
AGENT_PROPS = [
		SDO.name,
		SDO.affiliation,
		SDO.identifier,
		SDO.email,
		SDO.honorificPrefix,
		SDO.url,
]

# properties for OWL restriction instances
RESTRICTION_PROPS = [
		OWL.allValuesFrom,
		OWL.someValuesFrom,
		OWL.hasValue,
		OWL.onProperty,
		OWL.onClass,
		OWL.cardinality,
		OWL.qualifiedCardinality,
		OWL.minCardinality,
		OWL.minQualifiedCardinality,
		OWL.maxCardinality,
		OWL.maxQualifiedCardinality,
]

# all known properties
PROPS = set(
		ONT_PROPS + CLASS_PROPS + PROP_PROPS +
		AGENT_PROPS + RESTRICTION_PROPS)

ONT_TYPES = {
		OWL.Class: ("c", "OWL/RDFS Class"),
		RDF.Property: ("p", "RDF Property"),
		OWL.ObjectProperty: ("op", "OWL Object Property"),
		OWL.DatatypeProperty: ("dp", "OWL Datatype Property"),
		OWL.AnnotationProperty: ("ap", "OWL Annotation Property"),
		OWL.FunctionalProperty: ("fp", "OWL Functional Property"),
		OWL.InverseFunctionalProperty: ("ifp", "OWL Inverse Functional Property"),
		OWL.NamedIndividual: ("ni", "OWL Named Individual"),
}

RESTRICTION_TYPES = [
		OWL.cardinality,
		OWL.qualifiedCardinality,
		OWL.minCardinality,
		OWL.minQualifiedCardinality,
		OWL.maxCardinality,
		OWL.maxQualifiedCardinality,
		OWL.allValuesFrom,
		OWL.someValuesFrom,
		OWL.hasValue,
]

OWL_SET_TYPES = [OWL.unionOf, OWL.intersectionOf]


RDF_FOLDER = Path(__file__).parent / "rdf"



def check_all_props_are_known():
	"""Check all properties listed in the combined property lists in
	properties.py to see if their titles and descriptions are present in the
	background ontologies in the folder rdf/. Run after performing labelling
	inferencing."""
	bg = load_background_onts()
	for prop in PROPS:
		if (prop, RDF.type, None) not in bg:
			print(f"Unknown property: {prop}")
			print(f'Estimating title as "{make_title_from_iri(prop)}"')
			print()


def get_ns(ont: Graph) -> Tuple[str, str]:
	"""Gets the default Namespace for the given graph (ontology)"""
	# if this ontology declares a preferred URI, use that
	pref_iri = None
	for s_, o in ont.subject_objects(predicate=VANN.preferredNamespaceUri):
		pref_iri = str(o)
	
	pref_prefix = None
	for s_, o in ont.subject_objects(predicate=VANN.preferredNamespacePrefix):
		pref_prefix = str(o)
	if pref_prefix is None:
		pref_prefix = ""
	
	if pref_iri is not None:
		return pref_prefix, pref_iri
	
	# if not, try the URI of the main object, compared to all prefixes
	else:
		default_iri = None
		
		for s_ in chain(
				ont.subjects(predicate=RDF.type, object=OWL.Ontology),
				ont.subjects(predicate=RDF.type, object=SKOS.ConceptScheme),
				ont.subjects(predicate=RDF.type, object=PROF.Profile),
		):
			default_iri = str(s_)
		
		if default_iri is not None:
			prefix = ont.compute_qname(default_iri, True)[0]
			if prefix is not None:
				return prefix, default_iri
		else:
			# can't find either a declared or default namespace
			# so we have an error
			raise Exception(
					"pyLODE can't detect a URI for an owl:Ontology, "
					"a skos:ConceptScheme or a prof:Profile"
			)


def make_title_from_iri(iri: URIRef):
	"""Makes a human-readable title for an RDF resource from its IRI"""
	if isinstance(iri, URIRef):
		iri = str(iri)
	# can't tolerate any URI faults so return None if anything is wrong
	
	# URIs with no path segments or ending in slash
	segments = iri.split("/")
	if len(segments[-1]) < 1:
		return None
	
	# URIs with only a domain - no path segments
	if len(segments) < 4:
		return None
	
	# URIs ending in hash
	if segments[-1].endswith("#"):
		return None
	
	id_part = (
			segments[-1].split("#")[-1]
			if segments[-1].split("#")[-1] != ""
			else segments[-1].split("#")[-2]
	)
	
	# split CamelCase
	# title case if the first char is upercase (likely a Class)
	# else lower (property/Named Individual)
	words = re.split(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", id_part)
	if words[0][0].isupper():
		return " ".join(words).title()
	else:
		return " ".join(words).lower()


def generate_fid(title_: Union[Literal, None], iri: URIRef, fids: dict):
	"""Makes an HTML fragment ID for an RDF resource,
	based on title (preferred) or IRI"""
	s_iri = str(iri) if iri is not None else None
	s_title_ = str(title_) if title_ is not None else None
	
	# does this URI already have a fid?
	existing_fid = fids.get(s_iri)
	if existing_fid is not None:
		return existing_fid
	
	# if we get here, there is no fid, so make one
	def _remove_non_ascii_chars(s_):
		return "".join(j for j in s_ if ord(j) < 128).replace("&", "")
	
	# try creating an ID from label
	# remove spaces, escape all non-ASCII chars
	if s_title_ is not None:
		fid = _remove_non_ascii_chars(s_title_.replace(" ", ""))
		
		# if this generated fid is not in use, add it to fids and return it
		if fid not in fids.values():
			fids[s_iri] = fid
			return fid
		
		# this fid is already present
		# so generate a new one from the URI instead
	
	# split URI for last slash segment
	segments = s_iri.split("/")
	
	# return None for empty string - URI ends in slash
	if len(segments[-1]) < 1:
		return None
	
	# return None for domains, i.e. ['http:', '', '{domain}'],
	# no path segments
	if len(segments) < 4:
		return None
	
	# split out hash URIs
	# remove any training hashes
	if segments[-1].endswith("#"):
		return None
	
	fid = (
			segments[-1].split("#")[-1]
			if segments[-1].split("#")[-1] != ""
			else segments[-1].split("#")[-2]
	)
	
	# fid = fid.lower()
	
	# if this generated fid is not in use, add it to fids and return it
	if fid not in fids.values():
		fids[s_iri] = fid
		return fid
	else:
		# since it's in use but we've exhausted generation options,
		# just add 1 to existing fid name
		fids[s_iri] = fid + "1"
		return fid + "1"
		# yeah yeah, there could be more than one but unlikely


def back_onts_label_props(back_onts: Graph):
	"""Gets titles and descriptions for all properties
	in the background ontologies"""
	back_onts_titles = load_background_onts_titles(back_onts)
	
	def _get_prop_label(prop_iri: URIRef, back_onts: Graph) -> dict:
		title_ = None
		description = None
		ont_title = None
		for p_, o in back_onts.predicate_objects(prop_iri):
			if p_ == DCTERMS.title:
				title_ = o
			elif p_ == DCTERMS.description:
				description = o
		
		for k, v in back_onts_titles.items():
			if prop_iri.startswith(k):
				ont_title = v
		
		if title_ is None:
			title_ = make_title_from_iri(prop_iri)
		
		return {
				"title": title_,
				"description": description,
				"ont_title": ont_title,
		}
	
	pl = {}
	for prop in PROPS:
		pl[prop] = _get_prop_label(prop, back_onts)
	return pl


def load_ontology(ontology: Union[Graph, Path, str]) -> Graph:
	"""Loads and ontology into an RDFLib Graph.

	Can handle string data, file path, URL or Graph input"""
	try:
		# try URL
		if isinstance(ontology, str) and ontology.startswith("http"):
			return Graph().parse(location=ontology)
		elif isinstance(ontology, str):
			# see if it's a file path
			if Path(ontology).is_file():
				return Graph().parse(ontology)
			else:  # it's data
				if ontology.startswith("[") or ontology.startswith("{"):
					input_format = "json-ld"
				elif (
						ontology.startswith("<?xml")
						or ontology.startswith("<!--")
						or ontology.startswith("<rdf:RDF")
				):
					input_format = "xml"
				else:
					input_format = "turtle"  # this will also cover n-triples
				return Graph().parse(data=ontology, format=input_format)
		elif isinstance(ontology, Graph):
			return cast(ontology, Graph)
		elif isinstance(ontology, Path):
			return Graph().parse(ontology)
		else:
			raise ValueError(
					"The ontology you supply to OntDoc must be either "
					"an RDFlib Graph, a Path (to an RDF file) or a string "
					"(of RDF data)"
			)
	except Exception as e:
		print(f"{type(e).__name__} Error {e}")
		exit()


def load_background_onts():
	"""Loads background ontology files into an RDFLib graph from either
	RDF source files or a pickled Graph.

	Performs title and description inference and stores a pickle if
	generating from RDF source files."""
	
	def _parse_background_onts():
		g_ = Graph()
		for f_ in RDF_FOLDER.glob("*.ttl"):
			g_.parse(f_)
		
		return g_
	
	def _expand_background_onts_graph(back_ont: Graph):
		# make regular titles
		for s_, o in chain(
				back_ont.subject_objects(DC.title),
				back_ont.subject_objects(RDFS.label),
				back_ont.subject_objects(SKOS.prefLabel),
				back_ont.subject_objects(SDO.name),
		):
			back_ont.add((s_, DCTERMS.title, o))
		
		# make regular descriptions
		for s_, o in chain(
				back_ont.subject_objects(DC.description),
				back_ont.subject_objects(RDFS.comment),
				back_ont.subject_objects(SKOS.definition),
				back_ont.subject_objects(SDO.description),
		):
			back_ont.add((s_, DCTERMS.description, o))
	
	def _pickle_background_onts(back_ont: Graph):
		try:
			with open(RDF_FOLDER / "refs.pickle", "wb") as f_:
				pickle.dump(back_ont, f_)
		except FileNotFoundError:
			logging.warning("Could not cache background ontologies graph")
	
	if Path(RDF_FOLDER / "refs.pickle").is_file():
		logging.info("Loading background ontologies from a pickle file")
		with open(RDF_FOLDER / "refs.pickle", "rb") as f:
			return pickle.load(f)
	else:
		logging.info("Loading background ontologies from RDF files")
		g = _parse_background_onts()
		_expand_background_onts_graph(g)
		_pickle_background_onts(g)
		return g


def load_background_onts_titles(ont: Graph):
	"""Loads the titles of background ontologies
	into a dictionary of Ontology IRI / title"""
	
	def _get_background_ontology_titles(back_ont: Graph):
		onts_titles = {}
		for s_ in back_ont.subjects(predicate=RDF.type, object=OWL.Ontology):
			for o in back_ont.objects(subject=s_, predicate=DCTERMS.title):
				onts_titles[str(s_)] = str(o)
		
		return {
				k: v
				for k, v
				in sorted(
						onts_titles.items(),
						key=lambda item: item[1]
				)
		}
	
	def _pickle_background_onts_titles(ont_titles: dict):
		try:
			with open(RDF_FOLDER / "refs_titles.pickle", "wb") as f_:
				pickle.dump(ont_titles, f_)
		except FileNotFoundError:
			logging.warning(
					"Could not cache background ontologies' titles graph")
	
	if Path(RDF_FOLDER / "refs_titles.pickle").is_file():
		with open(RDF_FOLDER / "refs_titles.pickle", "rb") as f:
			return pickle.load(f)
	else:
		t = _get_background_ontology_titles(ont)
		_pickle_background_onts_titles(t)
		return t


def rdf_obj_html(
		ont: Graph,
		back_onts: Graph,
		ns: Tuple[str, str],
		obj: List[Union[URIRef, BNode, Literal]],
		fids,
		rdf_type=None,
		prop=None
):
	"""Makes a sensible HTML rendering of an RDF resource.

	Can handle IRIs, Blank Nodes of Agents or OWL Restrictions or Literals"""
	
	def _rdf_obj_single_html(
			ont_: Graph,
			back_onts_: Graph,
			ns_: Tuple[str, str],
			obj_: Union[URIRef, BNode, Literal],
			fids_,
			rdf_type_=None,
			prop=None
	):
		def _hyperlink_html(
				ont__: Graph,
				back_onts__: Graph,
				ns__: Tuple[str, str],
				iri__: URIRef,
				fids__,
				rdf_type__: Optional[URIRef] = None,
		):
			def _get_ont_type(ont___, back_onts___, iri___):
				types_we_know = [
						OWL.Class,
						OWL.ObjectProperty,
						OWL.DatatypeProperty,
						OWL.AnnotationProperty,
						OWL.FunctionalProperty,
						RDF.Property,
				]
				
				this_objects_types = []
				for o in ont___.objects(iri___, RDF.type):
					if o in ONT_TYPES.keys():
						this_objects_types.append(o)
				
				for x_ in types_we_know:
					if x_ in this_objects_types:
						return x_
				
				for o in back_onts___.objects(iri___, RDF.type):
					if o in ONT_TYPES.keys():
						this_objects_types.append(o)
				
				for x_ in types_we_know:
					if x_ in this_objects_types:
						return x_
			
			# find type
			if rdf_type__ is None:
				rdf_type__ = _get_ont_type(ont__, back_onts__, iri__)
			
			try:
				qname = ont__.compute_qname(iri__, True)
			except ValueError:
				qname = iri__
			
			prefix = "" if qname[0] == "" else f"{qname[0]}:"
			
			if ns__ is not None and str(iri__).startswith(ns__):
				fid = generate_fid(None, iri__, fids__)
				if fid is not None:
					iri__ = "#" + fid
			
			if rdf_type__ is not None:
				ret = span()
				ret.appendChild(a(f"{prefix}{qname[2]}", href=iri__))
				ret.appendChild(
						sup(
								ONT_TYPES[rdf_type__][0],
								_class="sup-" + ONT_TYPES[rdf_type__][0],
								title=ONT_TYPES[rdf_type__][1],
						)
				)
				return ret
			else:
				if isinstance(qname, tuple):
					return a(f"{prefix}{qname[2]}", href=iri__)
				return a(f"{qname}", href=iri__)
		
		def _literal_html(obj__):
			if str(obj__).startswith("http"):
				return _hyperlink_html(
						ont_, back_onts_, ns_, cast(URIRef, obj__), fids_
				)
			else:
				if prop == SKOS.example:
					return pre(str(obj__))
				else:
					return raw(markdown.markdown(str(obj__)))
		
		def _agent_html(ont__, obj__: Union[URIRef, BNode, Literal]):
			def _affiliation_html(ont___, obj___):
				name_ = None
				url_ = None
				
				for p_, o_ in ont___.predicate_objects(obj___):
					if p_ in AGENT_PROPS:
						if p_ == SDO.name:
							name_ = str(o_)
						elif p_ == SDO.url:
							url_ = str(o_)
				
				sp_ = span()
				if name_ is not None:
					if url_ is not None:
						sp_.appendChild(em(" of ", a(name_, href=url_)))
					else:
						sp_.appendChild(em(" of ", name_))
				else:
					if "http" in obj___:
						sp_.appendChild(em(" of ", a(obj___, href=obj___)))
				return sp_
			
			if isinstance(obj__, Literal):
				return span(str(obj__))
			honorific_prefix = None
			name = None
			identifier = None
			orcid = None
			orcid_logo = """
                    <svg width="15px" height="15px" viewBox="0 0 72 72" version="1.1"
                        xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink">
                        <title>Orcid logo</title>
                        <g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                            <g id="hero" transform="translate(-924.000000, -72.000000)" fill-rule="nonzero">
                                <g id="Group-4">
                                    <g id="vector_iD_icon" transform="translate(924.000000, 72.000000)">
                                        <path d="M72,36 C72,55.884375 55.884375,72 36,72 C16.115625,72 0,55.884375 0,36 C0,16.115625 16.115625,0 36,0 C55.884375,0 72,16.115625 72,36 Z" id="Path" fill="#A6CE39"></path>
                                        <g id="Group" transform="translate(18.868966, 12.910345)" fill="#FFFFFF">
                                            <polygon id="Path" points="5.03734929 39.1250878 0.695429861 39.1250878 0.695429861 9.14431787 5.03734929 9.14431787 5.03734929 22.6930505 5.03734929 39.1250878"></polygon>
                                            <path d="M11.409257,9.14431787 L23.1380784,9.14431787 C34.303014,9.14431787 39.2088191,17.0664074 39.2088191,24.1486995 C39.2088191,31.846843 33.1470485,39.1530811 23.1944669,39.1530811 L11.409257,39.1530811 L11.409257,9.14431787 Z M15.7511765,35.2620194 L22.6587756,35.2620194 C32.49858,35.2620194 34.7541226,27.8438084 34.7541226,24.1486995 C34.7541226,18.1301509 30.8915059,13.0353795 22.4332213,13.0353795 L15.7511765,13.0353795 L15.7511765,35.2620194 Z" id="Shape"></path>
                                            <path d="M5.71401206,2.90182329 C5.71401206,4.441452 4.44526937,5.72914146 2.86638958,5.72914146 C1.28750978,5.72914146 0.0187670918,4.441452 0.0187670918,2.90182329 C0.0187670918,1.33420133 1.28750978,0.0745051096 2.86638958,0.0745051096 C4.44526937,0.0745051096 5.71401206,1.36219458 5.71401206,2.90182329 Z" id="Path"></path>
                                        </g>
                                    </g>
                                </g>
                            </g>
                        </g>
                    </svg>"""
			url = None
			email = None
			affiliation = None
			
			for px, o in ont__.predicate_objects(obj__):
				if px in AGENT_PROPS:
					if px == SDO.name:
						name = str(o)
					elif px == SDO.honorificPrefix:
						honorific_prefix = str(o)
					elif px == SDO.identifier:
						identifier = str(o)
						if "orcid.org" in str(o):
							orcid = True
					elif px == SDO.url:
						url = str(o)
					elif px == SDO.email:
						email = str(o)
					elif px == SDO.affiliation:
						affiliation = o
			
			sp = span()
			
			if name is not None:
				if honorific_prefix is not None:
					name = honorific_prefix + " " + name
				
				if url is not None:
					sp.appendChild(a(name, href=url))
				else:
					sp.appendChild(span(name))
				
				if orcid:
					sp.appendChild(a(raw(orcid_logo), href=identifier))
				elif identifier is not None:
					sp.appendChild(a(identifier, href=identifier))
				
				if email is not None:
					email = email.replace("mailto:", "")
					sp.appendChild(
							span("(", a(email, href="mailto:" + email), ")"))
				
				if affiliation is not None:
					sp.appendChild(_affiliation_html(ont__, affiliation))
			return sp
		
		def _restriction_html(ont__, obj__, ns__):
			prop = None
			card = None
			cls = None
			
			for px, o in ont__.predicate_objects(obj__):
				if px != RDF.type:
					if px == OWL.onProperty:
						prop = _hyperlink_html(
								ont__,
								back_onts_,
								ns__,
								o,
								fids_
						)
					elif px in RESTRICTION_TYPES + OWL_SET_TYPES:
						if px in [
								OWL.minCardinality,
								OWL.minQualifiedCardinality,
								OWL.maxCardinality,
								OWL.maxQualifiedCardinality,
								OWL.cardinality,
								OWL.qualifiedCardinality,
						]:
							if px in [
									OWL.minCardinality,
									OWL.minQualifiedCardinality
							]:
								card = "min"
							elif px in [
									OWL.maxCardinality,
									OWL.maxQualifiedCardinality,
							]:
								card = "max"
							elif px in [
									OWL.cardinality,
									OWL.qualifiedCardinality
							]:
								card = "exactly"
							
							card = span(
									span(card, _class="cardinality"),
									span(str(o)))
						else:
							if px == OWL.allValuesFrom:
								card = "only"
							elif px == OWL.someValuesFrom:
								card = "some"
							elif px == OWL.hasValue:
								card = "value"
							elif px == OWL.unionOf:
								card = "union"
							elif px == OWL.intersectionOf:
								card = "intersection"
								
								card = span(
										span(card, _class="cardinality"),
										raw(_rdf_obj_single_html),
								)
							else:
								card = span(
										span(card, _class="cardinality"),
										span(
												_hyperlink_html(
														ont__,
														back_onts_,
														ns__,
														o,
														fids_,
														OWL.Class
												)
										),
								)
			
			restriction = span(prop, card, br()) if card is not None else prop
			restriction = (
					span(restriction, cls, br())
					if cls is not None else restriction
			)
			
			return span(restriction) if restriction is not None else "None"
		
		def _setclass_html(ont__, obj__, back_onts__, ns__, fids__):
			"""Makes lists of (union) 'ClassX or Class Y or ClassZ' or
			(intersection) 'ClassX and Class Y and ClassZ'"""
			if (obj__, OWL.unionOf, None) in ont__:
				joining_word = ' <span class="cardinality">or</span> '
			elif (obj__, OWL.intersectionOf, None) in ont__:
				joining_word = ' <span class="cardinality">and</span> '
			else:
				joining_word = ' <span class="cardinality">,</span> '
			
			class_set = set()
			for o in ont__.objects(obj__, OWL.unionOf | OWL.intersectionOf):
				for o2 in ont__.objects(o, RDF.rest * ZeroOrMore / RDF.first):
					class_set.add(
							_rdf_obj_single_html(
									ont__, back_onts__, ns__, o2, fids__, OWL.Class
							)
					)
			
			return raw(joining_word.join([mem.render() for mem in class_set]))
		
		def _bn_html(ont__, back_onts__, ns__, fids__, obj__: BNode):
			# TODO: remove back_onts and fids if not needed by subfunctions
			# What kind of BN is it?
			# An Agent, a Restriction or a Set Class (union/intersection)
			# handled all typing added in OntDoc inferencing
			if (obj__, RDF.type, PROV.Agent) in ont__:
				return _agent_html(ont__, obj__)
			elif (obj__, RDF.type, OWL.Restriction) in ont__:
				return _restriction_html(ont__, obj__, ns__)
			else:  # (obj, RDF.type, OWL.Class) in ont:  # Set Class
				return _setclass_html(ont__, obj__, back_onts__, ns__, fids__)
		
		if isinstance(obj_, URIRef):
			ret = _hyperlink_html(
					ont_, back_onts_, ns_, obj_, fids_, rdf_type__=rdf_type_
			)
		elif isinstance(obj_, BNode):
			ret = _bn_html(ont_, back_onts_, ns_, fids_, obj_)
		else:  # isinstance(obj, Literal):
			ret = _literal_html(obj_)
		
		return ret if ret is not None else span()
	
	if len(obj) == 1:
		return _rdf_obj_single_html(
				ont, back_onts, ns, obj[0], fids, rdf_type_=rdf_type, prop=prop
		)
	else:
		u_ = ul()
		for x in obj:
			u_.appendChild(
					li(
							_rdf_obj_single_html(
									ont, back_onts, ns, x, fids, rdf_type_=rdf_type, prop=prop
							)
					)
			)
		return u_


def prop_obj_pair_html(
		ont: Graph,
		back_onts: Graph,
		ns: Tuple[str, str],
		table_or_dl: str,
		prop_iri: URIRef,
		property_title: Literal,
		property_description: Literal,
		ont_title: Literal,
		fids,
		obj: List[Union[URIRef, BNode, Literal]],
		obj_type: Optional[str] = None,
):
	"""Makes an HTML Definition list dt & dd pair or a Table tr, th & td set,
	for a given RDF property & resource pair"""
	prop = a(
			str(property_title).title(),
			title=str(property_description).rstrip(".") +
			      ". Defined in " + str(ont_title),
			_class="hover_property",
			href=str(prop_iri),
	)
	o = rdf_obj_html(ont, back_onts, ns, obj, fids, rdf_type=obj_type, prop=prop_iri)
	
	if table_or_dl == "table":
		t = tr(th(prop), td(o))
	else:  # dl
		t = div(dt(prop), dd(o))
	
	return t


def section_html(
		section_title: str,
		ont: Graph,
		back_onts: Graph,
		ns: Tuple[str, str],
		obj_class: URIRef,
		prop_list: list,
		toc,
		toc_ul_id: str,
		fids: dict,
		props_labeled,
):
	"""Makes all the HTML (div, title & table) for all instances of a
	given RDF class, e.g. owl:Class or owl:ObjectProperty"""
	
	def _element_html(
			ont_: Graph,
			back_onts_: Graph,
			ns_: Tuple[str, str],
			iri: URIRef,
			fid: str,
			title_: str,
			ont_type: URIRef,
			props_list,
			this_props_,
			fids_: dict,
			props_labeled_,
	):
		"""Makes all the HTML (div, title & table) for one instance of a
		given RDF class, e.g. owl:Class or owl:ObjectProperty"""
		d = div(
				h3(
						title_,
						sup(
								ONT_TYPES[ont_type][0],
								_class="sup-" + ONT_TYPES[ont_type][0],
								title=ONT_TYPES[ont_type][1],
						),
				),
				id=fid,
				_class="property entity",
		)
		t = table(tr(th("IRI"), td(code(str(iri)))))
		# order the properties as per PROP_PROPS list order
		for prop in props_list:
			if prop != DCTERMS.title:
				if prop in this_props_.keys():
					t.appendChild(
							prop_obj_pair_html(
									ont_,
									back_onts_,
									ns_,
									"table",
									prop,
									props_labeled_.get(prop).get("title")
									if props_labeled_.get(prop) is not None
									else None,
									props_labeled_.get(prop).get("description")
									if props_labeled_.get(prop) is not None
									else None,
									props_labeled_.get(prop).get("ont_title")
									if props_labeled_.get(prop) is not None
									else None,
									fids_,
									this_props_[prop],
							)
					)
		d.appendChild(t)
		return d
	
	elems = div(id=toc_ul_id, _class="section")
	elems.appendChild(h2(section_title))
	# get all objects of this class
	for s_ in ont.subjects(predicate=RDF.type, object=obj_class):
		if obj_class == RDF.Property:
			specialised_props = [
					(s_, RDF.type, OWL.ObjectProperty),
					(s_, RDF.type, OWL.DatatypeProperty),
					(s_, RDF.type, OWL.AnnotationProperty),
					(s_, RDF.type, OWL.FunctionalProperty),
			]
			if any(x in ont for x in specialised_props):
				continue
		if isinstance(
				s_, URIRef
		):  # ignore blank nodes for things like [ owl:unionOf ( ... ) ]
			this_props = defaultdict(list)
			# get all properties of this object
			for p_, o in ont.predicate_objects(subject=s_):
				# ... in the property list for this class
				if p_ in prop_list:
					if p_ == RDFS.subClassOf \
							and (o, RDF.type, OWL.Restriction) in ont:
						this_props[ONTDOC.restriction].append(o)
					else:
						this_props[p_].append(o)
			if len(this_props[DCTERMS.title]) == 0:
				this_fid = generate_fid(None, s_, fids)
				this_title = make_title_from_iri(s_)
			else:
				this_fid = generate_fid(this_props[DCTERMS.title][0], s_, fids)
				this_title = this_props[DCTERMS.title]
			
			# add to ToC
			if toc.get(toc_ul_id) is None:
				toc[toc_ul_id] = []
			toc[toc_ul_id].append(("#" + this_fid, this_title))
			
			# create properties table
			elems.appendChild(
					_element_html(
							ont,
							back_onts,
							ns,
							s_,
							this_fid,
							this_title,
							obj_class,
							prop_list,
							this_props,
							fids,
							props_labeled,
					)
			)
	
	return elems


def de_space_html(html):
	return "".join([l_.strip().replace("\n", "") for l_ in html.split("\n")])



RDF_FOLDER = Path(__file__).parent / "rdf"


class PylodeError(Exception):
	pass


class OntDoc:
	"""Ontology Document class used to create HTML documentation
	from OWL Ontologies.
	Use:
		# initialise
		od = OntDoc(ontology="some-ontology-file.ttl")
		# produce HTML
		html = od.make_html()
		# or save HTML to a file
		od.make_html(destination="some-resulting-html-file.html")
	"""
	
	def __init__(self, ontology: Union[Graph, Path, str]):
		self.ont = load_ontology(ontology)
		self._ontdoc_inference(self.ont)
		self.back_onts = load_background_onts()
		self.back_onts_titles = load_background_onts_titles(self.back_onts)
		self.props_labeled = back_onts_label_props(self.back_onts)
		
		self.toc: Dict[str, str] = {}
		self.fids: Dict[str, str] = {}
		self.ns = get_ns(self.ont)
		
		# make HTML doc with title
		t = None
		for s in chain(
				self.ont.subjects(RDF.type, OWL.Ontology),
				self.ont.subjects(RDF.type, PROF.Profile),
				self.ont.subjects(RDF.type, SKOS.ConceptScheme),
		):
			for o2 in self.ont.objects(s, DCTERMS.title):
				t = str(o2)
		if t is None:
			raise PylodeError(
					"You MUST supply a title property "
					"(dcterms:title, rdf:label or sdo:name) for your ontology"
			)
		self.doc = dominate.document(title=t)
		
		with self.doc:
			self.content = div(id="content")
	
	def make_html(self, destination: Path = None, include_css: bool = True):
		"""Makes the complete OntDoc HTML document.
		Either writes to a file or returns a string"""
		self._make_head(
				self._make_schema_org(),
				include_css=include_css,
				destination=destination
		)
		self._make_body()
		
		if destination is not None:
			open(destination, "w").write(self.doc.render())
		else:
			return self.doc.render()
	
	def _ontdoc_inference(self, g):
		"""Expands the ontology's graph to make OntDoc querying easier.
		Uses axioms made up for OntDoc, but they are simple and obvious
		and don't collide with well-known ontologies"""
		# class types
		for s_ in g.subjects(RDF.type, OWL.Class):
			g.add((s_, RDF.type, RDFS.Class))
		
		# # property types
		# for s_ in chain(
		#     g.subjects(RDF.type, OWL.ObjectProperty),
		#     g.subjects(RDF.type, OWL.FunctionalProperty),
		#     g.subjects(RDF.type, OWL.DatatypeProperty),
		#     g.subjects(RDF.type, OWL.AnnotationProperty),
		# ):
		#     g.add((s_, RDF.type, RDF.Property))
		
		# name
		for s_, o in chain(
				g.subject_objects(DC.title),
				g.subject_objects(RDFS.label),
				g.subject_objects(SKOS.prefLabel),
				g.subject_objects(SDO.name),
		):
			g.add((s_, DCTERMS.title, o))
		
		# description
		for s_, o in chain(
				g.subject_objects(DC.description),
				g.subject_objects(RDFS.comment),
				g.subject_objects(SKOS.definition),
				g.subject_objects(SDO.description),
		):
			g.add((s_, DCTERMS.description, o))
		
		# source
		for s_, o in g.subject_objects(DC.source):
			g.add((s_, DCTERMS.source, o))
		
		#
		#   Blank Node Types
		#
		for s_ in g.subjects(OWL.onProperty, None):
			g.add((s_, RDF.type, OWL.Restriction))
		
		for s_ in chain(
				g.subjects(OWL.unionOf, None), g.subjects(OWL.intersectionOf, None)
		):
			g.add((s_, RDF.type, OWL.Class))
		
		# we do these next few so we only need to loop through
		# Class & Property properties once: single subject
		for s_, o in g.subject_objects(RDFS.subClassOf):
			g.add((o, ONTDOC.superClassOf, s_))
		
		for s_, o in g.subject_objects(RDFS.subPropertyOf):
			g.add((o, ONTDOC.superPropertyOf, s_))
		
		for s_, o in g.subject_objects(RDFS.domain):
			g.add((o, ONTDOC.inDomainOf, s_))
		
		for s_, o in g.subject_objects(SDO.domainIncludes):
			g.add((o, ONTDOC.inDomainIncludesOf, s_))
		
		for s_, o in g.subject_objects(RDFS.range):
			g.add((o, ONTDOC.inRangeOf, s_))
		
		for s_, o in g.subject_objects(SDO.rangeIncludes):
			g.add((o, ONTDOC.inRangeIncludesOf, s_))
		
		for s_, o in g.subject_objects(RDF.type):
			g.add((o, ONTDOC.hasMember, s_))
		
		#
		#   Agents
		#
		# creator
		for s_, o in chain(
				g.subject_objects(DC.creator),
				g.subject_objects(SDO.creator),
				g.subject_objects(SDO.author),
		):
			g.remove((s_, DC.creator, o))
			g.remove((s_, SDO.creator, o))
			g.remove((s_, SDO.author, o))
			g.add((s_, DCTERMS.creator, o))
		
		# contributor
		for s_, o in chain(
				g.subject_objects(DC.contributor),
				g.subject_objects(SDO.contributor),
		):
			g.remove((s_, DC.contributor, o))
			g.remove((s_, SDO.contributor, o))
			g.add((s_, DCTERMS.contributor, o))
		
		# publisher
		for s_, o in chain(
				g.subject_objects(DC.publisher), g.subject_objects(SDO.publisher)
		):
			g.remove((s_, DC.publisher, o))
			g.remove((s_, SDO.publisher, o))
			g.add((s_, DCTERMS.publisher, o))
		
		# indicate Agent instances from properties
		for o in chain(
				g.objects(None, DCTERMS.publisher),
				g.objects(None, DCTERMS.creator),
				g.objects(None, DCTERMS.contributor),
		):
			g.add((o, RDF.type, PROV.Agent))
		
		# Agent annotations
		for s_, o in g.subject_objects(FOAF.name):
			g.add((s_, SDO.name, o))
		
		for s_, o in g.subject_objects(FOAF.mbox):
			g.add((s_, SDO.email, o))
		
		for s_, o in g.subject_objects(ORG.memberOf):
			g.add((s_, SDO.affiliation, o))
	
	def _make_head(
			self,
			schema_org: Graph,
			include_css: bool = True,
			destination: Path = None
	):
		"""Healper function for make_html(). Makes <head>???</head> content"""
		with self.doc.head:
			# use standard pyLODE stylesheet
			if include_css:
				style(
						raw(
								"\n"
								+ open(Path(__file__).parent / "pylode.css").read()
								+ "\n\t"
						)
				)
			else:
				link(href="pylode.css", rel="stylesheet", type="text/css")
				shutil.copy(
						Path(__file__).parent / "pylode.css",
						destination.parent / "pylode.css")
			link(
					rel="icon",
					type="image/png",
					sizes="16x16",
					href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABhklEQVQ4jbWPzStEURjG3yQLirlGKUnKFO45Z+SjmXvnnmthQcpCoVhYmD/AwmJiI3OvZuZc2U3UlKU0/gAslMw9JgvhHxAr2fko7r0jHSsl+TgbTz2Lt5731/MASEiJW9ONml2QyX6rsGalmnT74v8BDf12hxJfpV8d1uwNKUBYszabdFv84L8B9X0rESVmmUup2fme0cVhJWaZHw4NWL1SewEAfDe6H3Dy6Ll456WEJsRZS630MwCAOI20ei5OBpxse5zcBZw8eS4uPpfIuDiCainIg9umBCU0GZzgLZ9Hn31OgoATL+CkLDGB5H1OKj4nFd/FBxUXJ0UZNb4edw/6nLyJXaj5FeCVyPLNIVmYK8TG1IwWb16L1gEACAFV90ftoT8bdOX0EeyY99gxBXZMgRz6qGb1KantAACI0UvE6F5XJqEjpsdURouI0Vt5gGOUkUNnPu7ObGIIMfNaGqDmjDRi9FZldF1lRgYzeqUyeoiY4ag5Iy3RgOYRM8+/M2bG8efsO4hGrpmJseyMAAAAAElFTkSuQmCC",
			)
			link(
					rel="icon",
					type="image/png",
					sizes="32x32",
					href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC40lEQVRYhe2UT0hUQRzHp6Iss1B3VZKIDbbdfW9mnoi4f3zzjkJQeOgS0SEIb1EWBGGlLLu460zQPQM1unUIIjA6rfpm6ZAhHjoIRVQUFUlEbG+euTsdXG1d3VL3bVD4g+9h+L35fT/8fvN7ADgY9aHY5fpIvK82HO9ysu66wxWOzbkjcekKx0a2ALYA/n2AGi3a6ArFezcidziecQygNhhrcUficjP6PwBqtGijKxy/thnVBePHywYoDsFhl53GV8SEcsTx4usCMLUewTVpc23BNvEzm6Neyf1+KcG2vwqwUjgrOJq2JmHftwmkVBRGTvncFodnbI7vChO/FRznCmHsNM7aHM9Yk7Df5iqsLMw9sMNOK2g+jS4IEz0UJv4iuJZb2RltWnB4UZqH6ioGAgAAGe5vtiZhtzDx7OoRadLmeM7m6IRjhnLMW2Vx1bA5GhAmnhIcz6/xNj4Ujsky8UspwfayjDPjsF2Y6L7N8Vzx/BfP+KPg6LbgSqd8DnfJW2CnbaLhfH5ephpqygJYvQU4Z3P82TLRsDDhUTnmrSq+Y3N0Mg+Xldy/zwEAnLMWZ3pHpNExmfLs/t0dOdVcbT0JeKxUwFP2VljjqiE47Jp53LTXNxhsUZjerTByXWX6VZWRs/4bIQ2ACv+UAomgDzLCISNZxAxZKMhIDjLy1JfsaK+I+eGBUBNk5E2x8RogX/PdcDZUqieWTSh5D6nOVKqfhoycUmlHFFIyu5RXqf7AcQDISCpv/tqbMBqK883RtmpISRoxQyJKPgGn3wNk5NEigDFa6hslqV/Kj+FdBQD0bshIDlKSLlVcoWQo36UhR80BAMB73lulMn0EMpJTqD6qJiOt3mho/8GbkT2BZNgDB/V+RI0fkOrT3kRIVQbaDizJm2hdNbINBxwk5xAj3yEjuV9rZ1iIkgxixkLBA83mz8uCjLwoGwAx0vOnFSy5mtR4VTaAQvVORMnwZgSpzkrV/QmdE2tKe46+MQAAAABJRU5ErkJggg==",
			)
			meta(http_equiv="Content-Type", content="text/html; charset=utf-8")
			script(
					raw("\n" + schema_org.serialize(format="json-ld") + "\n\t"),
					type="application/ld+json",
					id="schema.org",
			)
	
	def _make_body(self):
		"""Healper function for make_html(). Makes <body>???</body> content.
		Just calls other helper functions in order"""
		self._make_pylode_logo()
		self._make_metadata()
		self._make_main_sections()
		self._make_namespaces()
		self._make_legend()
		self._make_toc()
	
	def _make_pylode_logo(self):
		with self.doc:
			with div(id="pylode"):
				with p("made by "):
					with a(href="https://github.com/rdflib/pyLODE"):
						span("p", id="p")
						span("y", id="y")
						span("LODE")
					a(
							__version__,
							href="https://github.com/rdflib/pyLODE/release/"
							     + __version__,
							id="version",
					)
	
	def _make_metadata(self):
		# get all ONT_PROPS props and their (multiple) values
		this_onts_props = defaultdict(list)
		for s_ in chain(
				self.ont.subjects(predicate=RDF.type, object=OWL.Ontology),
				self.ont.subjects(predicate=RDF.type, object=SKOS.ConceptScheme),
				self.ont.subjects(predicate=RDF.type, object=PROF.Profile),
		):
			iri = s_
			for p_, o in self.ont.predicate_objects(s_):
				if p_ in ONT_PROPS:
					this_onts_props[p_].append(o)
		
		# make HTML for all props in order of ONT_PROPS
		sec = div(
				h1(this_onts_props[DCTERMS.title]),
				id="metadata",
				_class="section")
		sec.appendChild(h2("Metadata"))
		d = dl(div(dt(strong("IRI")), dd(code(str(iri)))))
		for prop in ONT_PROPS:
			if prop in this_onts_props.keys():
				d.appendChild(
						prop_obj_pair_html(
								self.ont,
								self.back_onts,
								self.ns,
								"dl",
								prop,
								self.props_labeled[prop]["title"],
								self.props_labeled[prop]["description"],
								self.props_labeled[prop]["ont_title"],
								self.fids,
								this_onts_props[prop],
						)
				)
		sec.appendChild(d)
		self.content.appendChild(sec)
	
	def _make_schema_org(self):
		sdo = Graph()
		for ont_iri in chain(
				self.ont.subjects(predicate=RDF.type, object=OWL.Ontology),
				self.ont.subjects(predicate=RDF.type, object=SKOS.ConceptScheme),
				self.ont.subjects(predicate=RDF.type, object=PROF.Profile),
		):
			sdo.add((ont_iri, RDF.type, SDO.DefinedTermSet))
			for p_, o in self.ont.predicate_objects(ont_iri):
				if p_ == DCTERMS.title:
					sdo.add((ont_iri, SDO.name, o))
				elif p_ == DCTERMS.description:
					sdo.add((ont_iri, SDO.description, o))
				elif p_ == DCTERMS.publisher:
					sdo.add((ont_iri, SDO.publisher, o))
					if not isinstance(o, Literal):
						for p2, o2 in self.ont.predicate_objects(o):
							if p2 in AGENT_PROPS:
								sdo.add((o, p2, o2))
				elif p_ == DCTERMS.creator:
					sdo.add((ont_iri, SDO.creator, o))
					if not isinstance(o, Literal):
						for p2, o2 in self.ont.predicate_objects(o):
							if p2 in AGENT_PROPS:
								sdo.add((o, p2, o2))
				elif p_ == DCTERMS.contributor:
					sdo.add((ont_iri, SDO.contributor, o))
					if not isinstance(o, Literal):
						for p2, o2 in self.ont.predicate_objects(o):
							if p2 in AGENT_PROPS:
								sdo.add((o, p2, o2))
				elif p_ == DCTERMS.created:
					sdo.add((ont_iri, SDO.dateCreated, o))
				elif p_ == DCTERMS.modified:
					sdo.add((ont_iri, SDO.dateModified, o))
				elif p_ == DCTERMS.issued:
					sdo.add((ont_iri, SDO.dateIssued, o))
				elif p_ == DCTERMS.license:
					sdo.add((ont_iri, SDO.license, o))
				elif p_ == DCTERMS.rights:
					sdo.add((ont_iri, SDO.copyrightNotice, o))
		
		return sdo
	
	def _make_main_sections(self):
		with self.content:
			if (None, RDF.type, OWL.Class) in self.ont:
				d = section_html(
						"Classes",
						self.ont,
						self.back_onts,
						self.ns,
						OWL.Class,
						CLASS_PROPS,
						self.toc,
						"classes",
						self.fids,
						self.props_labeled,
				)
				d.render()
			
			if (None, RDF.type, RDF.Property) in self.ont:
				d = section_html(
						"Properties",
						self.ont,
						self.back_onts,
						self.ns,
						RDF.Property,
						PROP_PROPS,
						self.toc,
						"properties",
						self.fids,
						self.props_labeled,
				)
				d.render()
			
			if (None, RDF.type, OWL.ObjectProperty) in self.ont:
				d = section_html(
						"Object Properties",
						self.ont,
						self.back_onts,
						self.ns,
						OWL.ObjectProperty,
						PROP_PROPS,
						self.toc,
						"objectproperties",
						self.fids,
						self.props_labeled,
				)
				d.render()
			
			if (None, RDF.type, OWL.DatatypeProperty) in self.ont:
				d = section_html(
						"Datatype Properties",
						self.ont,
						self.back_onts,
						self.ns,
						OWL.DatatypeProperty,
						PROP_PROPS,
						self.toc,
						"datatypeproperties",
						self.fids,
						self.props_labeled,
				)
				d.render()
			
			if (None, RDF.type, OWL.AnnotationProperty) in self.ont:
				d = section_html(
						"Annotation Properties",
						self.ont,
						self.back_onts,
						self.ns,
						OWL.AnnotationProperty,
						PROP_PROPS,
						self.toc,
						"annotationproperties",
						self.fids,
						self.props_labeled,
				)
				d.render()
			
			if (None, RDF.type, OWL.FunctionalProperty) in self.ont:
				d = section_html(
						"Functional Properties",
						self.ont,
						self.back_onts,
						self.ns,
						OWL.FunctionalProperty,
						PROP_PROPS,
						self.toc,
						"functionalproperties",
						self.fids,
						self.props_labeled,
				)
				d.render()
	
	def _make_legend(self):
		with self.content:
			with div(id="legend"):
				h2("Legend")
				with table(_class="entity"):
					
					if self.toc.get("classes") is not None:
						with tr():
							td(sup(
									"c",
									_class="sup-c",
									title="OWL/RDFS Class"))
							td("Classes")
					if self.toc.get("properties") is not None:
						with tr():
							td(sup("p", _class="sup-p", title="RDF Property"))
							td("Properties")
					if self.toc.get("objectproperties") is not None:
						with tr():
							td(sup(
									"op",
									_class="sup-op",
									title="OWL Object Property"))
							td("Object Properties")
					if self.toc.get("datatypeproperties") is not None:
						with tr():
							td(
									sup(
											"dp",
											_class="sup-dp",
											title="OWL Datatype Property",
									)
							)
							td("Datatype Properties")
					if self.toc.get("annotationproperties") is not None:
						with tr():
							td(
									sup(
											"ap",
											_class="sup-ap",
											title="OWL Annotation Property",
									)
							)
							td("Annotation Properties")
					if self.toc.get("functionalproperties") is not None:
						with tr():
							td(
									sup(
											"fp",
											_class="sup-fp",
											title="OWL Functional Property",
									)
							)
							td("Functional Properties")
					if self.toc.get("named_individuals") is not None:
						with tr():
							td(sup(
									"ni",
									_class="sup-ni",
									title="OWL Named Individual"
							))
							td("Named Individuals")
	
	def _make_namespaces(self):
		# get only namespaces used in ont
		nses = {}
		for n in chain(
				self.ont.subjects(),
				self.ont.predicates(),
				self.ont.objects()
		):
			for prefix, ns in self.ont.namespaces():
				if str(n).startswith(ns):
					nses[prefix] = ns
		
		with self.content:
			with div(id="namespaces"):
				h2("Namespaces")
				with dl():
					if self.toc.get("namespaces") is None:
						self.toc["namespaces"] = []
					for prefix, ns in sorted(nses.items()):
						p_ = prefix if prefix != "" else ":"
						dt(p_, id=p_)
						dd(code(ns))
						self.toc["namespaces"].append(("#" + prefix, prefix))
	
	def _make_toc(self):
		with self.doc:
			with div(id="toc"):
				h3("Table of Contents")
				with ul(_class="first"):
					li(h4(a("Metadata", href="#metadata")))
					
					if (
							self.toc.get("classes") is not None
							and len(self.toc["classes"]) > 0
					):
						with li():
							h4(a("Classes", href="#classes"))
							with ul(_class="second"):
								for c in self.toc["classes"]:
									li(a(c[1], href=c[0]))
					
					if (
							self.toc.get("properties") is not None
							and len(self.toc["properties"]) > 0
					):
						with li():
							h4(a("Properties", href="#properties"))
							with ul(_class="second"):
								for c in self.toc["properties"]:
									li(a(c[1], href=c[0]))
					
					if (
							self.toc.get("objectproperties") is not None
							and len(self.toc["objectproperties"]) > 0
					):
						with li():
							h4(a(
									"Object Properties",
									href="#objectproperties"
							))
							with ul(_class="second"):
								for c in self.toc["objectproperties"]:
									li(a(c[1], href=c[0]))
					
					if (
							self.toc.get("datatypeproperties") is not None
							and len(self.toc["datatypeproperties"]) > 0
					):
						with li():
							h4(a(
									"Datatype Properties",
									href="#datatypeproperties"
							))
							with ul(_class="second"):
								for c in self.toc["datatypeproperties"]:
									li(a(c[1], href=c[0]))
					
					if (
							self.toc.get("annotationproperties") is not None
							and len(self.toc["annotationproperties"]) > 0
					):
						with li():
							h4(a(
									"Annotation Properties",
									href="#annotationproperties"
							))
							with ul(_class="second"):
								for c in self.toc["annotationproperties"]:
									li(a(c[1], href=c[0]))
					
					if (
							self.toc.get("functionalproperties") is not None
							and len(self.toc["functionalproperties"]) > 0
					):
						with li():
							h4(a(
									"Functional Properties",
									href="#functionalproperties"
							))
							with ul(_class="second"):
								for c in self.toc["functionalproperties"]:
									li(a(c[1], href=c[0]))
					
					with li():
						h4(a("Namespaces", href="#namespaces"))
						with ul(_class="second"):
							for n in self.toc["namespaces"]:
								li(a(n[1], href="#" + n[1]))
					
					li(h4(a("Legend", href="#legend")), ul(_class="second"))
