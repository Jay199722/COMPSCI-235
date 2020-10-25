from typing import Iterable

import requests
from TMB.adapters.repository import AbstractRepository
from TMB.domain.model import Movie, Actor, User, Director, Genre, Comment, make_comment


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_comment(movie_id: int, comment_text: str, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        print("cant find user")
        user = User("Guest account", "Abcd1234")

    # Create comment.
    comment = make_comment(comment_text, user, movie)

    # Update the repository.
    repo.add_comment(comment)


def add_rating(movie_id: int, rating: float, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        user = User("Guest account", "Abcd1234")

    # Update the repository.
    repo.add_rating(rating, user, movie)


def add_image_link(movie_id: int, link: str, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    # Update the repository.
    repo.add_image_link(link, movie)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_date(date, repo: AbstractRepository):
    # Returns movies for the target date (empty if no matches), the date of the previous movie (might be null), the date
    # of the next movie (might be null)

    movies = repo.get_movies_by_date(target_date=date)

    movies_dto = list()
    prev_date = next_date = None

    if len(movies) > 0:
        prev_date = repo.get_date_of_previous_movie(movies[0])
        next_date = repo.get_date_of_next_movie(movies[0])

        # Convert Movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_date, next_date


def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre_name)

    return movie_ids


def get_movie_ids_for_director(director_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_director(director_name)

    return movie_ids


def get_movie_ids_for_actor(actor_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_actor(actor_name)

    return movie_ids


def get_movie_ids_for_title(title, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_title(title)

    return movie_ids


def get_movie_ids_for_date(date, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_date(date)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_comments_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return comments_to_dict(movie.comments)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    actors = movie.actors[0].actor_full_name
    for i in movie.actors[1:]:
        actors += ", "
        actors += i.actor_full_name
    if movie.image_hyperlink == '':
        movie_info = requests.get(f"http://www.omdbapi.com/?t={movie.title}&apikey=1de833f0").text
        try:
            image_link = movie_info.split('","')[13].split('":"')[1]
        except:
            image_link = "static/Movie_logo.jpg"
        movie.image_hyperlink = image_link

    movie_dict = {
        'id': movie.id,
        'date': movie.date,
        'title': movie.title,
        'first_para': movie.description,
        'hyperlink': movie.hyperlink,
        'image_hyperlink': movie.image_hyperlink,
        'comments': comments_to_dict(movie.comments),
        'genres': genres_to_dict(movie.genres),
        'rating': movie.rating,
        'votes': movie.votes,
        'metascore': movie.metascore,
        'director': movie.director.director_full_name,
        'actors': actors,
        'runtime_minutes': movie.runtime_minutes,
        'revenue': movie.revenue,
        'voted': movie.voted
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def comment_to_dict(comment: Comment):
    comment_dict = {
        'username': comment.user.username,
        'movie_id': comment.movie.id,
        'comment_text': comment.comment,
        'timestamp': comment.timestamp
    }
    return comment_dict


def comments_to_dict(comments: Iterable[Comment]):
    return [comment_to_dict(comment) for comment in comments]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'tagged_movies': [movie.id for movie in genre.tagged_movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


def director_to_dict(director: Director):
    director_dict = {
        'name': director.director_full_name,
        'directed_movies': [movie.id for movie in director.directed_movies]
    }
    return director_dict


def directors_to_dict(directors: Iterable[Director]):
    return [director_to_dict(director) for director in directors]


def actor_to_dict(actor: Actor):
    actor_dict = {
        'name': actor.actor_full_name,
        'joined_movies': [movie.id for movie in actor.joind_movies]
    }
    return actor_dict


def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(the_dict):
    movie = Movie(the_dict.id, the_dict.date, the_dict.title, the_dict.first_para, the_dict.hyperlink)
    # Note there's no comments or genres.
    return movie
