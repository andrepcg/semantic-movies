# coding=utf-8
import sys
from rdflib import Graph, Namespace, RDF, Literal, BNode, URIRef, XSD
import json
import random

class WSQueries:

	def __init__(self, ttl_file):
		self.g = Graph()
		self.g.parse(ttl_file, format="n3")

	def getDistinctGenres(self):
		query = "SELECT DISTINCT ?genre WHERE { ?a :hasGenre ?genre }"

		qres = self.g.query(query)

		l = []

		for row in qres:
			l.append(str(row[0]).split("#")[1])

		return l

	def getFilmsByGenre(self, genre):
		namespace="<http://www.semanticmovies.pt/#"+genre+">"

		l=[]
		query = "SELECT  ?film ?filmID ?poster  WHERE { "+namespace+" :isGenreOf ?a. ?a :hasTitle ?film. ?a :hasFilmID ?filmID. ?a :hasPoster ?poster}"


		qres=self.g.query(query)

		for row in qres:
			l.append({"hasTitle":str(row[0]),"hasFilmID":str(row[1]),"hasPoster":str(row[2])})

		return l

	def getRelatedFilms(self, id):
	
		listFilmGenre = []
		listDirectors = []
		listRelated = []

		filmGenre = self.getFilmGenre(id)
		for i in filmGenre:
			listFilmGenre.append( i["hasGenre"])

		directors = self.getDirectorsByFilm(id)

		listDirectors.append( directors[0]["hasPersonID"])

		for i in listFilmGenre:
			listRelated += random.sample(self.getFilmsByGenre(i), 5)

		for i in listDirectors:
			listRelated += self.getFilmsByDirector(i)

		aux = 0
		index = -1
		for i in listRelated:
			if i["hasFilmID"] == id:
				index = aux
				break
			aux+=1

		if index >= 0:
			#del listRelated[index]
			listRelated.pop(index)

		return random.sample(listRelated,6)

	def getFilmGenre(self, id):

		l=[]
		query = "SELECT ?filmID ?title ?genre WHERE {?a :hasGenre ?genre. ?a :hasFilmID ?filmID. ?a :hasTitle ?title. FILTER (regex(?filmID,'"+id+"')).}"
		qres=self.g.query(query)

		for row in qres:
			l.append({"hasFilmID":str(row[0]),"hasTitle":str(row[1]),"hasGenre":str(row[2]).split("#")[1]})

		return l

	def getFilmsByActor(self, personID):
		l=[]
		query = "SELECT ?actorID ?actor ?film ?filmID ?poster WHERE {?a :isActorOf ?b. ?a :hasPersonID ?actorID. ?a :hasName ?actor. ?b :hasTitle ?film. ?b :hasFilmID ?filmID. ?b :hasPoster ?poster. FILTER (regex(?actorID,'"+personID+"')).}"
		qres=self.g.query(query)

		for row in qres:
			l.append({"hasPersonID":str(row[0]),"hasName":str(row[1]),"hasTitle":str(row[2]), "hasFilmID":str(row[3]), "hasPoster":str(row[4])})

		return l

	def getFilmsByDirector(self, personID):
		l=[]
		query = "SELECT ?directorID ?director ?film ?filmID ?poster WHERE {?a :isDirectorOf ?b. ?a :hasPersonID ?directorID. ?a :hasName ?director. ?b :hasTitle ?film. ?b :hasFilmID ?filmID. ?b :hasPoster ?poster. FILTER (regex(?directorID,'"+personID+"')).}"
		qres=self.g.query(query)

		for row in qres:
			l.append({"hasPersonID":str(row[0]),"hasName":str(row[1]),"hasTitle":str(row[2]), "hasFilmID":str(row[3]), "hasPoster":str(row[4])})

		return l

	def getFilmsByWriter(self, personID):
		l=[]
		query = "SELECT ?writerID ?writer ?film ?filmID ?poster WHERE {?a :isWriterOf ?b. ?a :hasPersonID ?writerID. ?a :hasName ?writer. ?b :hasTitle ?film. ?b :hasFilmID ?filmID. ?b :hasPoster ?poster. FILTER (regex(?writerID,'"+personID+"')).}"
		qres=self.g.query(query)

		for row in qres:
			l.append({"hasPersonID":str(row[0]),"hasName":str(row[1]),"hasTitle":str(row[2]), "hasFilmID":str(row[3]), "hasPoster":str(row[4])})

		return l


	def getAllPersons(self):
		l=[]
		query = "SELECT ?personID ?person  WHERE { ?a :hasName ?person. ?a :hasPersonID ?personID.}"
		qres=self.g.query(query)

		for row in qres:
			l.append({"hasPersonID":str(row[0]),"hasName":str(row[1])})


		return l


	def getAllFilms(self):
		l=[]
		query = "SELECT ?filmID ?film ?poster WHERE {?a :hasTitle ?film. ?a :hasFilmID ?filmID. ?a :hasPoster ?poster }"
		qres=self.g.query(query)

		for row in qres:
			l.append({"hasFilmID":str(row[0]),"hasTitle":str(row[1]),"hasPoster":str(row[2])})


		return l


	def getPersonInfo(self, personID):
		l=[]
		query = "SELECT ?name ?id ?job WHERE { ?a :hasName ?name. ?a :hasPersonID ?id. ?a :hasJob ?job FILTER (regex(?id,'"+personID+"')).}"
		qres=self.g.query(query)

		for row in qres:
			l.append({"hasName":str(row[0]),"hasPersonID":personID,"hasJob":str(row[2])})


		return l[0]


	def getActorsByFilm(self, id):
		l=[]
		query = "SELECT ?filmID ?actor ?actorID WHERE {?a :hasActor ?b. ?a :hasFilmID ?filmID. ?b :hasName ?actor. ?b :hasPersonID ?actorID FILTER (regex(?filmID,'"+id+"')).}"
		qres=self.g.query(query)
		for row in qres:
			l.append({"hasFilmID":str(row[0]),"hasName":str(row[1]),"hasPersonID":str(row[2])})

		return l

	def getWritersByFilm(self, id):
		l=[]
		query = "SELECT ?filmID ?writer ?writerID WHERE {?a :hasWriter ?b. ?a :hasFilmID ?filmID. ?b :hasName ?writer. ?b :hasPersonID ?writerID. FILTER (regex(?filmID,'"+id+"')).}"
		qres=self.g.query(query)
		for row in qres:
			l.append({"hasFilmID":str(row[0]),"hasName":str(row[1]),"hasPersonID":str(row[2])})

		return l

	def getDirectorsByFilm(self, id):
		l=[]
		query = "SELECT ?filmID ?director ?directorID WHERE {?a :hasDirector ?b. ?a :hasFilmID ?filmID. ?b :hasName ?director. ?b:hasPersonID ?directorID. FILTER (regex(?filmID,'"+id+"')).}"
		qres=self.g.query(query)
		for row in qres:
			l.append({"hasFilmID":str(row[0]),"hasName":str(row[1]),"hasPersonID":str(row[2])})

		return l

	def getProducersByFilm(self, id):
		l=[]
		query = "SELECT ?filmID ?producer ?producerID WHERE {?a :hasProducer ?b. ?a :hasFilmID ?filmID. ?b :hasName ?producer. ?b :hasPersonID ?producerID. FILTER (regex(?filmID,'"+id+"')).}"
		qres=self.g.query(query)
		for row in qres:
			l.append({"hasFilmID":str(row[0]),"hasName":str(row[1]),"hasPersonID":str(row[2])})

		return l

	def getFilmInfo(self, id):
		l=[]
		query = "SELECT ?filmID ?title ?runtime ?release_date ?rating ?votes ?tagline ?plot ?poster ?actor WHERE {?a a :Film. ?a :hasFilmID ?filmID.  ?a :hasTitle ?title. ?a :hasRuntime ?runtime. ?a :hasReleaseDate ?release_date. ?a :hasRating ?rating. ?a :hasVotes ?votes. ?a :hasTagline ?tagline. ?a :hasPlot ?plot. ?a :hasPoster ?poster.  FILTER (regex(?filmID,'"+id+"')).}"

		qres=self.g.query(query)
		for row in qres:
			l.append({"hasFilmID":str(row[0]),"hasTitle":str(row[1]),"hasRuntime":int(row[2]),"hasReleaseDate":str(row[3]),"hasRating":str(row[4]),"hasVotes":str(row[5]),"hasTagline":str(row[6]),"hasPlot":str(row[7]),"hasPoster":str(row[8]),"hasActor":str(row[9])})

		return l[0]


	def searchFilm(self, keyword,dates,genre):
		l=[]

		namespace="<http://www.semanticmovies.pt/#"+genre+">"
		if dates[0] != "" and dates[1] != "":
			dates[0] = dates[0]+"-01-01"
			dates[1] = dates[1]+"-12-31"
			query = "SELECT ?id ?title ?runtime ?release_date ?genre ?rating ?votes ?tagline ?plot ?poster WHERE {?a a :Film. ?a :hasFilmID ?id.  ?a :hasTitle ?title. ?a :hasRuntime ?runtime. ?a :hasReleaseDate ?release_date. ?a :hasRating ?rating. ?a :hasVotes ?votes. ?a :hasTagline ?tagline. ?a :hasPlot ?plot. ?a :hasPoster ?poster. FILTER (regex(?title,'.*"+keyword+".*','i')). FIlTER (?release_date >= '"+dates[0]+"').FIlTER (?release_date <= '"+dates[1]+"')."

		elif dates[0] != "":
			dates[0] = dates[0]+"-01-01"
			query = "SELECT ?id ?title ?runtime ?release_date ?rating ?votes ?tagline ?plot ?poster WHERE {?a a :Film. ?a :hasFilmID ?id.  ?a :hasTitle ?title. ?a :hasRuntime ?runtime. ?a :hasReleaseDate ?release_date. ?a :hasRating ?rating. ?a :hasVotes ?votes. ?a :hasTagline ?tagline. ?a :hasPlot ?plot. ?a :hasPoster ?poster. FILTER (regex(?title,'.*"+keyword+".*','i')). FIlTER (?release_date >= '"+dates[0]+"')."

		elif dates[1] != "":
			dates[1] = dates[1]+"-12-31"
			query = "SELECT ?id ?title ?runtime ?release_date ?rating ?votes ?tagline ?plot ?poster WHERE {?a a :Film. ?a :hasFilmID ?id.  ?a :hasTitle ?title. ?a :hasRuntime ?runtime. ?a :hasReleaseDate ?release_date. ?a :hasRating ?rating. ?a :hasVotes ?votes. ?a :hasTagline ?tagline. ?a :hasPlot ?plot. ?a :hasPoster ?poster. FILTER (regex(?title,'.*"+keyword+".*','i')). FIlTER (?release_date <= '"+dates[1]+"')."

		else:
			query = "SELECT ?id ?title ?runtime ?release_date ?rating ?votes ?tagline ?plot ?poster WHERE {?a a :Film. ?a :hasFilmID ?id.  ?a :hasTitle ?title. ?a :hasRuntime ?runtime. ?a :hasReleaseDate ?release_date. ?a :hasRating ?rating. ?a :hasVotes ?votes. ?a :hasTagline ?tagline. ?a :hasPlot ?plot. ?a :hasPoster ?poster. FILTER (regex(?title,'.*"+keyword+".*','i')). "

		if genre != "":
			query += "?a :hasGenre "+namespace+"."

		query +="}"

		qres=self.g.query(query)
		for row in qres:
			l.append({"hasFilmID":str(row[0]),"hasTitle":str(row[1]),"hasRuntime":str(row[2]),"hasReleaseDate":str(row[3]),"hasRating":str(row[4]),"hasVotes":str(row[5]),"hasTagline":str(row[6]),"hasPlot":str(row[7]),"hasPoster":str(row[8])})

		return l

	def searchPerson(self, keyword,job):
		l = []
		namespace="<http://www.semanticmovies.pt/#"+job+">"

		if job != "":
			 query = "SELECT ?id ?person ?job  WHERE {?a a :Person. ?a :hasName ?person. ?a :hasPersonID ?id. ?a :hasJob "+namespace+". FILTER (regex(?person,'.*"+keyword+".*','i')).}"
		else:
			query = "SELECT ?id ?person ?job  WHERE {?a a :Person. ?a :hasName ?person. ?a :hasPersonID ?id. ?a :hasJob ?job. FILTER (regex(?person,'.*"+keyword+".*','i')).}"


		qres=self.g.query(query)

		for row in qres:
			l.append({"hasPersonID":str(row[0]),"hasName":str(row[1]),"hasJob":str(row[2])})


		for i in range(len(l)-1):
			
			for j in range(i+1,len(l)):
				if type(l[i])!=int and type(l[j])!=int:
					if (l[i]["hasName"]==l[j]["hasName"]):
						l[i]["hasJob"]=[l[i]["hasJob"],l[j]["hasJob"]]
						l[j] = -1

		if -1 in l:
			l.remove(-1)