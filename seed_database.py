"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # Get the title, overview, and poster_path from the movie dictionary. 
    title = movie['title']
    overview = movie['overview']
    poster_path = movie['poster_path']

    # Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    release_date = movie['release_date']
    format = "%Y-%m-%d"

    formatted_release_date = datetime.strptime(release_date, format)

    # create a movie here and append it to movies_in_db
    new_movie = crud.create_movie(title, overview, formatted_release_date, poster_path)
    movies_in_db.append(new_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    # create and add new user to db
    new_user = crud.create_user(email, password)
    model.db.session.add(new_user)

    # create 10 ratings for the new user
    for _ in range(10):
        random_movie = choice(movies_in_db)
        random_rating = randint(1, 5)

        new_rating = crud.create_rating(new_user, random_movie, random_rating)

        model.db.session.add(new_rating)
    
model.db.session.commit()