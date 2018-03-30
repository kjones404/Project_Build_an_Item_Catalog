from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Collection, Base, MovieItem

engine = create_engine('sqlite:///moviecatalogs.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# collection for fred
collection1 = Collection(name="john")

session.add(collection1)
session.commit()

movieItem1 = MovieItem(title="John Wick", year="2014",
                     img="https://image.tmdb.org/t/p/w342/5vHssUeVe25bMrof1HyaPyWgaP.jpg", description="Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.", collection=collection1)

session.add(movieItem1)
session.commit()
movieItem1 = MovieItem(title="John Wick", year="2014",
                     img="https://image.tmdb.org/t/p/w342/5vHssUeVe25bMrof1HyaPyWgaP.jpg", description="Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.", collection=collection1)

session.add(movieItem1)
session.commit()
movieItem1 = MovieItem(title="John Wick", year="2014",
                     img="https://image.tmdb.org/t/p/w342/5vHssUeVe25bMrof1HyaPyWgaP.jpg", description="Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.", collection=collection1)

session.add(movieItem1)
session.commit()
movieItem1 = MovieItem(title="John Wick", year="2014",
                     img="https://image.tmdb.org/t/p/w342/5vHssUeVe25bMrof1HyaPyWgaP.jpg", description="Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.", collection=collection1)

session.add(movieItem1)
session.commit()
movieItem1 = MovieItem(title="John Wick", year="2014",
                     img="https://image.tmdb.org/t/p/w342/5vHssUeVe25bMrof1HyaPyWgaP.jpg", description="Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.", collection=collection1)

session.add(movieItem1)
session.commit()
movieItem1 = MovieItem(title="John Wick", year="2014",
                     img="https://image.tmdb.org/t/p/w342/5vHssUeVe25bMrof1HyaPyWgaP.jpg", description="Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.", collection=collection1)

session.add(movieItem1)
session.commit()



print ("added movie items!")
