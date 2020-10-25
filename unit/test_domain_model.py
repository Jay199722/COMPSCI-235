from datetime import date

import pytest
from TMB.domain.model import *


@pytest.fixture()
def movie():
    return Movie(
        'test movie',
        1997,
        1001
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def genre():
    return Genre('action')


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.comments:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie):
    assert movie.id == 1001
    assert movie.date == 1997
    assert movie.title == 'test movie'
    assert movie.hyperlink == f'https://www.google.com/search?q={movie.title}&rlz=1C1CHZL_enNZ777NZ777&oq=123&aqs=chrome.0.69i59j69i60l3.1134j0j9&sourceid=chrome&ie=UTF-8 '
    assert len(movie.comments) == 0
    assert len(movie.genres) == 0

    assert repr(
        movie) == '<Movie test movie, 1997>'


def test_movie_less_than_operator():
    movie_1 = Movie(
        'abcd', 2010, None
    )

    movie_2 = Movie(
        'efg', 2011, None
    )

    assert movie_1 < movie_2


def test_genre_construction(genre):
    assert genre.genre_name == 'action'

    for movie in genre.tagged_movies:
        assert False

    assert not genre.is_applied_to(Movie(None, None, None))


def test_make_comment_establishes_relationships(movie, user):
    comment_text = 'COVID-19 in the USA!'
    comment = make_comment(comment_text, user, movie)

    # Check that the User object knows about the Comment.
    assert comment in user.comments

    # Check that the Comment knows about the User.
    assert comment.user is user

    # Check that Movie knows about the Comment.
    assert comment in movie.comments

    # Check that the Comment knows about the Movie.
    assert comment.movie is movie


def test_make_genre_associations(movie, genre):
    make_genre_association(movie, genre)

    # Check that the Movie knows about the Genre.
    assert movie.genres != []
    assert genre in movie.genres

    # check that the Genre knows about the Movie.
    assert genre.is_applied_to(movie)
    assert movie in genre.tagged_movies


def test_make_genre_associations_with_movie_already_genreged(movie, genre):
    make_genre_association(movie, genre)

    with pytest.raises(ModelException):
        make_genre_association(movie, genre)
