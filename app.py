import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import json
import requests
from seed import hc_250shows, hc_250_movies, hc_most_popular_movies, hc_box_office_movies

from forms import UserAddForm, LoginForm, SearchForm
from model import db, connect_db, User

CURR_USER_KEY = "curr_user"
# API_KEY = "59487502"  # This key belongs to Christopher Ivy. Please get your own.
API_KEY = "k_ybkbttjb"  # This key belongs to Christopher Ivy. Please get your own.
API_BASE_URL = "https://imdb-api.com/API/AdvancedSearch/k_ybkbttjb/"
API_BASE_URL_SEARCH = "https://imdb-api.com/en/API/SearchMovie/k_ybkbttjb/"
API_BASE_URL_TITLE = "https://imdb-api.com/en/API/Title/k_ybkbttjb/"
API_BASE_COMING_SOON = 'https://imdb-api.com/en/API/ComingSoon/k_ybkbttjb/'
API_BASE_TOP_TV = 'https://imdb-api.com/en/API/Top250TVs/k_ybkbttjb'
app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///cs_movies"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


# this is the home page aka (index.html)
@app.route("/", methods=["GET"])
def home_page():


		# this is hitting the api
	# res = requests.get(API_BASE_COMING_SOON)
	# coming_soon = res.json()
	# print(coming_soon['items'][0]['id'], '<<<<THIS IS IT')

	# res = requests.get(API_BASE_TOP_TV)
	# shows = res.json()
	# print(shows['items'][0][''image''])

	shows = hc_250shows
	movies = hc_most_popular_movies
	box_movies = hc_box_office_movies
	

	return render_template("index.html", shows=shows['items'], movies = movies['items'], box_movies=box_movies['items'])


@app.route('/movie_details/<movie_id>',  methods=['GET'])
def movie_details(movie_id):
	flash(movie_id)

	return render_template("movie-details.html")
