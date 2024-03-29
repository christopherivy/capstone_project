import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import json
import requests
from seed import hc_250shows, hc_250_movies, hc_most_popular_movies, hc_box_office_movies, hc_movie_details

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
API_BASE_TOP_MOVIES = 'https://imdb-api.com/en/API/Top250Movies/k_ybkbttjb/'
API_BASE_POPULAR_MOVIES = 'https://imdb-api.com/en/API/BoxOffice/k_ybkbttjb'


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
	res = requests.get(API_BASE_COMING_SOON)
	coming_soon = res.json()

	res = requests.get(API_BASE_TOP_TV)
	shows = res.json()

	res = requests.get(API_BASE_TOP_MOVIES)
	movies = res.json()

	res = requests.get(API_BASE_POPULAR_MOVIES)
	box_movies = res.json()


    
    # for manual testing of api
    # shows = hc_250shows
    # movies = hc_most_popular_movies
    # box_movies = hc_box_office_movies

	
	return render_template("index.html", shows=shows['items'], movies = movies['items'], box_movies=box_movies['items'])


@app.route('/movie_details/<movie_id>',  methods=['GET'])
def movie_details(movie_id):
	# flash(movie_id)

	# create obj to hold movie details
	# movie_details = hc_movie_details
	# movie_details_similars = hc_movie_details['similars']

	# https://imdb-api.com/en/API/Title/k_ybkbttjb/
	res = requests.get(f'{API_BASE_URL_TITLE}{movie_id}/Trailer,')
	movie_details = res.json()

	# hit api for movie id
	# set movie details = response

	return render_template("movie_details.html", movie_details=movie_details)


# handle user login
@app.route("/sign_in", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")

    return render_template("sign_in.html", form=form)

def do_login(user):
	"""Log in user."""

	session[CURR_USER_KEY] = user.id


# handle user signup
@app.route("/sign_up", methods=["GET", "POST"])
def signup():
    #  create user form
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", "danger")
            return render_template("sign_up.html", form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template("sign_up.html", form=form)


@app.route("/log_out")
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", "success")
    return redirect("/sign_in")


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
