from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Collection, MovieItem
app = Flask(__name__)


engine = create_engine('sqlite:///moviecatalogs.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/')
@app.route('/hello')
def HelloWorld():
    collection = session.query(Collection).first()
    items = session.query(MovieItem).filter_by(collection_id=collection.id)
    output = ''
    for i in items:
        output += i.title
        output += '</br>'
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
