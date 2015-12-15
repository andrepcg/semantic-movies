# coding=utf-8
import sys
from rdflib import Graph, Namespace, RDF, Literal, BNode, URIRef, XSD
from pprint import pprint
import json
reload(sys)
sys.setdefaultencoding("utf-8")

def getFilmsByGenre(genre):
    namespace="http://www.semanticmovies.pt/#Genre"
    l=[]
    query = "SELECT ?genre ?film WHERE { ?genre :isGenreOf ?b. ?b :hasTitle ?film. FILTER (regex(?a,'http://www.semanticmovies.pt/#Genre')). }"
    #query = "SELECT ?x WHERE { ?x rdf:type owl:NamedIndividual.  }"
    print query
    qres=g.query(query)

    for row in qres:
        l.append({"hasName":str(row[0]),"hasTitle":str(row[1])})


    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]

def getFilmGenre(id):

    l=[]
    query = "SELECT ?film ?genre WHERE {?a :hasGenre ?genre. ?a a :Film. ?a :hasFilmID ?film.  FILTER (regex(?film,'"+id+"')).}"
    print query
    qres=g.query(query)

    for row in qres:
        l.append({"hasTitle":str(row[0]),"hasGenre":str(row[1])})


    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]
def getFilmsByActor(personID):
    l=[]
    query = "SELECT ?id ?actor ?film WHERE {?a :isActorOf ?b. ?a :hasPersonID ?id. ?a :hasName ?actor. ?b :hasTitle ?film. FILTER (regex(?id,'"+personID+"')).}"
    qres=g.query(query)

    for row in qres:
        l.append({"hasName":str(row[1]),"hasTitle":str(row[2])})


    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]


def getAllActors():
    l=[]
    query = "SELECT ?id ?actor  WHERE {?a a :Person. ?a :hasName ?actor. ?a :hasPersonID ?id}"
    qres=g.query(query)

    for row in qres:
        l.append({"hasPersonID":str(row[0]),"hasName":str(row[1])})


    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]


def getAllFilms():
    l=[]
    query = "SELECT ?id ?film  WHERE {?a a :Film. ?a :hasTitle ?film. ?a :hasFilmID ?id.}"
    qres=g.query(query)

    for row in qres:
        l.append({"hasFilmID":str(row[0]),"hasTitle":str(row[1])})


    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]


def getActorInfo(personID):
    l=[]
    query = "SELECT ?birth ?gender ?id WHERE {?a a :Person. ?a :hasBirthDate ?birth. ?a :hasGender ?gender. ?a :hasPersonID ?id. FILTER (regex(?id,'"+personID+"')).}"
    qres=g.query(query)

    for row in qres:
        l.append({"hasBirthDate":str(row[0]),"hasGender":str(row[1])})


    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]


def getActorsByFilm(id):
    l=[]
    query = "SELECT ?id ?actor WHERE {?a :hasActor ?b. ?a :hasFilmID ?id. ?b :hasName ?actor. FILTER (regex(?id,'"+id+"')).}"
    qres=g.query(query)
    for row in qres:
        l.append({"hasFilmID":str(row[0]),"hasName":str(row[1])})

    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]

def getWritersByFilm(id):
    l=[]
    query = "SELECT ?id ?writer WHERE {?a :hasWriter ?b. ?a :hasFilmID ?id. ?b :hasName ?writer. FILTER (regex(?id,'"+id+"')).}"
    qres=g.query(query)
    for row in qres:
        l.append({"hasFilmID":str(row[0]),"hasName":str(row[1])})

    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]

def getDirectorsByFilm(id):
    l=[]
    query = "SELECT ?id ?director WHERE {?a :hasDirector ?b. ?a :hasFilmID ?id. ?b :hasName ?director. FILTER (regex(?id,'"+id+"')).}"
    qres=g.query(query)
    for row in qres:
        l.append({"hasFilmID":str(row[0]),"hasName":str(row[1])})

    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]

def getProducersByFilm(id):
    l=[]
    query = "SELECT ?id ?producer WHERE {?a :hasProducer ?b. ?a :hasFilmID ?id. ?b :hasName ?producer. FILTER (regex(?id,'"+id+"')).}"
    qres=g.query(query)
    for row in qres:
        l.append({"hasFilmID":str(row[0]),"hasName":str(row[1])})

    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]
def getFilmInfo(id):
    l=[]
    query = "SELECT ?id ?title ?runtime ?release_date ?rating ?votes ?tagline ?plot ?poster ?actor WHERE {?a a :Film. ?a :hasFilmID ?id.  ?a :hasTitle ?title. ?a :hasRuntime ?runtime. ?a :hasReleaseDate ?release_date. ?a :hasRating ?rating. ?a :hasVotes ?votes. ?a :hasTagline ?tagline. ?a :hasPlot ?plot. ?a :hasPoster ?poster.  FILTER (regex(?id,'"+id+"')).}"

    qres=g.query(query)
    for row in qres:
        l.append({"hasFilmID":str(row[0]),"hasTitle":str(row[1]),"hasRuntime":str(row[2]),"hasReleaseDate":str(row[3]),"hasRating":str(row[4]),"hasVotes":str(row[5]),"hasTagline":str(row[6]),"hasPlot":str(row[7]),"hasPoster":str(row[8]),"hasActor":str(row[9])})


    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]


def searchFilm(keyword):
    l=[]
    query = "SELECT ?id ?title ?runtime ?release_date ?rating ?votes ?tagline ?plot ?poster WHERE {?a a :Film. ?a :hasFilmID ?id.  ?a :hasTitle ?title. ?a :hasRuntime ?runtime. ?a :hasReleaseDate ?release_date. ?a :hasRating ?rating. ?a :hasVotes ?votes. ?a :hasTagline ?tagline. ?a :hasPlot ?plot. ?a :hasPoster ?poster. FILTER (regex(?title,'.*"+keyword+".*','i')).}"
    qres=g.query(query)
    for row in qres:
        l.append({"hasFilmID":str(row[0]),"hasTitle":str(row[1]),"hasRuntime":str(row[2]),"hasReleaseDate":str(row[3]),"hasRating":str(row[4]),"hasVotes":str(row[5]),"hasTagline":str(row[6]),"hasPlot":str(row[7]),"hasPoster":str(row[8])})


    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]


def searchActor(keyword):
    l = []
    query = "SELECT ?id ?actor  WHERE {?a a :Person. ?a :hasName ?actor. ?a :hasPersonID ?id. FILTER (regex(?actor,'.*"+keyword+".*','i')).}"

    qres=g.query(query)

    for row in qres:
        l.append({"hasPersonID":str(row[0]),"hasName":str(row[1])})


    if len(l) > 1 or len(l) == 0:
        return l
    else:
        return l[0]

g = Graph()

g.parse("populated_movies.ttl",format="n3")

print getAllActors()

print getFilmInfo("tt0120815")

print getFilmsByActor("nm0000199")
print searchFilm("léon")
print getFilmsByGenre("Genre")
print searchActor("dicapr")

print getFilmGenre("tt0120815")

print "\n\n"
print getActorsByFilm("tt0120815")
print getProducersByFilm("tt0120815")
print getDirectorsByFilm("tt0120815")
print getWritersByFilm("tt0120815")
