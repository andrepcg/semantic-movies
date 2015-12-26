from flask import Flask, render_template, request, session
from WSQueries import WSQueries
import random
app = Flask(__name__)
app.secret_key = 'asdhi7(/&7A;ASDHUjbasd,-91@@€£'

ws = WSQueries("populated_movies.ttl")

@app.route("/")
def index():
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

	if session['username']:
		session['visited_movies'].append(imdb)

	return render_template('movie.html', movie=filme, page="movies")

@app.route("/person")
def persons(imdb_id=None):
	return render_template('persons.html', page="person", persons=ws.getAllPersons())

@app.route("/person/<imdb_id>")
def person(imdb_id=None):
	asActor = ws.getFilmsByActor(imdb_id)
	asDirector = ws.getFilmsByDirector(imdb_id)
	asWriter = ws.getFilmsByWriter(imdb_id)

	if session['username']:
		session['visited_persons'].append(imdb_id)

	return render_template('person.html', page="person", person=ws.getPersonInfo(imdb_id), moviesAsActor=asActor, moviesAsDirector=asDirector, moviesAsWriter=asWriter)

@app.route("/genres")
def genres():
	genres = ws.getDistinctGenres()
	print(genres)
	return render_template('genres.html', page="genres", genres=genres)

@app.route("/genres/<genre_name>")
def genre(genre_name=None):
	movies = ws.getFilmsByGenre(genre_name)
	if session['username']:
		session['visited_genres'].append(genre_name)
	return render_template('genre.html', page="genres", genre=genre_name, movies=movies)


@app.route('/search', methods=['GET', 'POST'])
def search():

	if request.method == 'POST':

		option = int(request.form['searchOption'])

		if option == 0:
			name = str(request.form['title']) if request.form['title'] else ""
			fromYear = str(request.form['fromYear']) if request.form['fromYear'] else ""
			toYear = str(request.form['toYear']) if request.form['toYear'] else ""
			genre = str(request.form['genre']) if request.form['genre'] else ""

			searchParams = {}
			searchParams["title"] = name
			searchParams["fromYear"] = fromYear
			searchParams["toYear"] = toYear
			searchParams["genre"] = genre
			print(searchParams)
			res = ws.searchFilm(name ,[fromYear, toYear], genre)

			return render_template('movieSearch.html', page="search", movies=res, searchParams=searchParams)

		elif option == 2:
			print("do a barrel roll")

	else:
		return render_template('search.html', page="search")

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['visited_movies'] = []
		session['visited_genres'] = []
		session['visited_persons'] = []
		return redirect(url_for('index'))
	return '''
		<form action="" method="post">
			<p><input type=text name=username>
			<p><input type=submit value=Login>
		</form>
	'''

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True)