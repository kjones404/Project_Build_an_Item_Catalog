#!/usr/bin/env python3


from flask import Flask, render_template, request, redirect, url_for, flash, \
    jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Collection, MovieItem


from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Fresh Tomatoes v2"


engine = create_engine('sqlite:///moviecatalogs.db')
Base.metadata.bind = engine


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


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
