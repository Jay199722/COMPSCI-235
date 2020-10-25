import random
from typing import Iterable

import requests
from TMB.adapters.repository import AbstractRepository
from TMB.domain.model import Movie


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]

    return genre_names


def get_director_names(repo: AbstractRepository):
    directors = repo.get_directors()
    director_names = [director.director_full_name for director in directors]

    return director_names


def get_actor_names(repo: AbstractRepository):
    actors = repo.get_actors()
    actor_names = [actor.actor_full_name for actor in actors]

    return actor_names


def get_dates(repo: AbstractRepository):
    dates = repo.get_dates()

    return dates


def get_titles(repo: AbstractRepository):
    movies = repo.get_movies()
    titles = [movie.title for movie in movies]

    return titles


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of movies.
        quantity = movie_count - 1

    # Pick distinct and random movies.
    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    if movie.image_hyperlink == '':
        movie_info = requests.get(f"http://www.omdbapi.com/?t={movie.title}&apikey=1de833f0").text

        try:
            image_link = movie_info.split('","')[13].split('":"')[1]
        except:
            image_link = "static/Movie_logo.jpg"
        movie.image_hyperlink = image_link
    movie_dict = {
        'date': movie.date,
        'title': movie.title,
        'image_hyperlink': movie.image_hyperlink
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
