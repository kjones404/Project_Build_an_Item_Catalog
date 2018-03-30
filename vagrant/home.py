from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Collection, MovieItem
app = Flask(__name__)


engine = create_engine('sqlite:///moviecatalogs.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/home')
def home():
    collection = session.query(Collection).all()
    return render_template('home.html', collection=collection)

@app.route('/collections/<int:collection_id>/')
def movieCollection(collection_id):
    collection = session.query(Collection).filter_by(id=collection_id).one()
    items = session.query(MovieItem).filter_by(collection_id=collection.id)
    return render_template('collection.html', collection=collection,
                            items=items)

# Create route for newMovieItem function here
@app.route('/collections/<int:collection_id>/new/', methods=['GET', 'POST'])
def newMovie(collection_id):
    if request.method == 'POST':
        newItem = MovieItem(
            title=request.form['name'], collection_id=collection_id)
        session.add(newItem)
        session.commit()
        flash("new movie created!")
        return redirect(url_for('movieCollection', collection_id=collection_id))
    else:
        return render_template('newmovie.html', collection_id=collection_id)

# Create route for editmovieItem function here
@app.route('/collections/<int:collection_id>/<int:movie_id>/edit/',
            methods=['GET', 'POST'])
def editMovie(collection_id, movie_id):
    editedItem = session.query(MovieItem).filter_by(id=movie_id).one()
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('movieCollection', collection_id=collection_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmovie.html', collection_id=collection_id, movie_id=movie_id, item=editedItem)

# Create a route for deleteMovieItem function here
@app.route('/collections/<int:collection_id>/<int:movie_id>/delete/',
            methods=['GET', 'POST'])
def deleteMovie(collection_id, movie_id):
    itemToDelete = session.query(MovieItem).filter_by(id=movie_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('movieCollection', collection_id=collection_id))
    else:
        return render_template('delete.html', item=itemToDelete)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
