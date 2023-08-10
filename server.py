"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """View details for movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """View details for user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user_exists = crud.get_user_by_email(email)

    if user_exists:
        flash('An account with this email already exists!')
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!')
    
    return redirect('/')

@app.route("/login", methods=["POST"])
def login_user():
    """log in user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user_exists = crud.get_user_by_email(email)

    print(user_exists)

    if user_exists.email == email and user_exists.password == password:
        session['primary_key'] = user_exists.user_id
        flash('Logged in!')
    else:
        flash('Wrong email or password!')
    
    return redirect('/')

@app.route("/new-rating", methods=["POST"])
def add_new_rating():
    """Add new rating for movie"""
    user_id = session['primary_key']
    score = request.form.get("score")

    movie_title = request.form.get("movie")

    # print(user_id, movie, score)

    if user_id:
        user = crud.get_user_by_id(user_id)
        movie = crud.get_movie_by_title(movie_title)

        new_rating = crud.create_rating(user, movie, score)
        db.session.add(new_rating)
        db.session.commit()
        flash(f'New rating added for {movie_title}!')
    else:
        flash('Log in to rate a movie!')

    return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
