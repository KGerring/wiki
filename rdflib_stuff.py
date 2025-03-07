__author__ = 'Kristen'


_BFO='ontospy.data.schemas.bfo-1.1.owl'
OWLRules = '/Users/Kristen/Downloads/ordf-0.36/ordf/vocab/n3/owl-rules.n3'
GOLD = '/Users/Kristen/GOLD.owl'
FOAF = '/Users/Kristen/FOAF.xml'
RMRDF = '/Users/Kristen/RMRDF.owl'

GalenRDF = '/Onto/GalenRDF.owl'
RevealMeRDF = '/Onto/RevealMeRDF.owl'
MFOEM = '/Onto/MFOEM.owl'
OWLRules = '/Users/Krten/Downloads/ordf-0.36/ordf/vocab/n3/owl-rules.n3'
GOLD = '/Onto/GOLD.owl'
RevealMeOBO = '/Users/Kristen/RevealMeOBO.owl'
RevealMeOWL = '/Onto/RevealMe1.owl'
Documented = '/Onto/Documented.owl'                     #use labels
FOAF = '/Onto/foaf.rdf'
relationship = '/Onto/relationship.owl'
Fuzzy = '/Onto/Fuzzy.owl'
BFO = '/Onto/BFO.owl'

from FuXi.Horn.HornRules import HornFromN3
import os, pkg_resources

owl_rule_file = pkg_resources.resource_filename("ordf.vocab", os.path.join("n3", "owl-rules.n3"))
owl_rules = HornFromN3(owl_rule_file)
owl_formulae = owl_rules.formulae
owl_formula = [f.formula for f in owl_formulae]
rdfs_rule_file = pkg_resources.resource_filename("ordf.vocab", os.path.join("n3", "rdfs-rules.n3"))
rdfs_rules = HornFromN3(rdfs_rule_file)
rdfs_formulae = rdfs_rules.formulae
rdfs_formulae_n3 = [f.n3() for f in rdfs_formulae]
rdfs_formulae_formula = [f.formula for f in rdfs_formulae]


import rdflib
from rdflib.exceptions import Error, ParserError
from toolz import unique
from collections import defaultdict, Counter
from ontospy.libs.queryHelper import QueryHelper
from rdflib.namespace import *
from rdflib.graph import Graph
from rdflib.term import URIRef
from attrdict import AttrDict as AD
from attrdict.mapping import AttrMap
from operator import itemgetter, attrgetter, methodcaller
from orderedmultidict import omdict

PROPS = \
{
	'AnnotationProperty'        : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#AnnotationProperty'),
	'ObjectProperty'            : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#ObjectProperty'),
	'FunctionalProperty'        : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#FunctionalProperty'),
	'TransitiveProperty'        : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#TransitiveProperty'),
	'InverseFunctionalProperty' : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#InverseFunctionalProperty'),
	'DatatypeProperty'          : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#DatatypeProperty'),
	'AsymmetricProperty'        : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#AsymmetricProperty'),
	'SymmetricProperty'         : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#SymmetricProperty'),
	'OntologyProperty'          : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#OntologyProperty'),
	'ReflexiveProperty'         : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#ReflexiveProperty'),
	'IrreflexiveProperty'       : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#IrreflexiveProperty'),
	'Property'                  : rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'),
}

OBJECT_PROPS = {
	'FunctionalProperty'        : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#FunctionalProperty'),
	'InverseFunctionalProperty' : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#InverseFunctionalProperty'),
	'ObjectProperty'            : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#ObjectProperty'),
	'TransitiveProperty'        : rdflib.term.URIRef('http://www.w3.org/2002/07/owl#TransitiveProperty')
}



['AnnotationProperty','Functional', 'InverseFunctional', 'Transitive', 'Symmetric', 'Asymmetric', 'Reflexive', 'Irreflexive']
iteritems =methodcaller('items')
iterkeys = methodcaller('keys')
itervalues = methodcaller('values')





ace                 = Namespace("http://attempto.ifi.uzh.ch/ace_lexicon#")
bfo                 = Namespace('http://www.ifomis.org/bfo/1.1#')
dc                  = Namespace("http://purl.org/dc/elements/1.1/")
doc                 = Namespace('http://purl.obofoundry.org/obo/iao/d-acts.owl#')
fuzzy               = Namespace('http://www.site.uottawa.ca/~mkhedr/Ontologies/Fuzzy#')
galen               = Namespace('http://www.co-ode.org/ontologies/galen#')
GALEN               = Namespace('http://www.co-ode.org/ontologies/GALEN#')
MF                  = Namespace("http://purl.obolibrary.org/obo/MF#")
MFO                 = Namespace("http://purl.obolibrary.org/obo/MFO#")
mfoem               = Namespace('http://purl.obolibrary.org/obo/MFOEM#')
obo                 = Namespace("http://purl.obolibrary.org/obo/")
owl                 = Namespace('http://www.w3.org/2002/07/owl#')
rel                 = Namespace('http://purl.org/vocab/relationship/')
rm                  = Namespace('http://www.semanticweb.org/RevealMe/ontologies/1#')
snap                = Namespace("http://www.ifomis.org/bfo/1.1/snap#")
span                = Namespace('http://www.ifomis.org/bfo/1.1/span#')


def get_str(entity):
	if entity.__class__.__name__ == 'BNode':
		return entity.toPython()
	elif entity.__class__.__name__ == 'Literal':
		return entity._value
	elif entity.__class__.__name__ == 'URIRef':
		if entity.toPython().__contains__('#'):
			return entity.toPython().rsplit('#')[1]
		else:
			try:
				return os.path.basename(entity)
			except Error:
				return entity.toPython()
	elif entity.__class__.__name__ == 'Class' or 'ObjectProperty':
		if entity.uri.__class__.__name__ == 'URIRef':
			return entity.uri.toPython().rsplit('#')[1]
		else:
			return entity.uri.toPython()
	else:
		return entity

def get_ns(): return {k: v for k, v in locals().items() if isinstance(v, (Namespace, ClosedNamespace))}


def getNSprefix(aURI): return aURI.__str__().replace("#", "").split("/")[-1]


class GraphHelper(Graph):
	def __init__(self, source, uri=None):
		super(Graph, self).__init__()
		self.source = source
		self.rdfgraph = rdflib.Graph()
		self.graphuri	=uri
		self.ontologies = []
		self.classes = []
		self.namespaces = sorted(self.rdfgraph.namespaces())
		self.PROPS =PROPS
		self.properties = []
		self.annotationProperties = []
		self.datatypeProperties = []
		self.functionalProperties = []
		self.inverseFunctionalProperties = []
		self.objectProperties = []
		self.transitiveProperties = []
		self.ontologyProperties = []
#IFP, AP, DP, FP, OP, TP, OnP = set(P.InverseFunctionalProperty), set(P.AnnotationProperty), set(P.DatatypeProperty), set(P.FunctionalProperty), set(P.ObjectProperty), set(P.TransitiveProperty), set(P.OntologyProperty)

		self.__loadRDF(source)


	def __repr__(self):
		return "<GraphHelper Graph ({} triples, {} classes, {} properties) from {}>".format(len(self.rdfgraph), len(self.classes), len(self.properties), self.source)

	def __loadRDF(self, source):
		try:
			self.rdfgraph.parse(source)

			self.rdfgraph.bind("rdf", rdflib.namespace.RDF)
			self.rdfgraph.bind("rdfs", rdflib.namespace.RDFS)
			self.rdfgraph.bind("owl", rdflib.namespace.OWL)
			self.rdfgraph.bind("skos", rdflib.namespace.SKOS)
			self.rdfgraph.bind("galen", rdflib.namespace.Namespace(self.graphuri))
			for prefix, ns in self.namespaces:
				self.rdfgraph.bind(prefix, ns)
			self._load_Properties()
			self._load_All_Properties()
			self._load_Classes()
			self._extractNamespaces()


		except ParserError:
			self.rdfgraph.load(open(source))
			self.rdfgraph.bind("rdf", rdflib.namespace.RDF)
			self.rdfgraph.bind("rdfs", rdflib.namespace.RDFS)
			self.rdfgraph.bind("owl", rdflib.namespace.OWL)
			self.rdfgraph.bind("skos", rdflib.namespace.SKOS)
			self.rdfgraph.bind("galen", rdflib.namespace.Namespace(self.graphuri))
			for prefix, ns in self.namespaces:
				self.rdfgraph.bind(prefix, ns)
			self._load_Properties()
			self._load_All_Properties()
			self._load_Classes()
			self._extractNamespaces()

		print("----------\nLoaded %d triples from <%s>" % (len(self.rdfgraph), self.source))
		print("Classes found...: %d" % len(self.classes))
		print("Properties found: %d" % len(self.properties))
		print("Annotation......: %d" % len(self.annotationProperties))
		print("Datatype........: %d" % len(self.datatypeProperties))
		print("Object..........: %d" % len(self.objectProperties))
		print("Transitive......: %d" % len(self.transitiveProperties))
		print("Functional......: %d" % len(self.functionalProperties))



	def serialize(self, filename=None, rdf_format="turtle"):
		""" Shortcut that outputs the graph """
		if filename is not None:
			return self.rdfgraph.serialize(destination=filename, format=rdf_format)
		else:
			return self.rdfgraph.serialize(format=rdf_format)

	def sparql(self, stringa):
		""" wrapper around a sparql query """
		qres = self.rdfgraph.query(stringa)
		return list(qres)


	def _extractNamespaces(self):
		if self.graphuri not in [y for x,y in self.rdfgraph.namespaces()]:
			prefix = getNSprefix(self.graphuri)
			self.rdfgraph.bind(prefix, rdflib.Namespace(self.graphuri))
		self.namespaces = sorted(self.rdfgraph.namespaces())

	def _load_Properties(self):
		self.properties = []
		for line in list(self.rdfgraph.query( """SELECT ?x ?c WHERE { { { ?x a rdf:Property }  UNION  { ?x a owl:ObjectProperty } UNION  { ?x a owl:DatatypeProperty } UNION  { ?x a owl:AnnotationProperty } } .  ?x a ?c  FILTER(!isBlank(?x) ) . } ORDER BY	?c ?x """)):
			self.properties.append(get_str(line[0]))
			self.properties = sorted(self.properties)

	def getAllPropertiesItems(self): return [(get_str(line[1]), get_str(line[0])) for line in list(self.rdfgraph.query( """SELECT ?x ?c WHERE { { { ?x a rdf:Property }  UNION  { ?x a owl:ObjectProperty } UNION  { ?x a owl:DatatypeProperty } UNION  { ?x a owl:AnnotationProperty } } .  ?x a ?c  FILTER(!isBlank(?x) ) . } ORDER BY	?c ?x """))]

	def getAllProperties(self): return list(self.rdfgraph.query( """SELECT ?x ?c WHERE { { { ?x a rdf:Property }  UNION  { ?x a owl:ObjectProperty } UNION  { ?x a owl:DatatypeProperty } UNION  { ?x a owl:AnnotationProperty } } .  ?x a ?c  FILTER(!isBlank(?x) ) . } ORDER BY	?c ?x """))


	def get_property(self,type):
		properties = self.getAllProperties()
		return sorted([get_str(p[0]) for p in properties if p[1] == self.PROPS[type]])

	def Properties(self):
		Props = {}
		keys = ['DatatypeProperty', 'IrreflexiveProperty', 'FunctionalProperty', 'AsymmetricProperty', 'ObjectProperty',
		        'Property', 'InverseFunctionalProperty', 'OntologyProperty', 'TransitiveProperty', 'ReflexiveProperty',
		        'AnnotationProperty', 'SymmetricProperty']
		for k in keys:
			Props[k] = self.get_property(k)
		return AD(Props)

	def getAnnotationProperties(self):
		return self.get_property('AnnotationProperty')

	def getAsymmetricProperties(self):
		return self.get_property('AsymmetricProperty')

	def getDatatypeProperties(self):
		return self.get_property('DatatypeProperty')

	def getFunctionalProperties(self):
		return self.get_property('FunctionalProperty')

	def getInverseFunctionalProperties(self):
		return self.get_property('InverseFunctionalProperty')

	def getIrreflexiveProperties(self):
		return self.get_property('IrreflexiveProperty')

	def getObjectProperties(self):
		return self.get_property('ObjectProperty')

	def getOntologyProperties(self):
		return self.get_property('OntologyProperty')

	def getReflexiveProperties(self):
		return self.get_property('ReflexiveProperty')

	def getTransitiveProperties(self):
		return self.get_property('TransitiveProperty')



	def _load_Transitive_Properties(self):
		self.transitiveProperties = []
		TP = self.getTransitiveProperties()
		for t in TP:
			self.transitiveProperties.append(t)

	def _load_Datatype_Properties(self):
		self.datatypeProperties = []
		DP = self.getDatatypeProperties()
		for d in DP:
			self.datatypeProperties.append(t)


	def _load_Annotation_Properties(self):
		self.annotationProperties = []
		AP = self.getAnnotationProperties()
		for a in AP:
			self.annotationProperties.append(a)

	def _load_Functional_Properties(self):
		self.functionalProperties = []
		FP = self.getFunctionalProperties()
		for f in FP:
			self.functionalProperties.append(f)

	def _load_Inverse_Functional_Properties(self):
		self.inverseFunctionalProperties = []
		IFP = self.getInverseFunctionalProperties()
		for i in IFP:
			self.inverseFunctionalProperties.append(i)

	def _load_Object_Properties(self):
		self.objectProperties = []
		OP = self.getObjectProperties()
		for o in OP:
			self.objectProperties.append(o)


	def _load_All_Properties(self):
		self.transitiveProperties = []
		self.objectProperties = []
		self.inverseFunctionalProperties = []
		self.datatypeProperties = []
		self.functionalProperties = []
		self.annotationProperties = []
		OP = self.getObjectProperties()
		IFP = self.getInverseFunctionalProperties()
		FP = self.getFunctionalProperties()
		AP = self.getAnnotationProperties()
		TP = self.getTransitiveProperties()
		DP = self.getDatatypeProperties()
		for o in OP:
			self.objectProperties.append(o)
		for i in IFP:
			self.inverseFunctionalProperties.append(i)
		for f in FP:
			self.functionalProperties.append(f)
		for a in AP:
			self.annotationProperties.append(a)
		for t in TP:
			self.transitiveProperties.append(t)
		for d in DP:
			self.datatypeProperties.append(d)

	def PropAllSubs(self,aURI): return [get_str(p[0]) for p in self.rdfgraph.query( """SELECT DISTINCT ?x WHERE { { ?x rdfs:subPropertyOf+ <%s> }  FILTER (!isBlank(?x)) }""" % (aURI))]

	def PropAllSupers(self,aURI): return [get_str(p[0]) for p in self.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { <%s> rdfs:subPropertyOf+ ?x }  FILTER (!isBlank(?x)) }""" % (aURI))]

	def PropDirectSupers(self,aURI): return [get_str(p[0]) for p in self.rdfgraph.query( """SELECT DISTINCT ?x WHERE { { <%s> rdfs:subPropertyOf ?x } FILTER (!isBlank(?x)) } ORDER BY ?x """ % (aURI))]

	def getAllClasses(self): return [q[0] for q in list(self.rdfgraph.query("""SELECT DISTINCT ?x ?c WHERE { { { ?x a owl:Class } union { ?x a rdfs:Class } union { ?x rdfs:subClassOf ?y } union { ?z rdfs:subClassOf ?x } union { ?y rdfs:domain ?x } union { ?y rdfs:range ?x } } . ?x a ?c FILTER( !STRSTARTS(STR(?x), "http://www.w3.org/2002/07/owl") && !STRSTARTS(STR(?x), "http://www.w3.org/1999/02/22-rdf-syntax-ns") && !STRSTARTS(STR(?x), "http://www.w3.org/2000/01/rdf-schema") && !STRSTARTS(STR(?x), "http://www.w3.org/2001/XMLSchema") && !STRSTARTS(STR(?x), "http://www.w3.org/XML/1998/namespace") && (!isBlank(?x)) ) . } ORDER BY  ?x """))]

	def Classes(self): return [get_str(c) for c in self.getAllClasses()]

	def _load_Classes(self):
		self.classes = []
		Classes = self.Classes()
		for C in Classes:
			self.classes.append(C)
			self.classes = sorted(self.classes)

	def PropInfo(self, aURI):
		return AD({'AllSupers': self.PropAllSupers(aURI),
				   'AllSubs': self.PropAllSubs(aURI),
				   'DirectSupers': self.PropDirectSupers(aURI)})

	def ClassAllSupers(self,aURI): return [get_str(c[0]) for c in self.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { <%s> rdfs:subClassOf+ ?x } FILTER (!isBlank(?x))}""" % (aURI))]

	def ClassAllSubs(self,aURI): return [get_str(c[0]) for c in self.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { ?x rdfs:subClassOf+ <%s> } FILTER (!isBlank(?x))}""" % (aURI))]

	def ClassDirectSubs(self,aURI):  return [get_str(c[0]) for c in self.rdfgraph.query("""SELECT DISTINCT ?x WHERE {{ ?x rdfs:subClassOf <%s> } FILTER (!isBlank(?x))}""" % (aURI))]

	def ClassDirectSupers(self,aURI): return [get_str(c[0]) for c in self.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { <%s> rdfs:subClassOf ?x } FILTER (!isBlank(?x))} ORDER BY ?x """ % (aURI))]

	def ClassInfo(self, aURI): return AD({'AllSupers': self.ClassAllSupers(aURI), 'AllSubs': self.ClassAllSubs(aURI), 'DirectSupers': self.ClassDirectSupers(aURI), 'DirectSubs': self.ClassDirectSubs(aURI)})

	def ClassInstances(self,aURI): return list(self.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { ?x rdf:type <%s> } FILTER (!isBlank(?x)) } ORDER BY ?x""" % (aURI)))

	def Triples(self, aURI):
		triples = list(self.rdfgraph.query("""CONSTRUCT {<%s> ?y ?z } WHERE { { <%s> ?y ?z }}""" % (aURI, aURI )))
		results = []
		for t in triples:
			results.append((get_str(t[0]), get_str(t[1]), get_str(t[2])))
		return results

	def getEntities(self):
		P = self.getAnnotationProperties() + self.getAsymmetricProperties() + self.getDatatypeProperties() + self.getFunctionalProperties() + self.getInverseFunctionalProperties() + self.getObjectProperties()
		C = self.Classes()
		E = P + C
		return E

	def getComments(self, aURI):
		results = []
		for r in self.rdfgraph.objects(aURI, RDFS.comment):
			results += [get_str(r)]
		return results

	def getLabel(self, aURI):
		results = []
		for r in self.rdfgraph.objects(aURI, RDFS.label):
			results += [get_str(r)]
		return results

	def getDisjoint(self, aURI):
		results = []
		for r in self.rdfgraph.objects(aURI, OWL.disjointWith):
			results += [get_str(r)]
		if len(results) == 1:
			results = results[0]
		return results

	def getEquivalentClass(self, aURI):
		results = []
		for r in self.rdfgraph.objects(aURI, OWL.equivalentClass):
			results += [get_str(r)]
		if len(results) == 1:
			results = results[0]
		return results

	def getIndividuals(self):
		results = []
		uris = [uri for uri in self.rdfgraph.subjects(RDF.type, OWL.NamedIndividual)]
		for uri in uris:
			results.append(get_str(uri))
		return results

	def get_individual_type(self, aURI):
		type_uris = list(self.rdfgraph.objects(aURI, RDF.type))
		types = [get_str(cls) for cls in type_uris if get_str(cls) in self.Classes()]
		return types

	def getAllTriples(self, aURI):
		results = []
		trip = set(self.rdfgraph.triples((aURI, None, None))) | set(self.rdfgraph.triples((None, aURI, None))) | set(
			self.rdfgraph.triples((None, None, aURI)))
		trip = list(trip)
		for t in trip:
			results.append((get_str(t[0]), get_str(t[1]), get_str(t[2])))
		return results


	def getNSprefix(aURI): return aURI.__str__().replace("#", "").split("/")[-1]


	def base(aURI):     #todo author
		if '#' in aURI:
			return '%s#' % aURI.rsplit('#', 1)[0]
		return '%s/' % aURI.rsplit('/', 1)[0]

	def symbol(aURI):       #todo author
		if '#' in aURI:
			return aURI.rsplit('#', 1)[-1]
		return aURI.rsplit('/', 1)[-1]

	def getValuesForProperty(self, aPropURIRef):
		return list(self.rdfgraph.objects(None, aPropURIRef))













class OWLEntity:

	def __repr__(self): return "<OWL Entity for uri {} >".format(self.uri)
	def __init__(self, uri):
		self.uri = uri
		self.prefix = symbol(uri)
		self.triples = []
		self.parents = []
		self.children = []
		self.graph = rdflib.Graph()


class OWLClass:
	pass

class OWLProperty:
	pass

class OWLIndividual:
	pass

class Axioms:
	pass























'''

from orderedmultidict import omdict
H.getAllProperties()
_prop = []
for line in Prop:
	 _prop.append((get_str(line[1]), get_str(line[0])))
p = omdict(prop)
keys = p.keys()
['AnnotationProperty',
'FunctionalProperty',
'InverseFunctionalProperty',
'ObjectProperty',
'TransitiveProperty']
set_dict = defaultdict(set).fromkeys(p.keys(), set())
set_dict = set_dict.fromkeys(p.keys(), set())


for k,v in prop:
	set_dict[k].add(v)

ROOT = galen.DomainCategory

def make_edge(word):
	node1 = word
	for s in Subs(Namespace('http://www.co-ode.org/ontologies/galen#'+word)):
		D.add_edge(node1, s)


DFE = DFE[0]
IN = omdict(D.in_edges())
OUT = omdict(D.out_edges())



nx.all_pairs_dijkstra_path(G)
nx.single_source_dijkstra_path(G)

networkx.algorithms.ancestors
ancestors

BFS =networkx.algorithms.breadth_first_search
networkx.algorithms.core
networkx.algorithms.depth_first_search
networkx.algorithms.link_prediction
dfs_edges
networkx.algorithms.depth_first_search



G.out_edges()
'''

import re

def underscore(word):
	word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
	word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
	word = word.replace("-", "_")
	return word.lower()

def uncamelize(word):
	word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
	word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
	word = word.replace("-", "_")
	return word.lower().split('_')

def uncamelize_list(lst, get_common=None):
	result = []
	for word in lst:
		word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
		word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
		word = word.replace("-", "_")
		for segment in word.lower().split('_'):
			result.append(segment)
	if get_common is not None:
		cnt = Counter(result)
		return cnt.most_common(get_common)
	else:
		return sorted(result)

def _P(word): return [w for w in P if w.__contains__(word)]
def _C(word): return [w for w in C if w.__contains__(word)]
def _E(word): return [w for w in E if w.__contains__(word)]

def find(word):
	p = _P(word)
	c = _C(word)
	e = _E(word)
	print('Properties: {} \n Classes: {} \n All: {}'.format(p,c,e))


def camelize(string, uppercase_first_letter=True):
	if uppercase_first_letter:
		return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
	else:
		return string[0].lower() + camelize(string)[1:]

def get_most_common_words(lst):
	from collections import Counter
	from nltk.util import flatten





class Dict(AttrMap):
	@property
	def _keys(self): return sorted(self.keys())
	@property
	def _keys_index(self): return dict(enumerate(sorted(self.keys())))

	def _index(self): return {k:{v} for k,v in dict(enumerate(sorted(self.keys()))).items()}
	@property
	def _items(self): return sorted(self.items())
	@property
	def _values(self): return sorted(self.values())
	def sortedkeys(self): return sorted(self.keys())
	def sortedvals(self): return sorted(self.values())
	def sorteditems(self):
		result = []
		if self._mapping:
			for k,v in self._mapping.items():
				temp = []


	def copy(self): return {k:v for k,v in self.items()}

	def valfilter(self, predicate):
		rv = {}
		for k, v in self._items:
			if predicate(v):
				rv[k] = v
		return sorted(rv.keys())

	def keyfilter(self, predicate):
		rv = {}
		for k,v in iteritems(self):
			if predicate(k):
				rv[k] = v
		return sorted(rv.keys())

	def itemfilter(self, predicate):
		rv = {}
		for item in iteritems(self):
			if predicate(item):
				k,v = item
		return sorted(rv.keys())

	def itemmap(self, func):
		return sorted(dict(map(func, iteritems(self))).keys())

	def keymap(self, func):
		return dict(zip(map(func, iterkeys(self)), itervalues(self)))

	def valmap(self, func):
		return dict(zip(iterkeys(self), map(func, itervalues(self))))

	def reverse_dict(self):
		result = {}
		for key in self:
			for val in self[key]:
				if val not in result:
					result[val] = set()
				result[val].add(key)
		return result

	def contains(self, s): return [k for k in self.keys() if k.startswith(s+'_') or k.endswith('_'+s) or k.startswith(s)]
	def getquick(self, key): return itemgetter(key)(self)


def thing(s):
	pass
	def ontology(self): return self.rdfgraph.query("""SELECT DISTINCT ?x WHERE {?x a owl:Ontology}""")


	def entityTriples(self,aURI): return list(Q.rdfgraph.query("""CONSTRUCT {<%s> ?y ?z } WHERE { { <%s> ?y ?z }}""" % (aURI, aURI )))


H=GraphHelper(GalenRDF)
H._GraphHelper__load_All_Properties()
H._GraphHelper__extractNamespaces()
H._load_All_Classes()
H.Triples(galen.Urine)
H.ClassInfo(galen.Urine)


GalenOBO = '/Users/Kristen/GalenOBO.owl'
parser = obo.Parser(fp=open(GalenOBO))

'''
P = MyParser(GalenOBO)
terms = MyParser(GalenOBO).get_terms()
typedefs =MyParser(GalenOBO).get_typedefs()
typedefs_keys = MyParser(GalenOBO).get_typedefs_keys()
terms_keys = MyParser(GalenOBO).get_terms_keys()
rels = MyParser(GalenOBO).get_terms_rels()
rels_keys = sorted(rels.keys())
def get_super(name): return MyParser(GalenOBO).get_super_term(name)
def get_sub(name): return MyParser(GalenOBO).get_sub_term(name)
'''

G = Graph()
G.load(open(GalenRDF))
Q = QueryHelper(G)

######Properties######

'''

TP = get_property('TransitiveProperty')
AP = get_property('AnnotationProperty')
FP = get_property('FunctionalProperty')
IFP = get_property('InverseFunctionalProperty')
OP = get_property('ObjectProperty')
'''


def Property_Info():
	properties = Properties()
	classes = Classes()
	for k in properties.keys():
		print("Property type: {},  length: {}".format(k, len(properties[k])))

def PropAllSubs(aURI): return list(Q.rdfgraph.query( """SELECT DISTINCT ?x WHERE { { ?x rdfs:subPropertyOf+ <%s> }  FILTER (!isBlank(?x)) }""" % (aURI)))
def PropAllSupers(aURI): return list(Q.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { <%s> rdfs:subPropertyOf+ ?x }  FILTER (!isBlank(?x)) }""" % (aURI)))
def PropDirectSupers(aURI): return list(Q.rdfgraph.query( """SELECT DISTINCT ?x WHERE { { <%s> rdfs:subPropertyOf ?x } FILTER (!isBlank(?x)) } ORDER BY ?x """ % (aURI)))

def _PropAllSupers(aURI): return [get_str(p[0]) for p in PropAllSupers(aURI)]
def _PropAllSubs(aURI): return [get_str(p[0]) for p in PropAllSubs(aURI)]
def _PropDirectSupers(aURI): return [get_str(p[0]) for p in PropDirectSupers(aURI)]


def propInfo(aURI): return AD({'AllSupers': _PropAllSupers(aURI), 'AllSubs': _PropAllSubs(aURI), 'DirectSupers': _PropDirectSupers(aURI)})




#####Classes######
def Classes():
	result = {}
	classes = [q[0] for q in Q.getAllClasses()]
	for c in classes:
		result[c.toPython().split('#')[1]] = c
	return AD(result)


def ClassAllSupers(aURI): return list(Q.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { <%s> rdfs:subClassOf+ ?x } FILTER (!isBlank(?x))}""" % (aURI)))
def ClassAllSubs(aURI): return list(Q.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { ?x rdfs:subClassOf+ <%s> } FILTER (!isBlank(?x))}""" % (aURI)))
def ClassDirectSubs(aURI):  return list(Q.rdfgraph.query("""SELECT DISTINCT ?x WHERE {{ ?x rdfs:subClassOf <%s> } FILTER (!isBlank(?x))}""" % (aURI)))
def ClassDirectSupers(aURI): return list(Q.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { <%s> rdfs:subClassOf ?x } FILTER (!isBlank(?x))} ORDER BY ?x """ % (aURI)))






def ClassInstances(aURI): return list(Q.rdfgraph.query("""SELECT DISTINCT ?x WHERE { { ?x rdf:type <%s> } FILTER (!isBlank(?x)) } ORDER BY ?x""" % (aURI)))

def entityTriples(aURI): return list(Q.rdfgraph.query("""CONSTRUCT {<%s> ?y ?z } WHERE { { <%s> ?y ?z }}""" % (aURI, aURI )))
def _entityTriples(aURI):
	triples = entityTriples(aURI)
	results = []
	for t in triples:
		results.append((get_str(t[0]), get_str(t[1]), get_str(t[2])))
	return results







def _rel(word, dic = R):
	rels = dic[word]['relationship']
	result = []
	if len(rels) == 1:
		relA,relB = rels[0].split(' ')
		result.append(relA)
		result.append(relB)
	else:
		for rel in rels:
			relA, relB=rel.split(' ')
			result.append(relA)
			result.append(relB)
	return result




















