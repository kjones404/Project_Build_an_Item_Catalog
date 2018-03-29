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
collection1 = Collection(name="Fred")

session.add(collection1)
session.commit()

movieItem2 = MovieItem(title="The Fifth Element", year="1997",
                     img="https://image.tmdb.org/t/p/w342/zaFa1NRZEnFgRTv5OVXkNIZO78O.jpg", description="In 2257, a taxi driver is unintentionally given the task of saving a young girl who is part of the key that will ensure the survival of humanity.", collection=collection1)

session.add(movieItem2)
session.commit()


movieItem1 = MovieItem(title="John Wick", year="2014",
                     img="https://image.tmdb.org/t/p/w342/5vHssUeVe25bMrof1HyaPyWgaP.jpg", description="Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.", collection=collection1)

session.add(movieItem1)
session.commit()

movieItem2 = MovieItem(title="Guardians of the Galaxy", year="2014",
                     img="https://image.tmdb.org/t/p/w342/y31QB9kn3XSudA15tV7UWQ9XLuW.jpg", description="Light years from Earth, 26 years after being abducted, Peter Quill finds himself the prime target of a manhunt after discovering an orb wanted by Ronan the Accuser.", collection=collection1)

session.add(movieItem2)
session.commit()

movieItem3 = MovieItem(title="The Princess Bride", year="1987",
                     img="https://image.tmdb.org/t/p/w342/gpxjoE0yvRwIhFEJgNArtKtaN7S.jpg", description="In this enchantingly cracked fairy tale, the beautiful Princess Buttercup and the dashing Westley must overcome staggering odds to find happiness amid six-fingered swordsmen, murderous princes, Sicilians and rodents of unusual size. But even death can't stop these true lovebirds from triumphing.", collection=collection1)

session.add(movieItem3)
session.commit()

movieItem4 = MovieItem(title="Ghostbusters", year="2016",
                     img="https://image.tmdb.org/t/p/w342/4qnJ1hsMADxzwnOmnwjZTNp0rKT.jpg", description="Following a ghost invasion of Manhattan, paranormal enthusiasts Erin Gilbert and Abby Yates, nuclear engineer Jillian Holtzmann, and subway worker Patty Tolan band together to stop the otherworldly threat.", collection=collection1)

session.add(movieItem4)
session.commit()

movieItem5 = MovieItem(title="Office Space", year="1999",
                     img="https://image.tmdb.org/t/p/w342/iO9aZzrfmMvm3IqkFiQyuuUMLh2.jpg", description="Three office workers strike back at their evil employers by hatching a hapless attempt to embezzle money.", collection=collection1)

session.add(movieItem5)
session.commit()


print ("added movie items!")
