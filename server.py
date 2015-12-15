from flask import Flask, render_template
from WSQueries import WSQueries
import random
app = Flask(__name__)

ws = WSQueries("populated_movies.ttl")

@app.route("/")
def home():
	filmes = ws.getAllFilms()
	filmes = random.sample(filmes, 6)
	return render_template('index.html', movies=filmes, page="home")

@app.route("/movies")
def movies():
	# filmes por ano
	filmes = ws.getAllFilms()
	return render_template('movies.html', movies=filmes, page="movies")

@app.route("/movies/<imdb_id>")
def movie(imdb_id=None):
	# procurar filme por imdb_id
	filme = ws.getFilmInfo(imdb_id)
	filme["actors"] = ws.getActorsByFilm(imdb_id)
	filme["writers"] = ws.getWritersByFilm(imdb_id)
	filme["directors"] = ws.getDirectorsByFilm(imdb_id)
	filme["genres"] = ws.getFilmGenre(imdb_id)
	filme["related"] = ws.getRelatedFilms(imdb_id)

	return render_template('movie.html', movie=filme, page="movies")

@app.route("/person")
def persons(imdb_id=None):
	return render_template('persons.html', page="person", persons=ws.getAllPersons())

@app.route("/person/<imdb_id>")
def person(imdb_id=None):
	asActor = ws.getFilmsByActor(imdb_id)
	asDirector = ws.getFilmsByDirector(imdb_id)
	asWriter = ws.getFilmsByWriter(imdb_id)

	return render_template('person.html', page="person", person=ws.getPersonInfo(imdb_id), moviesAsActor=asActor, moviesAsDirector=asDirector, moviesAsWriter=asWriter)

@app.route("/genres")
def genres():

	return render_template('genres.html', page="genres", genres=1)

@app.route("/genres/<genre_name>")
def genre(genre_name=None):
	movies = ws.getFilmsByGenre(genre_name)
	return render_template('genre.html', page="genres", genre=genre_name, movies=movies)


if __name__ == "__main__":
	app.run(debug=True)