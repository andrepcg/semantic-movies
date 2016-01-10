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


	def getInfo(self, lista):
		l=[]

		if type(lista) == dict:
			lista=[lista]



		for i in lista:
			v = list(i.values())[0]
			if "Film" in v:
				query = "SELECT ?filmID ?title ?runtime ?release_date ?rating ?votes ?tagline ?plot ?poster ?actor WHERE {<"+v+"> :hasFilmID ?filmID. <"+v+"> :hasTitle ?title. <"+v+"> :hasRuntime ?runtime. <"+v+"> :hasReleaseDate ?release_date. <"+v+"> :hasRating ?rating. <"+v+"> :hasVotes ?votes. <"+v+"> :hasTagline ?tagline. <"+v+"> :hasPlot ?plot. <"+v+"> :hasPoster ?poster. }"
			   
				qres=self.g.query(query)
				for row in qres:
					l.append({"hasFilmID":str(row[0]),"hasTitle":str(row[1]),"hasRuntime":str(row[2]),"hasReleaseDate":str(row[3]),"hasRating":str(row[4]),"hasVotes":str(row[5]),"hasTagline":str(row[6]),"hasPlot":str(row[7]),"hasPoster":str(row[8]),"hasActor":str(row[9])})
			else:
				query = "SELECT ?name ?id ?job WHERE { <"+v+"> :hasName ?name. <"+v+"> :hasPersonID ?id. <"+v+"> :hasJob ?job.}"
				qres=self.g.query(query)

				for row in qres:
					l.append({"hasName":str(row[0]),"hasPersonID":str(row[1]),"hasJob":str(row[2])})

		return l

	def generateQuery(self, dict,length):
		l = []

		if length==1:
			query="SELECT "+dict["selectWord"]+" WHERE {"+dict["query1"]+" "+dict["query2"]+"}"
			
		elif (":hasGenre" in dict["query1"] or ":hasGenre" in dict["query2"] ):
			namespace="<http://www.semanticmovies.pt/#"+dict["filterWord"].capitalize()+">"

			if ":hasGenre" in dict["query1"]:
				dict["query1"]=dict["query1"].replace(dict["filter"],namespace)
			else:
				dict["query2"]=dict["query2"].replace(dict["filter"],namespace)
			query="SELECT "+dict["selectWord"]+" WHERE {"+dict["query1"]+" "+dict["query2"]+"}"
		elif (":hasReleaseDate" in dict["query1"] or ":hasReleaseDate" in dict["query2"] ):
			 query="SELECT "+dict["selectWord"]+" WHERE {"+dict["query1"]+" "+dict["query2"]+" FILTER ("+dict["filter"]+" >= '"+dict["filterWord"]+"-01-01').  FILTER ("+dict["filter"]+" <= '"+dict["filterWord"]+"-12-31').}"
		elif (":hasRating" in dict["query1"] or ":hasRating" in dict["query2"] ):
			query="SELECT "+dict["selectWord"]+" WHERE {"+dict["query1"]+" "+dict["query2"]+" FILTER ("+dict["filter"]+" >= "+dict["filterWord"]+"). FILTER ("+dict["filter"]+" <= "+dict["filterWord"].split(".")[0]+".9).}"
		else:
			query="SELECT "+dict["selectWord"]+" WHERE {"+dict["query1"]+" "+dict["query2"]+" FILTER (regex("+dict["filter"]+",'.*"+dict["filterWord"]+".*','i')).}"

		qres=self.g.query(query)
		for row in qres:
			l.append({"hasFilmID":str(row[0])})

		if len(l) > 1 or len(l) == 0:
			return l
		else:
			return l[0]

	def searchSemantic(self, frase):
		reservedWords=["todos","tem","cujo","de","da","do","com","em","que","os","o","as","a","onde","são","com","foi","é","no","participam","participa","participou","por","pelo"]

		ontology = {"filmes":"","filme":"","classificação":":hasRating","classificacao":":hasRating","genero":":hasGenre","ano":":hasReleaseDate","titulo":":hasTitle","nome":":hasName","atrizes":":hasActor","atriz":":hasActor","ator":":hasActor","atores":":hasActor","realizado":":hasDirector","realizados":":hasDirector","realizador":":hasDirector","dirigido":":hasDirector","dirigidos":":hasDirector","realizadores":":hasDirector","diretor":":hasDirector","diretores":":hasDirector","produzidos":":hasProducer","produzido":":hasProducer","produtor":":hasProducer","produtores":":hasProducer","escrito":":hasWriter","escritor":":hasWriter","escritores":":hasWriter"}
		string = frase.split()
		query1=""
		query2=""
		filterWord=""
		listaQuery=[]
		dict={}

		for i in string:
			if i.lower() in reservedWords:
				continue;
			elif i.lower() in ontology.keys():
				listaQuery.append(i)
			else:
				filterWord+=i+" "

		filterWord=filterWord.rstrip()

		if len(listaQuery)==1:
			dict["filterWord"] = ""
			dict["filter"] = "?a"
			dict["selectWord"] ="?a"
			dict["query2"] = ""

			if listaQuery[0] == "filme" or listaQuery[0] == "filmes":
				dict["query1"] = "?a a :Film."
			else:
				job = ontology[listaQuery[0]]
				job = job.replace(":has","")
				namespace = "<http://www.semanticmovies.pt/#"+job+">"
				dict["query1"] = "?a :hasJob "+namespace+"."

		elif len(listaQuery)==2:
			if ontology[listaQuery[1]]!="":
				query1="?a "+ontology[listaQuery[1]]+" ?b"
			else:
				query1="?a "+ontology[listaQuery[0]]+" ?b"

			if listaQuery[1] == "filme" or listaQuery[1] == "filmes":
				dict["filter"]="?a"
				dict["selectWord"]="?b"
			else:
				dict["filter"]="?b"
				dict["selectWord"]="?a"
			dict["filterWord"]=filterWord
			dict["query1"]=query1+"."
			if(":hasName" not in dict["query1"] and ":hasTitle" not in dict["query1"] and ":hasGenre" not in dict["query1"] and ":hasReleaseDate" not in dict["query1"] and ":hasRating" not in dict["query1"]):
				if listaQuery[1] == "filme" or listaQuery[1] == "filmes":
					 dict["query1"]+=dict["filter"]+" :hasTitle ?c."
				else:
					dict["query1"]+=dict["filter"]+" :hasName ?c."
				dict["filter"]="?c"
			dict["query2"]=""

		elif len(listaQuery)==3:
			query1+="?a "+ontology[listaQuery[0]]+ontology[listaQuery[1]]+" ?b"

			if listaQuery[1] == "filme" or listaQuery[1] == "filmes":
				compose="?a"
				dict["selectWord"]="?b"
			else:
				compose="?b"
				dict["selectWord"]="?a"

			query2+=compose+" "+ontology[listaQuery[2]]+" ?c"
			dict["filter"]="?c"
			dict["filterWord"]=filterWord
			dict["query1"]=query1+"."
			dict["query2"]=query2+". "
			if(":hasName" not in dict["query2"] and ":hasTitle" not in dict["query2"] and ":hasGenre" not in dict["query2"] and ":hasReleaseDate" not in dict["query2"] and ":hasRating" not in dict["query2"]):
				if listaQuery[1] == "filme" or listaQuery[1] == "filmes":
					 dict["query2"]+=dict["filter"]+" :hasTitle ?d."
				else:
					dict["query2"]+=dict["filter"]+" :hasName ?d."
				dict["filter"]="?d"



		l = self.generateQuery(dict,len(listaQuery))
		l = self.getInfo(l)
		return l

