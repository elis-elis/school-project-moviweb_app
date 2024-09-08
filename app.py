from flask import Flask, request, jsonify, flash, render_template, redirect, url_for
from flask_cors import CORS
from config import Config
from data_models import db, User, Movie, user_movies
from datamanager.sqlite_data_manager import SQLiteDataManager
import requests

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# initialize an instance of SQLiteDataManager with the Flask app
data_manager = SQLiteDataManager(app)


# with app.app_context():
#    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Handle POST request (form submission)
        user_name = request.form.get('user_name')

        # Validate and remove any leading or trailing whitespace characters
        if user_name and user_name.strip():
            data_manager.add_user(user_name)
            flash('User added successfully! 🦕', 'success')
            return redirect(url_for('add_user'))
        else:
            flash('User name is required and cannot be empty! 🦖', 'error')
            # Return the form with an error message
            return render_template('add_user.html')
    else:
        # Handle GET request (display form)
        return render_template('add_user.html')


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        # Extract movie data from the form
        movie_data = {
            'title': request.form.get('title'),
            'director': request.form.get('director'),
            'release_year': request.form.get('release_year'),
            'rating': request.form.get('movie_rating')
        }

        # Check if all fields are filled
        if movie_data['title'] and movie_data['director'] and movie_data['release_year'] and movie_data['rating']:
            # Add the movie to the database
            data_manager.add_movie(movie_data)
            flash('Movie added successfully! 🎡', 'success')
            # Redirect to the same page to clear the form
            return redirect(url_for('add_movie'))
        else:
            flash('All fields are required! 🌋', 'error')

    else:
        return render_template('add_movie.html', movie_data={})


@app.route('/users/<int:user_id>', methods=['GET'])
def display_user_movies(user_id):
    # Fetch user from the database, this is to ensure the user exists
    user = data_manager.get_user_by_id(user_id)

    # Fetch the user's favorite movies
    movies = data_manager.get_user_movies(user_id)

    if not user:
        flash(f'User with ID {user_id} is not found.', 'error')
        return redirect('/users')

    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
def add_movie_to_user(user_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
