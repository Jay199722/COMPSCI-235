import TMB.adapters.repository as repo
import TMB.news.services as services
import TMB.utilities.utilities as utilities
import requests
from TMB.authentication.authentication import login_required
from better_profanity import profanity
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

# Configure Blueprint.
news_blueprint = Blueprint(
    'news_bp', __name__)

@news_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 3

    # Read query parameters.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_comments = request.args.get('view_comments_for')
    return mbg(movies_per_page, genre_name, cursor, movie_to_show_comments)


def mbg(movies_per_page, genre_name, cursor, movie_to_show_comments, s=False):
    if movie_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent movie id.
        movie_to_show_comments = -1
    else:
        # Convert movie_to_show_comments from string to int.
        movie_to_show_comments = int(movie_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that are tagged with genre_name.
    movie_ids = services.get_movie_ids_for_genre(genre_name, repo.repo_instance)
    if len(movie_ids) == 0:
        raise IndexError

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)
    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('news_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('news_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('news_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('news_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # Construct urls for viewing movie comments and adding comments.
    for movie in movies:
        movie['view_comment_url'] = url_for('news_bp.movies_by_genre', genre=genre_name, cursor=cursor,
                                            view_comments_for=movie['id'])
        movie['add_comment_url'] = url_for('news_bp.comment_on_movie', movie=movie['id'])

    st = ""
    if s:
        st = f'Search result for "Genre: {genre_name}"'

    # Generate the webpage to display the movies.
    return render_template(
        'news/movies.html',
        title='Movies',
        movies_title='Movies tagged by ' + genre_name,
        movies=movies,
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_comments_for_movie=movie_to_show_comments,
        director_urls=utilities.get_directors_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        title_urls=utilities.get_titles_and_urls(),
        date_urls=utilities.get_dates_and_urls(),
        search_txt=st
    )


@news_blueprint.route('/movies_by_director', methods=['GET'])
def movies_by_director():
    movies_per_page = 3

    # Read query parameters.
    director_name = request.args.get('director')
    cursor = request.args.get('cursor')
    movie_to_show_comments = request.args.get('view_comments_for')
    return mbd(movies_per_page, director_name, cursor, movie_to_show_comments)


def mbd(movies_per_page, director_name, cursor, movie_to_show_comments, s=False):
    if movie_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent movie id.
        movie_to_show_comments = -1
    else:
        # Convert movie_to_show_comments from string to int.
        movie_to_show_comments = int(movie_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that are directed with director_name.
    movie_ids = services.get_movie_ids_for_director(director_name, repo.repo_instance)
    if len(movie_ids) == 0:
        raise IndexError

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('news_bp.movies_by_director', director=director_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('news_bp.movies_by_director', director=director_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('news_bp.movies_by_director', director=director_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('news_bp.movies_by_director', director=director_name, cursor=last_cursor)

    # Construct urls for viewing movie comments and adding comments.
    for movie in movies:
        movie['view_comment_url'] = url_for('news_bp.movies_by_director', director=director_name, cursor=cursor,
                                            view_comments_for=movie['id'])
        movie['add_comment_url'] = url_for('news_bp.comment_on_movie', movie=movie['id'])

    st = ""
    if s:
        st = f'Search result for "Director: {director_name}"'

    # Generate the webpage to display the movies.
    return render_template(
        'news/movies.html',
        title='Movies',
        movies_title='Movies directed by ' + movies[0]['director'],
        movies=movies,
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_comments_for_movie=movie_to_show_comments,
        director_urls=utilities.get_directors_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        title_urls=utilities.get_titles_and_urls(),
        date_urls=utilities.get_dates_and_urls(),
        search_txt=st
    )


@news_blueprint.route('/movies_by_actor', methods=['GET'])
def movies_by_actor():
    movies_per_page = 3

    # Read query parameters.
    actor_name = request.args.get('actor')
    cursor = request.args.get('cursor')
    movie_to_show_comments = request.args.get('view_comments_for')
    return mba(movies_per_page, actor_name, cursor, movie_to_show_comments)


def mba(movies_per_page, actor_name, cursor, movie_to_show_comments, s=False):
    if movie_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent movie id.
        movie_to_show_comments = -1
    else:
        # Convert movie_to_show_comments from string to int.
        movie_to_show_comments = int(movie_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that are acted with actor_name.
    movie_ids = services.get_movie_ids_for_actor(actor_name, repo.repo_instance)
    if len(movie_ids) == 0:
        raise IndexError

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('news_bp.movies_by_actor', actor=actor_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('news_bp.movies_by_actor', actor=actor_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('news_bp.movies_by_actor', actor=actor_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('news_bp.movies_by_actor', actor=actor_name, cursor=last_cursor)

    # Construct urls for viewing movie comments and adding comments.
    for movie in movies:
        movie['view_comment_url'] = url_for('news_bp.movies_by_actor', actor=actor_name, cursor=cursor,
                                            view_comments_for=movie['id'])
        movie['add_comment_url'] = url_for('news_bp.comment_on_movie', movie=movie['id'])

    st = ""
    if s:
        st = f'Search result for "Actor: {actor_name}"'

    name_matched = list()
    for m in movies:
        for a1 in m['actors'].split(","):
            if actor_name in a1:
                name_matched.append(a1)

    actor_full_name = max(name_matched, key=name_matched.count)

    # Generate the webpage to display the movies.
    return render_template(
        'news/movies.html',
        title='Movies',
        movies_title='Movies acted by ' + actor_full_name,
        movies=movies,
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_comments_for_movie=movie_to_show_comments,
        director_urls=utilities.get_directors_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        title_urls=utilities.get_titles_and_urls(),
        date_urls=utilities.get_dates_and_urls(),
        search_txt=st
    )


@news_blueprint.route('/movies_by_title', methods=['GET'])
def movies_by_title():
    movies_per_page = 3

    # Read query parameters.
    title_name = request.args.get('title')
    cursor = request.args.get('cursor')
    movie_to_show_comments = request.args.get('view_comments_for')
    return mbt(movies_per_page, title_name, cursor, movie_to_show_comments)


def mbt(movies_per_page, title_name, cursor, movie_to_show_comments, s=False):
    if movie_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent movie id.
        movie_to_show_comments = -1
    else:
        # Convert movie_to_show_comments from string to int.
        movie_to_show_comments = int(movie_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that are titled with title_name.
    movie_ids = services.get_movie_ids_for_title(title_name, repo.repo_instance)
    if len(movie_ids) == 0:
        raise IndexError

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('news_bp.movies_by_title', title=title_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('news_bp.movies_by_title', title=title_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('news_bp.movies_by_title', title=title_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('news_bp.movies_by_title', title=title_name, cursor=last_cursor)

    # Construct urls for viewing movie comments and adding comments.
    for movie in movies:
        movie['view_comment_url'] = url_for('news_bp.movies_by_title', title=title_name, cursor=cursor,
                                            view_comments_for=movie['id'])
        movie['add_comment_url'] = url_for('news_bp.comment_on_movie', movie=movie['id'])

    st = ""
    if s:
        st = f'Search result for "Title: {title_name}"'

    # Generate the webpage to display the movies.
    return render_template(
        'news/movies.html',
        title='Movies',
        movies_title=movies[0]['title'],
        movies=movies,
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_comments_for_movie=movie_to_show_comments,
        director_urls=utilities.get_directors_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        title_urls=utilities.get_titles_and_urls(),
        date_urls=utilities.get_dates_and_urls(),
        search_txt=st
    )


@news_blueprint.route('/movies_by_date', methods=['GET'])
def movies_by_date():
    movies_per_page = 3

    # Read query parameters.
    date = request.args.get('date')
    cursor = request.args.get('cursor')
    movie_to_show_comments = request.args.get('view_comments_for')
    return mbda(movies_per_page, date, cursor, movie_to_show_comments)


def mbda(movies_per_page, date, cursor, movie_to_show_comments, s=False):
    if date is None:
        date = '2014'
    if movie_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent movie id.
        movie_to_show_comments = -1
    else:
        # Convert movie_to_show_comments from string to int.
        movie_to_show_comments = int(movie_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that are dated with date_name.
    movie_ids = services.get_movie_ids_for_date(date, repo.repo_instance)
    movie_ids.sort()
    if len(movie_ids) == 0:
        raise IndexError

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('news_bp.movies_by_date', date=date, cursor=cursor - movies_per_page)
        first_movie_url = url_for('news_bp.movies_by_date', date=date)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('news_bp.movies_by_date', date=date, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('news_bp.movies_by_date', date=date, cursor=last_cursor)

    # Construct urls for viewing movie comments and adding comments.
    for movie in movies:
        movie['view_comment_url'] = url_for('news_bp.movies_by_date', date=date, cursor=cursor,
                                            view_comments_for=movie['id'])
        movie['add_comment_url'] = url_for('news_bp.comment_on_movie', movie=movie['id'])

    st = ""
    if s:
        st = f'Search result for "Year: {date}"'

    # Generate the webpage to display the movies.
    return render_template(
        'news/movies.html',
        title='Movies',
        movies_title='Movies in ' + date,
        movies=movies,
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_comments_for_movie=movie_to_show_comments,
        director_urls=utilities.get_directors_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        title_urls=utilities.get_titles_and_urls(),
        date_urls=utilities.get_dates_and_urls(),
        search_txt=st
    )


@news_blueprint.route('/comment', methods=['GET', 'POST'])
@login_required
def comment_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an movie id, when subsequently called with a HTTP POST request, the movie id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the movie id, representing the commented movie, from the form.
        movie_id = int(form.movie_id.data)

        # Use the service layer to store the new comment.
        services.add_comment(movie_id, form.comment.data, username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        ratting = form.ratting.data

        services.add_rating(movie_id, float(ratting), username, repo.repo_instance)

        # Cause the web browser to display the page of all movies that have the same date as the commented movie,
        # and display all comments, including the new comment.
        return redirect(url_for('news_bp.movies_by_title', title=movie['title'], view_comments_for=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie id, representing the movie to comment, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie'))

        # Store the movie id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie id of the movie being commented from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the movie to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'news/comment_on_movie.html',
        title='Edit movie',
        movie=movie,
        form=form,
        handler_url=url_for('news_bp.comment_on_movie'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        director_urls=utilities.get_directors_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        title_urls=utilities.get_titles_and_urls(),
        date_urls=utilities.get_dates_and_urls()
    )


@news_blueprint.route('/search', methods=['GET'])
def search():
    # 获取GET数据，注意和获取POST数据的区别
    movies_per_page = 3

    # Read query parameters.
    aim_name = request.args.get('keyword').lower().strip()
    option = request.args.get('option').lower().strip()
    cursor = request.args.get('cursor')
    movie_to_show_comments = request.args.get('view_comments_for')
    if option == "genre":
        try:
            return mbg(movies_per_page, aim_name, cursor, movie_to_show_comments, True)
        except IndexError:
            pass

    if option == "director":
        try:
            return mbd(movies_per_page, aim_name, cursor, movie_to_show_comments, True)
        except IndexError:
            pass

    if option == "actor":
        try:
            return mba(movies_per_page, aim_name, cursor, movie_to_show_comments, True)
        except IndexError:
            pass

    if option == "year":
        try:
            return mbda(movies_per_page, aim_name, cursor, movie_to_show_comments, True)
        except IndexError:
            pass

    if option == "title":
        try:
            return mbt(movies_per_page, aim_name, cursor, movie_to_show_comments, True)
        except IndexError:
            pass
    if option not in ['genre', 'director', 'actor', 'year', 'title']:
        message = "Please select correct search filter and try again"
    else:
        message = f"Sorry, Can't find movie related to {option}: {aim_name}, Please try again"
    return render_template(
        'home/home.html',
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        director_urls=utilities.get_directors_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        title_urls=utilities.get_titles_and_urls(),
        date_urls=utilities.get_dates_and_urls(),
        returned_message=message
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class OneToTen:
    def __init__(self, message=None):
        if not message:
            message = 'Please enter your ratting up to 10'
        self.message = message

    def __call__(self, form, field):
        try:
            if float(field.data) > 10 or float(field.data) < 1:
                raise ValidationError(self.message)
        except:
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    ratting = TextAreaField('Ratting', [
        DataRequired(),
        Length(min=0, message='Your ratting is not available'),
        OneToTen(message='Please enter your ratting up to 10')])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')
