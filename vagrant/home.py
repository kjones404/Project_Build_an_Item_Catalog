#!/usr/bin/env python3


from flask import Flask, render_template, request, redirect, url_for, flash, \
    jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Collection, MovieItem
import json


app = Flask(__name__)


engine = create_engine('sqlite:///moviecatalogs.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/collections/JSON')
def allJSON():
    collection = session.query(Collection).all()
    return jsonify(collection=[i.serialize for i in collection])

@app.route('/collections/<int:collection_id>/JSON')
def collectionJSON(collection_id):
    collection = session.query(Collection).filter_by(id=collection_id).one()
    movies = session.query(MovieItem).filter_by(
        collection_id=collection_id).all()
    return jsonify(MovieItems=[i.serialize for i in movies])

@app.route('/collections/<int:collection_id>/<int:movie_id>/JSON')
def movieJSON(collection_id, movie_id):
    collection = session.query(Collection).filter_by(id=collection_id).one()
    movie = session.query(MovieItem).filter_by(id=movie_id).one()
    return jsonify(MovieItem= movie.serialize)


@app.route('/')
@app.route('/home')
def home():
    collection = session.query(Collection).all()
    return render_template('home.html', collection=collection)

@app.route('/collections/<int:collection_id>')
@app.route('/collections/<int:collection_id>/')
def movieCollection(collection_id):
    collection = session.query(Collection).filter_by(id=collection_id).one()
    items = session.query(MovieItem).filter_by(collection_id=collection.id)
    return render_template('collection.html', collection=collection,
                            items=items)

# Create route for newMovieItem function here
@app.route('/collections/add', methods=['GET', 'POST'])
@app.route('/collections/add/', methods=['GET', 'POST'])
def addCollection():
    if request.method == 'POST':
        newItem = Collection(
            name=request.form['name'])
        session.add(newItem)
        session.commit()
        flash("New collection created!")
        return redirect(url_for('home'))
    else:
        return render_template('add.html')

# Create route for editmovieItem function here
@app.route('/collections/<int:collection_id>/edit',
            methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/edit/',
            methods=['GET', 'POST'])
def editCollection(collection_id):
    collection = session.query(Collection).filter_by(id=collection_id).one()
    if request.method == 'POST':
        if request.form['name']:
            collection.name = request.form['name']
        session.add(collection)
        session.commit()
        flash("Collection Updated!")
        return redirect(url_for('movieCollection', collection_id=collection_id))
    else:
        return render_template(
            'edit.html', collection_id=collection_id)

# Create a route for deleteMovieItem function here
@app.route('/collections/<int:collection_id>/delete',
            methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/delete/',
            methods=['GET', 'POST'])
def deleteCollection(collection_id):
    collection = session.query(Collection).filter_by(id=collection_id).one()
    if request.method == 'POST':
        session.delete(collection)
        session.commit()
        flash("Collection Deleted!")
        return redirect(url_for('home'))
    else:
        return render_template('delete.html', collection_id=collection_id)

# Create route for newMovieItem function here
@app.route('/collections/<int:collection_id>/new', methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/new/', methods=['GET', 'POST'])
def newMovie(collection_id):
    if request.method == 'POST':
        newItem = MovieItem(
            title=request.form['title'],
            year=request.form['year'],
            description=request.form['description'],
            img=request.form['img'], collection_id=collection_id)
        session.add(newItem)
        session.commit()
        flash("New movie created!")
        return redirect(url_for('movieCollection', collection_id=collection_id))
    else:
        return render_template('newmovie.html', collection_id=collection_id)


# Create route for editmovieItem function here
@app.route('/collections/<int:collection_id>/<int:movie_id>/edit',
            methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/<int:movie_id>/edit/',
            methods=['GET', 'POST'])
def editMovie(collection_id, movie_id):
    editedItem = session.query(MovieItem).filter_by(id=movie_id).one()
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['year']:
            editedItem.year = request.form['year']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['img']:
            editedItem.img = request.form['img']
        session.add(editedItem)
        session.commit()
        flash("Movie Updated!")
        return redirect(url_for('movieCollection', collection_id=collection_id))
    else:
        return render_template(
            'editmovie.html', collection_id=collection_id, movie_id=movie_id, item=editedItem)

# Create a route for deleteMovieItem function here
@app.route('/collections/<int:collection_id>/<int:movie_id>/delete',
            methods=['GET', 'POST'])
@app.route('/collections/<int:collection_id>/<int:movie_id>/delete/',
            methods=['GET', 'POST'])
def deleteMovie(collection_id, movie_id):
    itemToDelete = session.query(MovieItem).filter_by(id=movie_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Movie Deleted!")
        return redirect(url_for('movieCollection', collection_id=collection_id))
    else:
        return render_template('deletemovie.html', item=itemToDelete)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
