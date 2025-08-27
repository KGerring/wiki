#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename = namespaces
# author=KGerring
# date = 3/30/22
# project alltypes
# docs root 
"""
 alltypes  

"""
from __future__ import annotations

from dataclasses import dataclass as dclass

import aenum
import aniso8601
import anyconfig
import asttokens
import bibsearch
import bibsearch.bibsearch._get_parser
import bibtexparser
import bidict
import Bio  # Newick; Bio.Phylo.BaseTree; Bio.Phylo._cdao_owl
#Bio.Phylo._cdao_owl.resolve_uri; Bio.Phylo.CDAOIO
#resolve_uri
import bleach  # ALLOWED_ATTRIBUTES, ALLOWED_PROTOCOLS, Linker, Cleaner
import box
import bs4
import bytecode
import click
import click_shell
import concepts
import configargparse
import cufflinks
import dacite
#prefixcommons.curie_util.read_biocontext('monarch_context')
import datapackage
import datasets
import defusedxml
import dill
import diskcache
import docformatter
import docstring_parser
import dominate
import email_reply_parser
import enchant
import extruct
import fastavro
#libarchive
import fastobo  # fastobo.doc.OboDoc; doc = fastobo.load("tests/data/ms.obo"); fastobo.dump_owl(doc, "tests/data/ms.ofn", format="ofn")
import feedparser
import frontmatter
import fsspec
import furl
import genson
import graphtage
import hexbytes
import html2text
import html5lib
import humanize
import hyperlink  # scheme_uses_netloc, register_scheme,parse,DecodedURL, URL, parse
import icdiff
import identify
import idna
import ietfdata
import influxdb_client
import intervaltree
import isodate
import isort
import jinja2
import jschon
import jsonasobj
import jsonasobj2
import jsondiff
import jsonschema
import jupytext
import kombu
import language_tags
import lark
import lizard
import loguru
import lunchbox
import lxml
import markdown
import metaflow
import mf2py
import mimeparse
import mimerender
import more_itertools
import multipledispatch
import murmurhash
import myst_parser
import nltk
import normality
import numpydoc
import owlready2
import pantomime  # normalize_extension, parse_mimetype
import pavlova
import port_for  # port_for.PortStore(); /etc/port-for.conf
import pronto
import pyaml
import pydantic
#import pyfiglet
import pyld
import owlrl, tableschema, datapackage
#import pyrdfa3
#pyshex.prefixlib.PrefixLibrary
import pyshex  # pyshex.known_prefixes, PrefixLibrary
import pytaxonomies  # Taxonomies
import rdfextras
import rdflib

import readme_renderer
import recommonmark
import rfc3986  # URIReference, iri_reference, urlparse, urlparse, normalize_uri
import rfc3987  # ,parse, compose, http://tools.ietf.org/html/rfc3986#section-5.3, list(rfc3987.patterns); rfc3987._uri_rules, _common_rules
import rich
import routes
import ruamel
import skosify
import skosprovider
import thinc
import toolz
import typer
import ubelt
import uritemplate  # URITemplate
import w3lib
import wasabi
import webob
import werkzeug
import xml2rfc
import xmltodict


from attr import define, field

from cachecontrol.caches import FileCache, RedisCache
from cachecontrol.controller import CacheController
from gridfs import GridFS

from linkml_runtime.linkml_model.types import Uri, Uriorcurie
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.metamodelcore import URI, Curie, URIorCURIE
from prefixcommons import contract_uri  # get_prefixes, default_curie_maps
from prefixcommons import curie_transformer, curie_util, expand_uri
from prefixcommons.curie_transformer import \
    CsvTransformer  # get_prefixes,default_curie_maps,read_biocontext
from prefixcommons.curie_transformer import Transformer
from prefixcommons.curie_util import (
    extract_prefixmap,
    read_biocontext,
    read_local_jsonld_context,
    read_remote_jsonld_context
)
from redis import Redis, StrictRedis
from requests_cache import (
    CachedHTTPResponse,
    CachedSession,
    CacheMixin,
    get_cache,
    install_cache
)

from requests_cache.backends.base import BaseCache
from requests_cache.backends.gridfs import GridFSCache, GridFSPickleDict
from requests_cache.backends.mongodb import (
    MongoCache,
    MongoDict,
    MongoPickleDict
)
from requests_cache.backends.redis import RedisCache, RedisDict, RedisHashDict
from requests_cache.models import (
    AnyRequest,
    AnyResponse,
    CachedRequest,
    CachedResponse
)

from requests_html import HTMLSession, HTML

#CommentedMap, CommentedSeq, DefaultFetcher, add_lc_filename, relname, yaml_no_t, file_uri, uri_file_path
from ruamel.yaml.comments import CommentedBase
from werkzeug.urls import (
    iri_to_uri,
    uri_to_iri,
    url_fix,
    url_join,
    url_parse,
    url_unparse
)

import sys
import os
import re


"""
import pubs
from pubs import datacache, databroker, filebroker, pretty, utils, repo
from pubs import paper, events, content, apis, update
from pubs import uis, query, pubs_cmd, plugins, paper, p3, events, content, command_utils, \
    color, apis, bibstruct, completion, content
from pubs import templates, config, plugs, commands
import pubs.templates.str_templates
import pubs.config.conf as conf #load_default_conf, get_confpath, check_conf
#/Users/kristen/.pubsrc
"""
#import feedgenerator

 # DecodedURL

#import hdfs    scheme://username:password@host:port/path?query#fragment



#import kgx


#session = CachedSession('http_cache', backend='mongodb', host='192.168.1.63', port=27017)
# backend = MongoCache(host='192.168.1.63', port=27017)
#session = CachedSession('http_cache', backend=backend)

#import skosify #localname, get_concept_scheme, detect_namespace, create_concept_scheme
#expand_curielike, expand_mapping_target, Config, config

#CONTEXT
#import skosprovider #ConceptScheme, Collection, Registry, Concept, CONTEXT, dct:bibliographicCitation
#import spark_parser

#import textblob




#bibsearch,datasets-cli,datapackage,extruct,fastavro,genson,graphtage
#'html2text
#ia,jfl,pyjson5
#jsondiff, jsonschema,jupytext, kgx,
#gen-csv
#gen-jsonld-context,gen-linkml,gen-namespaces,gen-prefix-map,gen-projec, gen-proto
#gen-rdf,gen-sparql, gen-sqlddl-legacy, gen-sqltables,gen-sssom,gen-sqlddl
#linkml-convert,run-tutorial,linkml-sqldb,
#linkml-jsonschema-validate, linkml-apply, gen-api-datamodel, gen-crud-datamodel, comparefiles,gen-python-api
#metaflow, myst-anchors, netaddr
#ontogram, openapi-spec-validator, pubs
#pypistats pytaxonomies, schema-salad-tool



def file_uri(path: str, split_frag: bool = False) -> str:
    if path.startswith("file://"):
        return path
    if split_frag:
        pathsp = path.split("#", 2)
        if len(pathsp) == 2:
            frag = "#" + urllib.parse.quote(str(pathsp[1]))
        else:
            frag = ""
        urlpath = urllib.request.pathname2url(str(pathsp[0]))
    else:
        urlpath = urllib.request.pathname2url(path)
        frag = ""
    if urlpath.startswith("//"):
        return f"file:{urlpath}{frag}"
    return f"file://{urlpath}{frag}"

os_c = ('http://open-services.net/ns/core#',
        'https://raw.githubusercontent.com/oslc-op/oslc-specs/master/specs/core/core-vocab.ttl')
#https://open-services.net/specifications/vocabularies/

#http://openlinksw.com/services/facets/1.0/

obo = 'http://purl.obolibrary.org/obo/'
cido = 'http://purl.obolibrary.org/obo/cido.owl/'

ldci = 'https://dcmi.github.io/ldci/D2695955'
ldci_structure = 'https://dcmi.github.io/ldci/structure/'
'https://raw.githubusercontent.com/dcmi/ldci/master/docs/D2695955.json'
'http://asn.desire2learn.com/resources/D2695955_manifest.json'
dcterm = 'http://purl.org/dc/terms'
aut = 'http://www.loc.gov/loc.terms/relators/aut'
cidoc = 'http://purl.org/NET/cidoc-crm/core#'
api = ('http://purl.org/linked-data/api/vocab',
       'http://linked-data-api.googlecode.com/svn/trunk/vocab/api.ttl')
reg = ('http://purl.org/linked-data/registry',
       'https://raw.githubusercontent.com/ukgovld/registry-core/master/src/main/vocabs/registryVocab.ttl')
ldp = 'http://www.w3.org/ns/ldp#'

sdmx = ('http://purl.org/linked-data/sdmx',
        'https://raw.githubusercontent.com/UKGovLD/publishing-statistical-data/master/specs/src/main/vocab/sdmx.ttl')
        
#http://purl.org/linked-data/sdmx/2009/attribute#'

rss_href="http://purl.org/rss/1.0/spec"
mods = "http://purl.org/rss/1.0/modules/"
cnt = "http://purl.org/rss/1.0/modules/content/"
a = 'http://purl.org/rss/1.0/modules/proposed.html'
prism = 'http://purl.org/rss/1.0/modules/prism/'

csv = 'http://cvs.web.resource.org/'

rdf = ('http://purl.org/rss/1.0/schema.rdf', 'https://web.resource.org/rss/1.0/schema.rdf')
webreference = 'http://www.webreference.com/authoring/languages/xml/rss/'

#http://purl.org/rss/1.0/modules/content/
#http://purl.org/twc/vocab/datacarver#
#http://purl.org/vocommons/bridge#

#http://www.getty.edu/research/tools/vocabularies/lod/
void= ('http://vocab.getty.edu/.well-known/void', 'http://vocab.getty.edu/void.ttl')
#http://vocab.getty.edu/
#http://vocab.getty.edu/ontology

class prefixcc:
    _base =     'http://prefix.cc/popular/all.file.txt'
    _all_vall = 'http://prefix.cc/popular/all.file.vann'
    all_cc =    'http://prefix.cc/popular/all.file.json'
    _context =  'http://prefix.cc/context'
    _fmts =     'http://prefix.cc/about/formats'
    vann =      "http://purl.org/vocab/vann/"

monarch_context = 'https://raw.githubusercontent.com/prefixcommons/biocontext/master/registry/monarch_context.jsonld'
mon = 'https://monarchinitiative.org/.well-known/genid/'

class prefixes:
    json_ld_rc = 'http://www.w3.org/2013/json-ld-context/rdfa11'
    context=        'https://w3c.github.io/json-ld-rc/context.jsonld'
    pre =           'https://w3c.github.io/json-ld-rc/prefixes.ttl'
    rdfa_ld = 'https://w3c.github.io/json-ld-rc/rdfa-1.1.jsonld'
    rdfa_rc = "https://w3c.github.io/json-ld-rc/rdfa-1.1.ttl"
    rdfa= "http://www.w3.org/ns/rdfa#"
    ics = 'http://www.w3.org/TR/rdfa-core/#s_initialcontexts'
    biolink = ('https://w3id.org/biolink/vocab/', 'https://biolink.github.io/biolink-model/docs/')
    'http://www.obofoundry.org/ro/ro.owl'
    #http://www.w3.org/TR/grddl-primer/
    'https://sparontologies.github.io/cito/current/cito.html'
    
    study_protocol = "http://purl.org/net/OCRe/study_protocol.owl#"
    geopolitical = "http://aims.fao.org/aos/geopolitical.owl#"
    vitro = "http://vitro.mannlib.cornell.edu/ns/vitro/0.7#"
    skos2 = "http://www.w3.org/2008/05/skos#"
    
    vcore="http://vivoweb.org/ontology/core#", 'https://duraspace.org/wp-content/uploads/2020/02/vivo.owl'
    obo = "http://purl.obolibrary.org/obo/", 'http://ontologies.berkeleybop.org'
    statistics = "http://purl.org/net/OCRe/statistics.owl#"
    swrl=   "http://www.w3.org/2003/11/swrl#"
    error = "http://www.essepuntato.it/2009/10/error/"
    swrlb = "http://www.w3.org/2003/11/swrlb#"
    
    #http://purl.org/ontology/bibo
    
    collections = 'https://raw.githubusercontent.com/collections-ontology/collections-ontology/master/collections.owl'
    
            #'http://raw.githubusercontent.com/SPAROntologies/cito/master/docs/current/cito.owl'
    cito = 'http://raw.githubusercontent.com/SPAROntologies/cito/master/docs/current/cito.owl'
    
    #oo = 'http://www.sparontologies.net/ontologies/cito'
    oa = 'http://www.w3.org/ns/oa', #oa.rdf #http://www.w3.org/ns/oa.ttl
    
    rdfs2html = 'http://www.w3.org/2002/06/rdfs2html'
    w3p = rec54 = 'http://www.w3.org/2001/02pd/rec54#'
    cnt = 'http://www.w3.org/2011/content#'
    gr = 'http://purl.org/goodrelations/v1#', 'http://www.heppnetz.de/ontologies/goodrelations/v1.owl'
    iiif = 'http://iiif.io/api/image/2#', 'https://iiif.io/api/image/2/ontology.xml'
    oa = 'http://www.w3.org/ns/oa#'
    ore = 'http://www.openarchives.org/ore/terms/'
    
    pcdm = 'http://pcdm.org/models#', 'https://pcdm.org/2016/04/18/models'
    wot = "http://xmlns.com/wot/0.1/"
    vs = "http://www.w3.org/2003/06/sw-vocab-status/ns#"
    
    sioc = 'http://rdfs.org/sioc/ns#'
    svcs = 'http://rdfs.org/sioc/services#'
    trig = 'http://www.w3.org/2004/03/trix/rdfg-1/'
    rec54 = 'http://www.w3.org/2001/02pd/rec54#rec54.rdf'
    doc = "http://www.w3.org/2000/10/swap/pim/doc#"
    log = "http://www.w3.org/2000/10/swap/log#"
    
    #http://www.w3.org/Consortium/Process/tr.html#Reports
    #http://www.w3.org/Consortium/Process/tr.html
    #http://lexvo.org/ontology#Language
    #http://www.openannotation.org/spec/tutorial/
    
    cnt = 'http://www.w3.org/2011/content#'
    trig = 'http://www.w3.org/2004/03/trix/rdfg-1/'
    
    'http://www.w3.org/community/openannotation'
    'https://www.w3.org/community/openannotation/wiki/Main_Page'
    'http://www.w3.org/community'
    'http://www.w3.org/community/openannotation/wiki/Incubator'
    'http://www.w3.org/community/openannotation/wiki/UseCases'
    'http://www.w3.org/community/openannotation/wiki/Serializations'
    'http://www.w3.org/community/openannotation/wiki/Provenance'
    'http://www.w3.org/community/openannotation/wiki/RDFa'
    'http://www.w3.org/community/openannotation/wiki/Open_Issues'
    'http://www.w3.org/community/openannotation/wiki/Challenges'
    'http://www.w3.org/community/openannotation/wiki/Meetings'
    'http://www.w3.org/community/openannotation/'
    
    
    
    #http://bibliontology.com/
    #/ontologies/fabio
    #/ontologies/biro
    #/ontologies/pwo
    #http://vocab.org/frbr/core
    #/ontologies/datacite
    #/ontologies/fr
    cito = 'https://sparontologies.github.io/cito/current/cito.html'
    ('https://sparontologies.github.io/cito/current/cito.xml',
     'https://sparontologies.github.io/cito/current/cito.ttl',
     'https://sparontologies.github.io/cito/current/cito.json')
    
    cm = 'https://w3id.org/spar/mediatype/text/cache-manifest'
    protege = "http://protege.stanford.edu/plugins/owl/protege#"
  

INITIAL_CTX = (('as', 'https://www.w3.org/ns/activitystreams#'),
               ('cc', 'http://creativecommons.org/ns#'),
               ('csvw', 'http://www.w3.org/ns/csvw#'),
               ('ctag', 'http://commontag.org/ns#'),
               ('dc', 'http://purl.org/dc/terms/'),
               ('dc11', 'http://purl.org/dc/elements/1.1/'),
               ('dcat', 'http://www.w3.org/ns/dcat#'),
               ('dcterms', 'http://purl.org/dc/terms/'),
               ('dqv', 'http://www.w3.org/ns/dqv#'),
               ('duv', 'https://www.w3.org/ns/duv#'),
               ('foaf', 'http://xmlns.com/foaf/0.1/'),
               ('gr', 'http://purl.org/goodrelations/v1#'),
               ('grddl', 'http://www.w3.org/2003/g/data-view#'),
               ('ical', 'http://www.w3.org/2002/12/cal/icaltzd#'),
               ('jsonld', 'http://www.w3.org/ns/json-ld#'),
               ('ldp', 'http://www.w3.org/ns/ldp#'),
               ('ma', 'http://www.w3.org/ns/ma-ont#'),
               ('oa', 'http://www.w3.org/ns/oa#'),
               ('odrl', 'http://www.w3.org/ns/odrl/2/'),
               ('og', 'http://ogp.me/ns#'),
               ('org', 'http://www.w3.org/ns/org#'),
               ('owl', 'http://www.w3.org/2002/07/owl#'),
               ('prov', 'http://www.w3.org/ns/prov#'),
               ('qb', 'http://purl.org/linked-data/cube#'),
               ('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
               ('rdfa', 'http://www.w3.org/ns/rdfa#'),
               ('rdfs', 'http://www.w3.org/2000/01/rdf-schema#'),
               ('rev', 'http://purl.org/stuff/rev#'),
               ('rif', 'http://www.w3.org/2007/rif#'),
               ('rr', 'http://www.w3.org/ns/r2rml#'),
               ('schema', 'http://schema.org/'),
               ('sd', 'http://www.w3.org/ns/sparql-service-description#'),
               ('sioc', 'http://rdfs.org/sioc/ns#'),
               ('skos', 'http://www.w3.org/2004/02/skos/core#'),
               ('skosxl', 'http://www.w3.org/2008/05/skos-xl#'),
               ('time', 'http://www.w3.org/2006/time#'),
               ('v', 'http://rdf.data-vocabulary.org/#'),
               ('vcard', 'http://www.w3.org/2006/vcard/ns#'),
               ('void', 'http://rdfs.org/ns/void#'),
               ('wdr', 'http://www.w3.org/2007/05/powder#'),
               ('wdrs', 'http://www.w3.org/2007/05/powder-s#'),
               ('xhv', 'http://www.w3.org/1999/xhtml/vocab#'),
               ('xml', 'http://www.w3.org/XML/1998/namespace'),
               ('xsd', 'http://www.w3.org/2001/XMLSchema#'))


#: http://www.w3.org/ns/formats
#  http://www.w3.org/ns/formats/Format
#: http://www.w3.org/ns/formats/data/Turtle
#: formats:media_type #http://www.w3.org/ns/formats/media_type
#: formats:preferred_suffix
#rdfs:isDefinedBy <http://www.w3.org/TR/turtle/> ;
#rdfs:seeAlso <http://www.w3.org/TR/turtle/#sec-mediaReg>
#formats:media_type "text/turtle" ;
#formats:preferred_suffix ".ttl" .

#rdfs:subClassOf <http://rdfs.org/ns/void> .


scot = 'http://rdfs.org/scot/spec', 'http://rdfs.org/scot/ns#'
sdm = "https://w3id.org/vocab/sdm" #SPARQL endpoint metadata, 'http://linkedvocabs.org/vocab/sdm/sdm.owl'
#http://purl.org/vocommons/voaf#vocabulary
cal = 'http://reference.data.gov.uk/def/intervals/CalendarInterval'
sd = "http://www.w3.org/ns/sparql-service-description"
#  http://www.w3.org/ns/r2rml#
#sio = "http://semanticscience.org/ontology/sio.owl"
#  http://protege.stanford.edu/plugins/owl/protege#
protege = 'https://protege.stanford.edu/plugins/owl/dc/protege-dc.owl'
relational = 'http://ontology.cybershare.utep.edu/dbowl/relational-to-ontology-mapping-primitive.owl'


# https://dbpedia.org/sparql
    # /sparql/?help=nsdecl
    #/sparql/?help=rdfinf
    #/sparql/?help=macrolibs
    #/sparql/?help=views
    #/sparql/?help=enable_cxml
    #/conductor, /fct,
    # sparql_form
    # browsing_links: HTML (table) = 'text/x-html+tr'
    # CXML (Pivot Collection): text/cxml
    # Turtle (beautified): application/x-nice-turtle
    # text/cxml+qrcode
    # XHTML+RDFa: application/xhtml+xml
    # ODATA/JSON: application/odata+json
    # HTML+Microdata (table): application/x-nice-microdata
    # Microdata/JSON: application/microdata+json
    # application/sparql-results+xml
    # application/sparql-results+json
    
    #ld_plain: application/x-ld+json
    #ld_ctx: application/ld+json
    #html_list: text/x-html+ul
    #html_table: text/x-html+tr
    #html_turtle: text/x-html-script-turtle
    #Turtle (beautified - browsing oriented)', 'text/x-html-nice-turtle
    
    # http://www.w3.org/ns/sparql-service-description#UnionDefaultGraph
    # http://www.w3.org/ns/sparql-service-description#DereferencesURIs
    # http://www.w3.org/ns/sparql-service-description.html
    


class AwesomeOpenSource:
    url =  'https://awesomeopensource.com/projects'
    cats = '/Users/kristen/getallcategories.json'
    # /Users/kristen/.wget-hsts


# https://www.w3.org/TR/rdftm-survey/               "http://validator.w3.org/check?uri=referer"
# https://www.w3.org/TR/2013/NOTE-ld-glossary-20130627/
# https://www.w3.org/TR/2011/NOTE-void-20110303/
# http://www.w3.org/TR/cooluris/
# https://www.w3.org/TR/swbp-vocab-pub/



# extruct = extruct.tool:main
# forte.data.ontology.ontology_code_generator OntologyCodeGenerator
# /opt/anaconda3/envs/py39/lib/python3.9/site-packages/forte/ontology_specs
# forte.data.ontology.code_generation_objects.ImportManager
# html2text isort-identify-imports   jupytext, linkml-sparql-validate
# pgist
#shexeval #pyshex.shex_evaluator:evaluate_cli pyshex.shex_evaluator.genargs
#xml2rfc

#xmlschema.validators.schema, xmlschema.cli, xml2json
#xmlschema.resources.fetch_schema_locations
#iter_select,XPath2Parser,get_namespace,normalize_url,xmlschema.resources.is_local_url,normalize_locations,fetch_namespaces



HOSTS = ('arxiv.org',
         'bitbucket.org',
         'dxr.mozilla.org',
         'files.pythonhosted.org',
         'gist.githubusercontent.com',
         'git.kernel.org',
         'github-releases.githubusercontent.com',
         'github.com',
         'hg.mozilla.org',
         'patch-diff.githubusercontent.com',
         'raw.githubusercontent.com',
         'tools.ietf.org',
         'www.niso.org',
         'www.python.org',
         'www.w3.org')



w3c_tags = (('accessibility',
             'All specifications aiming at making the Web accessible to people with disabilities'),
            ('browser',
             'Specifications for Web browsers and other interactive user agents'),
            ('css', 'How documents are presented on screens using CSS'),
            ('data',
             'Specifications to facilitate the creation, exchange, and usage of semantically rich data on the Web'),
            ('dom', 'Specifications describing the Document Object Model (DOM)'),
            ('graphics',
             'Specifications dealing with graphical content (image formats, web fonts, canvas, etc)'),
            ('html',
             'Defines the HyperText Markup Language (HTML) format and its extensions'),
            ('http', 'client-server protocol allowing resources fetching such as HTML.'),
            ('i18n',
             'How to use Web Technologies with different languages, scripts and culture'),
            ('media',
             'Specificaitons related to audio, video and captions and other Web Media related items'),
            ('performance',
             'Specifications to measure and improve aspects of application performance of user agent features and API'),
            ('privacy',
             'Specifications aiming at improving support for user privacy on the Web'),
            ('protocol', 'Defining the different protocols used on the Web'),
            ('security',
             'Provides technical and policy mechanisms to improve security and enable secure cross-site communications for applications on the Web'),
            ('wot',
             'Provides interoperability across Internet of Things (IoT) Platforms and application domains'),
            ('xml',
             'Specifications defining the Extensible Markup Language (XML) and its extensions'))
formats = 'http://www.w3.org/ns/formats/'
FORMAT_URIS = (('json_ld', 'http://www.w3.org/ns/formats/JSON-LD'),
               ('ld_patch', 'http://www.w3.org/ns/formats/LD_Patch'),
               ('microdata', 'http://www.w3.org/ns/formats/microdata'),
               ('n3', 'http://www.w3.org/ns/formats/N3'),
               ('n_quads', 'http://www.w3.org/ns/formats/N-Quads'),
               ('n_triples', 'http://www.w3.org/ns/formats/N-Triples'),
               ('owl_functional', 'http://www.w3.org/ns/formats/OWL_Functional'),
               ('owl_manchester', 'http://www.w3.org/ns/formats/OWL_Manchester'),
               ('owl_xml', 'http://www.w3.org/ns/formats/OWL_XML'),
               ('powder', 'http://www.w3.org/ns/formats/POWDER'),
               ('powder_s', 'http://www.w3.org/ns/formats/POWDER-S'),
               ('prov_n', 'http://www.w3.org/ns/formats/PROV-N'),
               ('prov_xml', 'http://www.w3.org/ns/formats/PROV-XML'),
               ('rdf_json', 'http://www.w3.org/ns/formats/RDF_JSON'),
               ('rdf_xml', 'http://www.w3.org/ns/formats/RDF_XML'),
               ('rdfa', 'http://www.w3.org/ns/formats/RDFa'),
               ('rif_xml', 'http://www.w3.org/ns/formats/RIF_XML'),
               ('sparql_results_csv', 'http://www.w3.org/ns/formats/SPARQL_Results_CSV'),
               ('sparql_results_json', 'http://www.w3.org/ns/formats/SPARQL_Results_JSON'),
               ('sparql_results_tsv', 'http://www.w3.org/ns/formats/SPARQL_Results_TSV'),
               ('sparql_results_xml', 'http://www.w3.org/ns/formats/SPARQL_Results_XML'),
               ('trig', 'http://www.w3.org/ns/formats/TriG'),
               ('turtle', 'http://www.w3.org/ns/formats/Turtle'))

# html-glossary-to-rdf-schema.xsl
# trdoc-data.xsl
# rdfize.xsl
# spec.xsl



#"http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd"
ov="http://open.vocab.org/terms/"



class dbpedia_mappings:
    maps = "http://mappings.dbpedia.org"
    src = '/opensearch_desc.php'
    mg = '/index.php/Mapping_Guide'
    ext = '/index.php/Use_the_DBpedia_Extraction_Framework'
    domains = "http://mappings.dbpedia.org/validation/index.html"
    com = '/index.php/Mapping_commons'
    ont_prop = "http://mappings.dbpedia.org/index.php?title=Special:AllPages&amp;namespace=202"
    ont_data ="http://mappings.dbpedia.org/index.php?title=Special:AllPages&amp;namespace=206"
    ont_cl = "http://mappings.dbpedia.org/index.php?title=Special:AllPages&amp;namespace=200"
    

class dbpedia:
    """
    http://dbpedia.org/datatype/
    
    /describe/?uri=http://dbpedia.org/datatype/
    'http://osde.demo.openlinksw.com/#/editor?uri=http://dbpedia.org/sparql?default-graph-uri=http://dbpedia.org&query=DESCRIBE <http://dbpedia.org/datatype/>&format=text/turtle&amp;view=statements'
    
    format=text/csv", format=rdf
    format=application/json-ld
    format=text/x-html-script-turtle
    format=text/x-html-script-ld+json
    http://dbpedia.org/sparql?default-graph-uri=http://dbpedia.org&amp;query=DESCRIBE <http://dbpedia.org/datatype/>&amp;format=application/microdata+json
    http://dbpedia.org/sparql?default-graph-uri=http://dbpedia.org&amp;query=DESCRIBE <http://dbpedia.org/datatype/>&amp;format=text/x-html-script-ld+json
    """
    downloads = "http://dbpedia.org/downloads"
    rdfs = 'http://www.w3.org/2000/01/rdf-schema#'
    og = 'https://ogp.me/ns#'
    dct = 'http://purl.org/dc/terms/'
    dbd = 'http://dbpedia.org/datatype/'
    dbp = 'http://dbpedia.org/property/'
    dbo = 'http://dbpedia.org/ontology/'
    dbr = 'http://dbpedia.org/resource/'
    dbt = "http://dbpedia.org/resource/Template:"
    cls = "http://dbpedia.org/resource/classes#"
    vo = "http://purl.org/vocommons/voaf#Vocabulary"
    defs = "http://dbpedia.org/ontology/data/definitions.ttl"
    oo = "http://wiki.dbpedia.org/Ontology"
    
    ttl = 'http://dbpedia.org/data3/.ttl'
    bif = "http://www.openlinksw.com/schemas/bif#"
    linkeddata = "http://linkeddata.org/"
    od = "https://opendefinition.org/"
    b3s = "http://b3s.openlinksw.com/"
    atom = "http://atomowl.org/ontologies/atomrdf#"
    admin = "http://webns.net/mvcb/"
    address = "http://schemas.talis.com/2005/address/schema#"
    a = "http://www.w3.org/2005/Atom"
    db_commons = 'http://commons.dbpedia.org/resource/'
    cc= "http://web.resource.org/cc/"
    cb = "http://www.crunchbase.com/"
    c = "http://www.w3.org/2002/12/cal/icaltzd#"
    dawg = "http://www.w3.org/2001/sw/DataAccess/tests/test-dawg#"
    cvbase = "http://purl.org/captsolo/resume-rdf/0.2/base#"
    cv = "http://purl.org/captsolo/resume-rdf/0.2/cv#"
    content = "http://purl.org/rss/1.0/modules/content/"
    dbc = "http://dbpedia.org/resource/Category:"
    d_war = 'http://war.dbpedia.org/resource/'
    exif = "http://www.w3.org/2003/12/exif/ns/"
    wikidata = "http://wikidata.dbpedia.org/resource/"
    fn = "http://www.w3.org/2005/xpath-functions/#"
    freebase = "http://rdf.freebase.com/ns/"
    foaf = "http://xmlns.com/foaf/0.1/"
    gml = "http://www.opengis.net/gml"
    gold = "http://purl.org/linguistics/gold/"
    hlisting = "http://www.openlinksw.com/schemas/hlisting/"
    hrev = "http://purl.org/stuff/hrev#"
    ical = "http://www.w3.org/2002/12/cal/ical#"
    ir = "http://web-semantics.org/ns/image-regions"
    link = "http://www.xbrl.org/2003/linkbase"
    ldp = "http://www.w3.org/ns/ldp#"
    lod = "http://lod.openlinksw.com/"
    math = "http://www.w3.org/2000/10/swap/math#"
    mesh = "http://purl.org/commons/record/mesh/"
    meta = "urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    oo = "urn:oasis:names:tc:opendocument:xmlns:meta:1.0:"
    mf = "http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#"
    mo = "http://purl.org/ontology/mo/"
    mql = "http://www.freebase.com/"
    nfo = "http://www.semanticdesktop.org/ontologies/nfo/#"
    ng = "http://www.openlinksw.com/schemas/ning#"
    oai = "http://www.openarchives.org/OAI/2.0/"
    oai_dc = "http://www.openarchives.org/OAI/2.0/oai_dc/"
    obo = "http://www.geneontology.org/formats/oboInOwl#"
    opensearch = "http://a9.com/-/spec/opensearchrss/1.0/"
    opencyc = "http://sw.opencyc.org/concept/"
    opl = "http://www.openlinksw.com/schema/attribution#"
    opl_xbrl = "http://www.openlinksw.com/schemas/xbrl/"
    oplweb = "http://www.openlinksw.com/schemas/oplweb#"
    ore = "http://www.openarchives.org/ore/terms/"
    ov = "http://open.vocab.org/terms/"
    prov = "http://www.w3.org/ns/prov#"
    rdfdf = "http://www.openlinksw.com/virtrdf-data-formats#"
    rev = "http://purl.org/stuff/rev#"
    sc = "http://purl.org/science/owl/sciencecommons/"
    scovo = "http://purl.org/NET/scovo#"
    sd = "http://www.w3.org/ns/sparql-service-description#"
    sh = "http://www.w3.org/ns/shacl#"
    shsh = "http://www.w3.org/ns/shacl-shacl#"
    sioc = "http://rdfs.org/sioc/ns#"
    sioct = "http://rdfs.org/sioc/types#"
    slash = "http://purl.org/rss/1.0/modules/slash/"
    sp = "http://spinrdf.org/sp#"
    spin = "http://spinrdf.org/spin#"
    spl = "http://spinrdf.org/spl#"
    sql = "http://www.openlinksw.com/schemas/sql#"
    stat = "http://www.w3.org/ns/posix/stat#"
    twfy = "http://www.openlinksw.com/schemas/twfy#"
    umbel = "http://umbel.org/umbel#"
    units = "http://dbpedia.org/units/"
    v = "http://www.openlinksw.com/xsltext/"
    vcard = "http://www.w3.org/2001/vcard-rdf/3.0#"
    vcard2006 = "http://www.w3.org/2006/vcard/ns#"
    vi =    "http://www.openlinksw.com/virtuoso/xslt/"
    virt =  "http://www.openlinksw.com/virtuoso/xslt"
    virtrdf = "http://www.openlinksw.com/schemas/virtrdf#"
    wf = "http://www.w3.org/2005/01/wf/flow#"
    wfw = "http://wellformedweb.org/CommentAPI/"
    wikidata = "http://www.wikidata.org/entity/"
    wikipedia_en = "http://en.wikipedia.org/wiki/"
    xf = "http://www.w3.org/2004/07/xpath-functions"
    xhtml = "http://www.w3.org/1999/xhtml"
    xhv = "http://www.w3.org/1999/xhtml/vocab#"
    xi = "http://www.xbrl.org/2003/instance"
    xml = "http://www.w3.org/XML/1998/namespace"
    xsd = "http://www.w3.org/2001/XMLSchema#"
    xsl10 = "http://www.w3.org/XSL/Transform/1.0"
    xsl1999 = "http://www.w3.org/1999/XSL/Transform"
    xslwd = "http://www.w3.org/TR/WD-xsl"
    yago = "http://dbpedia.org/class/yago/"
    yago_res = "http://yago-knowledge.org/resource/"
    zem = "http://s.zemanta.com/ns#"
    
    
"""
bibo: 	http://purl.org/ontology/bibo/
cc: 	http://creativecommons.org/ns#
dc: 	http://purl.org/dc/terms/
ex: 	http://example.org/
foaf: 	http://xmlns.com/foaf/0.1/
owl: 	http://www.w3.org/2002/07/owl#
rdf: 	http://www.w3.org/1999/02/22-rdf-syntax-ns#
rdfa: 	http://www.w3.org/ns/rdfa#
rdfs: 	http://www.w3.org/2000/01/rdf-schema#
xhv: 	http://www.w3.org/1999/xhtml/vocab#
xsd: 	http://www.w3.org/2001/XMLSchema#"""

simple = '''
dcat             https://w3c.github.io/dxwg/dcat/
http://www.w3.org/ns/dcat#themeTaxonomy
https://github.com/w3c/dxwg/wiki/Cataloguing-data-services
https://github.com/w3c/dxwg/tree/gh-pages/dcat/examples
https://w3c.github.io/dxwg/dcat/examples/vocab-dcat-3/compress-and-package.ttl

duv_bp           https://www.w3.org/TR/vocab-duv/
dow_bp           https://www.w3.org/TR/dwbp/


http://www.iana.org/assignments/media-types/text/csv
http://publications.europa.eu/resource/authority/file-type/TAR
http://www.iana.org/assignments/media-types/application/gzip
"https://www.iana.org/assignments/provisional-standard-media-types"
"https://www.iana.org/assignments/media-type-sub-parameters"
"https://www.iana.org/assignments/media-types-parameters"
https://www.iana.org/assignments/media-types/media-types.xml
https://www.iana.org/assignments/media-types/media-types.xhtml
https://www.iana.org/assignments/media-types/media-types.txt
https://www.iana.org/assignments/media-types/application.csv
https://www.iana.org/assignments/media-types/audio.csv
https://www.iana.org/assignments/media-types/font.csv
https://www.iana.org/assignments/media-types/image.csv
https://www.iana.org/assignments/media-types/message.csv
https://www.iana.org/assignments/media-types/model.csv
https://www.iana.org/assignments/media-types/multipart.csv
https://www.iana.org/assignments/media-types/text.csv
https://www.iana.org/assignments/media-types/video.csv
#".provn"

import html
html.unescape(text)




pending          http://pending.schema.org/
dc               http://purl.org/dc/elements/1.1/
dcterms          http://purl.org/dc/terms/
vann             http://purl.org/vocab/vann/
schema           http://schema.org/

                 /explorer/datasets/data_at_a_glance/
                 /explorer/datasets/articles/
                 /explorer/datasets/books/
                 /explorer/datasets/persons/
                 /explorer/datasets/ontology/
                 /explorer/releases/
                 https://scigraph.springernature.com:443/explorer/downloads/
                 https://sn-scigraph.figshare.com
                 /explorer/search?q=Semantic Web
                 
                 /resource?u=http://www.w3.org/2002/07/owl#Ontology
                 
                 onto_core
                 http://scigraph.springernature.com/ontologies/core/.json
                 http://scigraph.springernature.com/ontologies/core/.nt
                 http://scigraph.springernature.com/ontologies/core/.ttl
                 http://scigraph.springernature.com/ontologies/core/.xml
                 #jsonld,#ntriples,#ttl,#rdfxml
                 
                 curl -H 'Accept: application/ld+json' 'https://scigraph.springernature.com/ontologies/core/'
                 curl -H 'Accept: application/n-triples' 'https://scigraph.springernature.com/ontologies/core/'
                 curl -H 'Accept: text/turtle' 'https://scigraph.springernature.com/ontologies/core/'
                 curl -H 'Accept: application/rdf+xml' 'https://scigraph.springernature.com/ontologies/core/'
                 
                 http://scigraph.springernature.com/ontologies/core/.json.schema
                 https://json-ld.org/playground/#startTab=tab-expanded&json-ld=http://scigraph.springernature.com/ontologies/core/.json
                 https://springernature.github.io/scigraph/jsonld/sgcontext.json
                 
                 
                 https://www.springernature.com/scigraph
                 https://dev.springernature.com/adding-constraints
sg               http://scigraph.springernature.com/
sgo              http://scigraph.springernature.com/ontologies/core/
sgo-pmc          http://scigraph.springernature.com/ontologies/product-market-codes/
vivo             http://vivoweb.org/ontology/core#
grid_institutes  http://www.grid.ac/institutes/
grid             http://www.grid.ac/ontology/
geo              http://www.opengis.net/ont/geosparql#
rdf              http://www.w3.org/1999/02/22-rdf-syntax-ns#
rdfs             http://www.w3.org/2000/01/rdf-schema#
xsd              http://www.w3.org/2001/XMLSchema#
owl              http://www.w3.org/2002/07/owl#
geo-pos          http://www.w3.org/2003/01/geo/wgs84_pos#
skos             http://www.w3.org/2004/02/skos/core#
skosxl           http://www.w3.org/2008/05/skos-xl#
foaf             http://xmlns.com/foaf/0.1/
ctx              https://springernature.github.io/scigraph/jsonld/sgcontext.json
gold             http://purl.org/linguistics/gold/
bibliography     http://www.linguistics-ontology.org/bibliography/bibliography.owl


articles https://raw.githubusercontent.com/figshare/user_documentation/master/swagger_documentation/documentation/models/articles.json
coll https://raw.githubusercontent.com/figshare/user_documentation/master/swagger_documentation/documentation/models/collections.json
cio             https://raw.githubusercontent.com/micheldumontier/semanticscience/master/ontology/sio/release/sio-release.owl

registry_schema https://raw.githubusercontent.com/OBOFoundry/OBOFoundry.github.io/master/util/schema/registry_schema.json

ssom_jsonld     https://raw.githubusercontent.com/mapping-commons/sssom/master/sssom/jsonld/sssom.context.jsonld


csvw            http://www.w3.org/ns/csvw.ttl
				http://www.w3.org/ns/csvw#
				
				http://www.w3.org/ns/dqv
				http://www.w3.org/ns/dqv.ttl
				http://www.w3.org/ns/dqv.rdf
				http://www.w3.org/ns/dqv.jsonld
				
				https://www.w3.org/TR/vocab-dqv
				https://www.w3.org/TR/vocab-duv
				http://www.w3.org/ns/ma-ont.ttl
				http://www.w3.org/2007/rif#
				http://www.w3.org/1999/xhtml/vocab#
				http://rdfs.org/sioc/ns#  http://rdfs.org/sioc/spec

rfc_index       https://www.rfc-editor.org/rfc-index.xml

files           /Users/kristen/Desktop/ontologies

rfc             https://xml2rfc.tools.ietf.org/public/rfc/bibxml/reference.RFC.4880.xml

onts            https://raw.githubusercontent.com/OBOFoundry/OBOFoundry.github.io/master/registry/ontologies.yml

search_help = https://w3c.github.io/tr-pages/help.html

http://www.w3.org/ns/prov.xsd
http://www.w3.org/ns/prov-dictionary.xsd
http://www.w3.org/ns/prov-links.xsd
http://www.w3.org/ns/prov-core.xsd




'''



'''
import skosify
from skosify.config import config, Config



import skosprovider
from skosprovider.skos import filter_labels_by_language, dict_to_source, dict_to_note,  dict_to_label, Collection, Concept, ConceptScheme, Source
from skosprovider.registry import Registry
from skosprovider.providers import VocabularyProvider, MemoryProvider, DictionaryProvider, SimpleCsvProvider
from skosprovider.utils import dict_dumper
from skosprovider.uri import UriGenerator, UriPatternGenerator, DefaultUrnGenerator, DefaultConceptSchemeUrnGenerator, TypedUrnGenerator

pub = 'http://pub.tenforce.com/schemas/iso25964/skos-thes/' == 'http://purl.org/iso25964/skos-thes'


vocab_namespace = "http://www.w3.org/2004/02/skos/core"
skos_guide =    "https://www.w3.org/TR/swbp-skos-core-guide/"
skos_map =      "https://www.w3.org/2004/02/skos/mapping/spec/"
sem_web_wiki = 'https://www.w3.org/2001/sw/wiki/Main_Page'
skos_list = "https://www.w3.org/TR/?tag=data"
import_large = "https://github.com/INCATools/ontology-development-kit/blob/master/docs/DealWithLargeOntologies.md"

specref = 'https://api.specref.org/bibrefs'

requests.models.Request = Request
equests.models.PreparedRequest
requests.adapters.HTTPAdapter
requests.utils.requote_uri
requests.utils.get_environ_proxies
requests.utils.get_netrc_auth
requests.utils.rewind_body
requests.sessions.merge_setting
requests.sessions.SessionRedirectMixin


http://docs.oasis-open.org/docbook/specs/
http://docs.oasis-open.org/docbook/specs/bibliography.xml
http://docs.oasis-open.org/docbook/specs/media-type/
http://docs.oasis-open.org/docbook/specs/media-type/draft-walsh-app-docbook-xml-00.html
http://docs.oasis-open.org/docbook/specs/media-type/draft-walsh-app-docbook-xml-00.txt
http://docs.oasis-open.org/docbook/specs/index.xml


http://docs.oasis-open.org/docbook/specs/docbook-4.5-spec.xml
http://docs.oasis-open.org/docbook/specs/docbook-4.5-spec.html
http://docs.oasis-open.org/docbook/xml/5.0/catalog.xml
http://www.oasis-open.org/docbook/xsd/4.4/htmltblx.xsd
http://www.oasis-open.org/docbook/xsd/4.4/dbhierx.xsd
https://www.oasis-open.org/committees/entity/spec.html


The first quoted string after PUBLIC is the DTD's PUBLIC identifier, and the second quoted string is the SYSTEM identifier. In this case, the SYSTEM identifier is a full URL to the OASIS website.


'''
'https://datatracker.ietf.org/feed/document-changes/draft-ietf-poised95-std-proc-3/',
'https://www.ietf.org/lib/dt/8.0.0/ietf/js/ietf.js',
'https://datatracker.ietf.org#content',
'https://datatracker.ietf.org/program/',
'https://datatracker.ietf.org/rg/',
'https://datatracker.ietf.org/adm/',
'https://datatracker.ietf.org/doc/recent',
'https://datatracker.ietf.org/doc/search',
'https://datatracker.ietf.org/ipr/',
'https://datatracker.ietf.org/doc/downref/',
'https://datatracker.ietf.org/stats/',
'https://datatracker.ietf.org/group/edu/materials/',
'https://datatracker.ietf.org/api/',
'https://datatracker.ietf.org/release/',
'https://datatracker.ietf.org/doc/rfc2026/',
'https://datatracker.ietf.org/doc/rfc2026/writeup/',
'https://datatracker.ietf.org/doc/rfc2026/email/',
'https://datatracker.ietf.org/doc/rfc2026/history/',
'https://www.rfc-editor.org/rfc/pdfrfc/rfc2026.txt.pdf',
'https://datatracker.ietf.org/doc/rfc2026/bibtex/',
'https://datatracker.ietf.org/doc/rfc2026/references/',
'https://www.ietf.org/tools/idnits?url=https://www.ietf.org/archive/id/draft-ietf-poised95-std-proc-3-06.txt',
'https://www.ietf.org/lib/dt/sprint/ietf_utf8.sql.gz'
#"https://www.rfc-editor.org/errata_search.php?rfc=2026"
_ids = "https://www.ietf.org/tools/idnits?url=https://www.ietf.org/archive/id/draft-ietf-poised95-std-proc-3-06.txt"
#"/ipr/search/?submit=draft&amp;id=draft-ietf-poised95-std-proc-3"
refs = "/doc/rfc2026/references/", "/doc/rfc2026/referencedby/", "/doc/rfc2026/bibtex/", "/doc/html/rfc2026", \
       "https://www.rfc-editor.org/rfc/rfc2026.html",

DATA_API =  'https://datatracker.ietf.org/api/v1/'
GROUP = 'https://datatracker.ietf.org/api/v1/group/group/'
#https://datatracker.ietf.org/api/v1/person/person/?name__startswith=Dr.%20&format=json
#https://datatracker.ietf.org/api/v1/doc/state/?type=charter&format=json
#https://datatracker.ietf.org/doc/draft-ietf-poised95-std-proc-3/doc.json

DOC =       'https://datatracker.ietf.org/api/v1/doc/document/'
#https://datatracker.ietf.org/api/v1/doc/document/?name=draft-ietf-eppext-keyrelay
#'https://datatracker.ietf.org/api/v1/doc/document/?limit=0&name__contains=-v6ops-&states__type__slug__in=draft-rfceditor'
#states__type__slug__in=draft
#'https://datatracker.ietf.org/api/v1/doc/state/?format=json&limit=0&type__slug__in=draft-rfceditor'
#'https://datatracker.ietf.org/api/v1/doc/state/?format=json&limit=0&type__slug__in=draft-iesg'
#'https://datatracker.ietf.org/api/v1/doc/state/?format=json&limit=0&type__slug__in=draft-stream-ietf'
#'https://datatracker.ietf.org/api/v1/doc/document/?limit=0&name__contains=-v6ops-'
#'https://datatracker.ietf.org/api/v1/doc/document/?limit=0&name__contains=-v6ops-&states__type__slug__in=draft-rfceditor'
#https://datatracker.ietf.org/api/v1/doc/document/?limit=0&name__contains=-v6ops-&states__type__slug__in=draft-iesg
DT_SUBM = ' https://datatracker.ietf.org/submit/'
IDS = ' https://www.ietf.org/ietf/1id-abstracts.txt'
ABBREV = 'https://www.rfc-editor.org/materials/abbrev.expansion.txt'
BIBS = 'https://www.rfc-editor.org/refs/bibxml/'
STD = 'https://xml2rfc.tools.ietf.org/public/rfc/bibxml-rfcsubseries/'
STATUS_MEMO = 'https://www.rfc-editor.org/materials/status-memos.txt'
BCP = 'https://www.rfc-editor.org/search/rfc_search_detail.php?sortkey=Number&sorting=DESC&page=All&pubstatus%5B%5D=Best%20Current%20Practice'
EP = 'http://www.essepuntato.it/lode/owlapi/http://www.w3.org/2008/05/skos-xl'

labs = "https://labs.w3.org/repo-manager/repos"
    #createMemoryHistory
owl2xml="http://www.w3.org/2006/12/owl2-xml#"
vs="http://www.w3.org/2003/06/sw-vocab-status/ns#"
ontolex="http://www.w3.org/ns/lemon/ontolex#"
lemon_all = 'http://www.w3.org/ns/lemon/all'
lenon_onto = 'http://www.w3.org/ns/lemon/ontolex'
lime =      'http://www.w3.org/ns/lemon/lime#' #The LInguistic MEtadata
vartrans =  'http://www.w3.org/ns/lemon/vartrans'
decomp =     'http://www.w3.org/ns/lemon/decomp'
synsem = 'http://www.w3.org/ns/lemon/synsem'
ccr = 'https://openskos.meertens.knaw.nl/ccr/browser/'
olia = 'http://purl.org/olia/'
iso = 'http://www.isocat.org'
LMF = 'http://www.lexicalmarkupframework.org'
comm_ol = 'https://www.w3.org/community/ontolex/'
lexicog = 'https://www.w3.org/2019/09/lexicog/'
'https://github.com/cimiano/ontolex'

#lime:lexicalizationModel <http://www.w3.org/2008/05/skos-xl>
#lime:referenceDataset :Agrovoc ;
ontolex = 'https://www.w3.org/2016/05/ontolex/#metadata-lime' #ontolex:ConceptSet
lexinfo = 'http://lexinfo.net/ontology/2.0/lexinfo'
Agrovoc = 'http://aims.fao.org/aos/agrovoc/void.ttl#'
void = 'http://rdfs.org/ns/void#'
rc = 'https://w3id.org/ro/crate/1.1/context'
#ro-crate-preview.html
#ro-crate-metadata.json
ctd = 'https://www.researchobject.org/ro-crate/1.1/context.jsonld'

class w3c:
    """
    'https://raw.githubusercontent.com/w3c/w3c.github.io/main/w3c.json-schema.json'
    id = https://w3c.github.io/w3cjson-schema.json
    
    """
    pass


class ontologydesignpatterns:
    """
    
    http://www.ontologydesignpatterns.org/cp/owl/collectionentity.owl
	http://www.ontologydesignpatterns.org/cp/owl/classification.owl
	http://www.ontologydesignpatterns.org/cp/owl/place.owl
	http://www.ontologydesignpatterns.org/cp/owl/timeindexedsituation.owl
	http://www.ontologydesignpatterns.org/cp/owl/situation.owl
	www.ontologydesignpatterns.org
	
    """
    ODP = 'http://ontologydesignpatterns.org/wiki/Submissions:Faceted_Classification_Scheme'
    _base = 'www.ontologydesignpatterns.org'
    sc = 'http://www.ontologydesignpatterns.org/schemas'
    LMM = 'http://ontologydesignpatterns.org/wiki/Ontology:LMM'
    cpas= "http://www.ontologydesignpatterns.org/schemas/cpannotationschema.owl#"
    dul = 'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#'
    _dul = 'http://www.ontologydesignpatterns.org/ont/dul/ontopic.owl#'

class dbpedia:
    dbp = 'http://dbpedia.org/property/'
    dbo = 'http://dbpedia.org/ontology/'
    dbr = 'http://dbpedia.org/resource/'
    defs =      'http://dbpedia.org/ontology/data/definitions.ttl'
    ontprop =   'http://mappings.dbpedia.org/index.php/OntologyProperty:'
    
    
class stylesheet:
    rdfs2html = 'http://www.w3.org/2002/06/rdfs2html'
    r2h =  'http://www.w3.org/2002/06/rdfs2html.xsl'
    rcs = 'http://www.w3.org/2001/03swell/rcs#'
    style = "http://www.w3.org/StyleSheets/base.css"
    
class Glossary:
    """
    'http://www.w3.org/2000/06/webdata/xslt?
        xmlfile=http://www.w3.org/1999/02/22-rdf-syntax-ns&
        xslfile=http://dev.w3.org/cvsweb/~checkout~/2004/rdfs2html/rdfs2html.xsl?rev=1.1'
    
    """
    SUBGLOSSARY  = ('All',
                    'webarch.rdf',
                    'ATAG10.rdf',
                    'CSS2.rdf',
                    'CCPP-struct-vocab.rdf',
                    'DOM-Level-2-Traversal-Range.rdf',
                    'DOM-Level-2-Events.rdf',
                    'REC-xml.rdf',
                    'xml11.rdf',
                    'weaving.rdf',
                    'DOM-Level-2-HTML.rdf',
                    'di-gloss.rdf',
                    'w3c-jargon.rdf',
                    'hypertext-terms.rdf',
                    'rfc2616-sec1.rdf',
                    'MathML2.rdf',
                    'xhtml-modularization.rdf',
                    'REC-xml-names.rdf',
                    'xml-names11.rdf',
                    'owl-guide.rdf',
                    'PNG.rdf',
                    'qaframe-spec.rdf',
                    'rdf-mt.rdf',
                    'charreq.rdf',
                    'rdf-syntax.rdf',
                    'ruby.rdf',
                    'soap12-part1.rdf',
                    'speech-synthesis.rdf',
                    'P3P.rdf',
                    'uuag10.rdf',
                    'voicexml20.rdf',
                    'qa-glossary.rdf',
                    'WCA-terms.rdf',
                    'wcag10.rdf',
                    'ws-gloss.rdf',
                    'Process.rdf',
                    'xforms.rdf',
                    'xhtml1.rdf',
                    'xinclude.rdf',
                    'xkms2-req',
                    'xlink.rdf',
                    'xpath.rdf',
                    'xpath20',
                    'xmlschema-2.rdf',
                    'xptr-framework.rdf',
                    'xpath-datamodel',
                    'xquery',
                    'xslt20')
    _ns =       'http://www.w3.org/2003/glossary/'
    _base =     'http://www.w3.org/2003/03/glossary-project/'
    schema =    'http://www.w3.org/2003/03/glossary-project/schema#'
    XSLT='http://www.w3.org/2001/05/xslt'
    webdata = "http://www.w3.org/2000/06/webdata/xslt"
    cwm = 'http://www.w3.org/2000/10/swap/doc/cwm'
    
        #xslfile = "http://dev.w3.org/cvsweb/~checkout~/2004/rdfs2html/rdfs2html.xsl?rev=1.1"
    'http://www.w3.org/People/Dom/'
    'http://dev.w3.org/cvsweb/2004/rdfs2html/rdfs2html.xsl'
    RDF = 'http://www.w3.org/2003/03/glossary-project/schema.rdf'
    rdfs2html = 'http://www.w3.org/2002/06/rdfs2html'
    r2h =       'http://www.w3.org/2002/06/rdfs2html.xsl'
    #http://www.w3.org/2002/06/rdfs2html.xsl
    spec = 'http://www.w3.org/2003/03/glossary-project/xmlspec-glossary-to-rdf-schema.xsl'
    #http://www.w3.org/2003/03/glossary-project/glossary-util.xsl
    #http://www.w3.org/2003/03/glossary-project/rdfize.xsl
    'http://www.w3.org/2003/03/glossary-project/xmlspec-trdoc-data.xsl'
    'http://www.w3.org/QA/glossary'
    wai = "http://www.w3.org/WAI/GL/Glossary/printable"
    rdfthes = "http://www.w3.org/2001/sw/Europe/reports/thes/rdfthes.html"
    "http://www.w3.org/People/Berners-Lee/Weaving/glossary.html"
    analysis = 'http://www.w3.org/2003/03/glossary-project/analysis'
    terms = "http://www.w3.org/Architecture/Terms.html"
    ont = "http://www.daml.org/2001/03/daml+oil#"
    rcs = "http://www.w3.org/2001/03swell/rcs#"
    
    #"http://www.w3.org/Terms"
    styles = ("http://www.w3.org/2002/02/style-xsl.css", "http://www.w3.org/StyleSheets/base.css",
              "http://www.w3.org/2002/09/wbs/style.css", "http://www.w3.org/2003/glossary/gloss-style.css",
              'http://www.w3.org/2002/07/01-style-xsl.xsl' #application/xml
              )
    #"http://www.w3.org/WAI/GL/Glossary/printable"
    #http://www.w3.org/WAI/GL/Glossary/"
    #"http://www.w3.org/WAI/GL/WCAG20/"
    
    GLO = "http://www.w3.org/QA/glossary"
    TMF = "http://www.loria.fr/projets/TMF/"
    'daml3: <http://www.daml.org/2001/03/daml+oil#>.'
    'daml1: <http://www.daml.org/2000/10/daml-ont#>.'
    ont="http://www.daml.org/2001/03/daml+oil#"
    rcs = "http://www.w3.org/2001/03swell/rcs.n3"
        #charmod.n3
        #cp.n3, finiteSets.n3, finiteSetsAx.n3, http.n3, mime.n3, rcs.n3, relalg.n3, xrdf.n3, xml.n3, pra.n3, listsAx.n3, Makefile
    
    #http://validator.w3.org
    
    'https://www.w3.org/Help/search'
    
    'http://www.w3.org/2000/10/swap/doc/cwm.html'
    'http://www.w3.org/2000/10/swap/doc/Examples.html'
    
    #http://www.w3.org//2000/01/sw/Overview.html
    
    'http://www.w3.org/2000/10/swap/logic.n3#N3Document'
    'http://www.w3.org/DesignIssues/N3Alternatives.html'
    'http://www.w3.org/DesignIssues/Notation3.html'
    'http://www.w3.org/DesignIssues/RDB-RDF.html'
    #http://www.w3.org/2000/10/swap/doc/Motivation.html,
    #http://dev.w3.org/cvsweb/2000/10/swap/
    #http://dev.w3.org/cvsweb/
    #doc/cwm.html, *.py
    'http://www.w3.org/2000/10/swap/pim/qif2n3.py' #qif -> rdf
    'http://www.w3.org/2000/10/swap/pim/lookout.py'
    'http://www.w3.org/2000/10/swap/tab2n3.py'  # tsv -> rdf
    'http://www.w3.org/2000/10/swap/dbork/dbview.py'
    #http://www.w3.org/2000/10/swap/util/make2n3.py # make
    
    
    #/Help/siteindex
    rfc = '1766'
    Identifier = 'http://www.w3.org/QA/2002/01/Glossary-req'
    gl2sch = 'http://www.w3.org/2001/10/trdoc-data.xsl'
    trdoc = 'http://www.w3.org/2001/11/trdoc-data-ts/'
    org = 'http://www.w3.org/2001/04/roadmap/org#'
    gloss = 'glossary-util.xsl'
    uri = 'http://www.w3.org/2000/07/uri43/uri.xsl'
    pubrules = "https://www.w3.org/Guide/pubrules"
    grps = "https://www.w3.org/2000/04/mem-news/public-groups.rdf"
    #http://www.w3.org/2001/10/trdoc-data.xsl
    #trdoc = '/Users/kristen/Downloads/trdoc-data.xsl'
    #../11/trdoc-data-ts
    #../07/pubrules-form
    #trd="http://www.w3.org/2001/10/trdoc-data.xsl"
        #doc="http://www.w3.org/2000/10/swap/pim/doc#"
        #rec="http://www.w3.org/2001/02pd/rec54#"
        #contact="http://www.w3.org/2000/10/swap/pim/contact#"
    _str = 'http://www.w3.org/2001/10/str-util.xsl'
    
    glu = 'glossary-util.xsl'
    to_rdf =    '/Users/kristen/Downloads/html-glossary-to-rdf-schema.xsl'
    rdfize = '/Users/kristen/Downloads/rdfize.xsl'
    #uri="http://www.w3.org/2000/07/uri43/uri.xsl?template="
    uri = 'http://www.w3.org/2000/07/uri43/uri.xsl' "http://www.ietf.org/rfc/rfc2396.txt"
    
   
class Gloss:
    '''
    /2003/glossary/alpha
    /2003/glossary/keyword queryform
    
        include = 'def'
        index = 'All'
    
    /2003/glossary/keyword/All/?keywords=abstract module
    /2003/glossary/keyword/All/?keywords=access
    /2003/glossary/keyword/All/?keywords=accessibility
    /2003/glossary/keyword/All/?keywords=ACSS%20%28Audio%20cascading%20style%20sheets%29
    /2003/glossary/subglossary
    
    http://www.w3.org/TR/ws-gloss/
    http://www.w3.org/TR/2004/NOTE-ws-gloss-20040211/
    
    //base[@href]|//x:base[@href]'
    
    x = 'http://www.w3.org/1999/xhtml'
    descendant-or-self::*[@id=$id]
    HtmlMixin
    parse
    lxml.html.XHTMLParser
    lxml.html.HTMLParser
    
    from lxml.html.clean import Cleaner, clean, clean_html, autolink, autolink_html, word_break, word_break_html
    
    javascript,comments,
    remove_tags: list
    kill_tags: list
    allow_tags: list
    remove_unknown_tags
    safe_attrs_only: bool
    safe_attrs: set
    add_nofollow: bool
    host_whitelist: list
    
    allow_embedded_url
    clean_html
    add_nofollow = False
    allow_tags = None
    comments = True
    page_structure = True
    scripts = True
    _remove_javascript_link
    clean_html
    
    '''
    
    


err = "https://www.rfc-editor.org/rfc/inline-errata/rfc2026.html"
IRTF = "https://www.irtf.org/"
IANA = "https://www.iana.org/"
IETF = 'https://www.ietf.org/'
IAB = "https://www.iab.org/"
RFC_ED = 'https://www.rfc-editor.org/'
oio = 'http://www.geneontology.org/formats/oboInOwl#'
rfc_json = 'https://datatracker.ietf.org/doc/rfc2026/doc.json'
specref = 'https://api.specref.org/bibrefs'
#?refs=FileAPI,

SWAP = '/Users/kristen/repos/_tmp/swap'
#/Users/kristen/Downloads/xml2rdf.py, xml2infoset.py, variables.py


SUFFIX_FORMAT_MAP = rdflib.util.SUFFIX_FORMAT_MAP


#linkml sssom-py datasets ontobio rdflib _Ontospy mime pyLODE pyrdfa3 specref opencitations
#linkml-registry datapackage-py biocontext ttlfiles FAIR-checker mc2skos linkml-model linkml_models.yaml
#bioregistry OntoWiki fairdatapoint ro-crate-py























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




if __name__ == '__main__':
	print(__file__)
