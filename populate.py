from rdflib import Graph, Namespace, RDF, Literal, BNode, URIRef, XSD
import json
from pprint import pprint
from imdbpie import Imdb

imdb = Imdb(cache=True)

top250 = imdb.top_250()

'''
print movie.imdb_id
print movie.title
print movie.type
print movie.year
print movie.plots
print movie.plot_outline
print movie.rating
print movie.genres
print movie.votes
print movie.runtime
print movie.poster_url
print movie.cover_url
print movie.release_date
print movie.certification
print movie.trailer_image_urls
print movie.directors_summary
print movie.creators
print movie.cast_summary
print movie.writers_summary

print movie.cast_summary #actores
print movie.writers_summary #escritores
print movie.directors_summary #directores
'''

g = Graph()
g.parse('ontologia.owl', format="n3")
print("graph has %s statements.\n" % len(g))

ns=Namespace('http://www.semanticmovies.pt/MovieOntology#')
global_ns = Namespace('http://www.semanticmovies.pt/#')

LocalNamespace = Namespace('http://www.semanticmovies.pt/Film/')

for m in top250:
	movie = imdb.get_title_by_id(m["tconst"])
	FilmNode = URIRef(LocalNamespace[movie.imdb_id]);

	g.add((FilmNode,RDF.type,ns.Film))
	g.add((FilmNode,ns.hasFilmID,Literal(movie.imdb_id)))
	g.add((FilmNode,ns.hasTitle,Literal(movie.title)))
	g.add((FilmNode,ns.hasRating,Literal(movie.rating)))
	g.add((FilmNode,ns.hasRuntime,Literal(movie.runtime)))
	g.add((FilmNode,ns.hasReleaseDate,Literal(movie.release_date)))
	g.add((FilmNode,ns.hasVotes,Literal(movie.votes)))
	g.add((FilmNode,ns.hasTagline,Literal(movie.tagline)))
	g.add((FilmNode,ns.hasPlot,Literal(movie.plot_outline)))
	g.add((FilmNode,ns.hasPoster,Literal(movie.poster_url)))

	for genre in movie.genres:
		g.add((FilmNode,ns.hasGenre,global_ns[genre]))
		g.add((global_ns[genre],ns.isGenreOf,FilmNode))

	for person in (movie.cast_summary + movie.writers_summary + movie.directors_summary):
		search = g.value(predicate=ns.hasPersonID, object=Literal(person.imdb_id))
		if(search == None):
			Person = URIRef(Namespace('http://www.semanticmovies.pt/Person/')[person.imdb_id])
			g.add((Person,RDF.type,ns.Person))
			g.add((Person, ns.hasName, Literal(person.name)))
			g.add((Person, ns.hasPersonID, Literal(person.imdb_id)))

	for actor in movie.cast_summary:
		search = g.value(predicate=ns.hasPersonID, object=Literal(actor.imdb_id))
		g.add((FilmNode,ns.hasActor,search))
		g.add((search, ns.hasJob, global_ns["Actor"]))
		g.add((search, ns.isActorOf, FilmNode))
		g.add((global_ns["Actor"], ns.isJobOf, search))

	for writer in movie.writers_summary:
		search = g.value(predicate=ns.hasPersonID, object=Literal(writer.imdb_id))
		g.add((FilmNode,ns.hasWriter,search))
		g.add((search, ns.hasJob, global_ns["Writer"]))
		g.add((search, ns.isWriterOf, FilmNode))
		g.add((global_ns["Writer"], ns.isJobOf, search))

	for director in movie.directors_summary:
		search = g.value(predicate=ns.hasPersonID, object=Literal(director.imdb_id))
		g.add((FilmNode,ns.hasDirector,search))
		g.add((search, ns.hasJob, global_ns["Director"]))
		g.add((search, ns.isDirectorOf, FilmNode))
		g.add((global_ns["Director"], ns.isJobOf, search))

g.serialize(destination='populated_movies.ttl', format='n3')

# isGenreOf, isAwardOf, isActorOf, isProducerOf, isWriterOf, isDirectorOf, isJobOf