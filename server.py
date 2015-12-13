from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
	return render_template('home.html', name=name)

@app.route("/movies")
def movie(imdb_id=None):
	# filmes por ano
	return render_template('movie.html', movies=)

@app.route("/movies/<imdb_id>")
def movie(imdb_id=None):
	# procurar filme por imdb_id
	return render_template('movie.html', movie=)

@app.route("/person/<imdb_id>")
def person(imdb_id=None):
	# procurar pessoa por imdb_id
	return render_template('person.html', person=)

if __name__ == "__main__":
	app.run(debug=True)