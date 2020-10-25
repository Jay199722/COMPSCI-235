import TMB.adapters.repository as repo
import TMB.utilities.services as services
from flask import Blueprint, url_for

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_names.sort()
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('news_bp.movies_by_genre', genre=genre_name)

    return genre_urls


def get_directors_and_urls():
    director_names = services.get_director_names(repo.repo_instance)
    director_names.sort()
    director_urls = dict()
    for director_name in director_names:
        director_urls[director_name] = url_for('news_bp.movies_by_director', director=director_name)

    return director_urls


def get_actors_and_urls():
    actor_names = services.get_actor_names(repo.repo_instance)
    actor_names.sort()
    actor_urls = dict()
    for actor_name in actor_names:
        actor_urls[actor_name] = url_for('news_bp.movies_by_actor', actor=actor_name)

    return actor_urls


def get_titles_and_urls():
    titles = services.get_titles(repo.repo_instance)
    title_urls = dict()
    for title in titles:
        title_urls[title] = url_for('news_bp.movies_by_title', title=title)

    return title_urls


def get_dates_and_urls():
    dates = services.get_dates(repo.repo_instance)
    date_urls = dict()
    for date in dates:
        date_urls[date] = url_for('news_bp.movies_by_date', date=date)

    return date_urls


def get_selected_movies(quantity=5):
    movies = services.get_random_movies(quantity, repo.repo_instance)

    for movie in movies:
        movie['hyperlink'] = url_for('news_bp.movies_by_date', date=movie['date'])
    return movies
