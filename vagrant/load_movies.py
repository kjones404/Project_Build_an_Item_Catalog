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


# collection for Fred
collection1 = Collection(name="Fred")

session.add(collection1)
session.commit()

movieItem1 = MovieItem(title="The Fifth Element", year="1997",
                     img="https://image.tmdb.org/t/p/w342/zaFa1NRZEnFgRTv5OVXkNIZO78O.jpg", description="In 2257, a taxi driver is unintentionally given the task of saving a young girl who is part of the key that will ensure the survival of humanity.", collection=collection1)

session.add(movieItem1)
session.commit()

movieItem2 = MovieItem(title="John Wick", year="2014",
                     img="https://image.tmdb.org/t/p/w342/5vHssUeVe25bMrof1HyaPyWgaP.jpg", description="Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.", collection=collection1)

session.add(movieItem2)
session.commit()

movieItem3 = MovieItem(title="Guardians of the Galaxy ", year="2014",
                     img="https://image.tmdb.org/t/p/w342/y31QB9kn3XSudA15tV7UWQ9XLuW.jpg", description="Light years from Earth, 26 years after being abducted, Peter Quill finds himself the prime target of a manhunt after discovering an orb wanted by Ronan the Accuser.", collection=collection1)

session.add(movieItem3)
session.commit()

movieItem4 = MovieItem(title="The Princess Bride", year="1987",
                     img="https://image.tmdb.org/t/p/w342/gpxjoE0yvRwIhFEJgNArtKtaN7S.jpg", description="In this enchantingly cracked fairy tale, the beautiful Princess Buttercup and the dashing Westley must overcome staggering odds to find happiness amid six-fingered swordsmen, murderous princes, Sicilians and rodents of unusual size. But even death can't stop these true lovebirds from triumphing.", collection=collection1)

session.add(movieItem4)
session.commit()

movieItem5 = MovieItem(title="Office Space", year="1999",
                     img="https://image.tmdb.org/t/p/w342/iO9aZzrfmMvm3IqkFiQyuuUMLh2.jpg", description="Three office workers strike back at their evil employers by hatching a hapless attempt to embezzle money.", collection=collection1)
session.add(movieItem5)
session.commit()

movieItem6 = MovieItem(title="Ghostbusters", year="1984",
                     img="https://image.tmdb.org/t/p/w342/3FS3oBdorgczgfCkFi2u8ZTFfpS.jpg", description="After losing their academic posts at a prestigious university, a team of parapsychologists goes into business as proton-pack-toting ghostbusters who exterminate ghouls, hobgoblins and supernatural pests of all stripes. An ad campaign pays off when a knockout cellist hires the squad to purge her swanky digs of demons that appear to be living in her refrigerator", collection=collection1)

session.add(movieItem6)
session.commit()

# collection for Bob
collection2 = Collection(name="Bob")

session.add(collection2)
session.commit()

movieItem1 = MovieItem(title="WALL-E", year="2008",
                     img="https://image.tmdb.org/t/p/w342/9cJETuLMc6R0bTWRA5i7ctY9bxk.jpg", description="WALL-E is the last robot left on an Earth that has been overrun with garbage and all humans have fled to outer space. For 700 years he has continued to try and clean up the mess, but has developed some rather interesting human-like qualities. When a ship arrives with a sleek new type of robot, WALL-E thinks he's finally found a friend and stows away on the ship when it leaves.", collection=collection1)

session.add(movieItem1)
session.commit()

movieItem2 = MovieItem(title="Up", year="2009",
                     img="https://image.tmdb.org/t/p/w342/nk11pvocdb5zbFhX5oq5YiLPYMo.jpg", description="Carl Fredricksen spent his entire life dreaming of exploring the globe and experiencing life to its fullest. But at age 78, life seems to have passed him by, until a twist of fate (and a persistent 8-year old Wilderness Explorer named Russell) gives him a new lease on life.", collection=collection1)

session.add(movieItem2)
session.commit()

movieItem3 = MovieItem(title="Brave", year="2012",
                     img="https://image.tmdb.org/t/p/w342/qhABv2d4NZLhsOOA4iBFM4rfuJC.jpg", description="", collection=collection1)

session.add(movieItem3)
session.commit()

movieItem4 = MovieItem(title="Ratatouille", year="2007",
                     img="https://image.tmdb.org/t/p/w342/y8y6Fv0k068OnHBZtu949A1t6pj.jpg", description="A rat named Remy dreams of becoming a great French chef despite his family's wishes and the obvious problem of being a rat in a decidedly rodent-phobic profession. When fate places Remy in the sewers of Paris, he finds himself ideally situated beneath a restaurant made famous by his culinary hero, Auguste Gusteau. Despite the apparent dangers of being an unlikely - and certainly unwanted - visitor in the kitchen of a fine French restaurant, Remy's passion for cooking soon sets into motion a hilarious and exciting rat race that turns the culinary world of Paris upside down.", collection=collection1)

session.add(movieItem4)
session.commit()

movieItem5 = MovieItem(title="Finding Nemo", year="2003",
                     img="https://image.tmdb.org/t/p/w342/syPWyeeqzTQIxjIUaIFI7d0TyEY.jpg", description="Nemo, an adventurous young clownfish, is unexpectedly taken from his Great Barrier Reef home to a dentist's office aquarium. It's up to his worrisome father Marlin and a friendly but forgetful fish Dory to bring Nemo home -- meeting vegetarian sharks, surfer dude turtles, hypnotic jellyfish, hungry seagulls, and more along the way.", collection=collection1)
session.add(movieItem5)
session.commit()

movieItem6 = MovieItem(title="Piper", year="2016",
                     img="https://image.tmdb.org/t/p/w342/jLRllZsubY8UWpeMyDLVXdRyEWi.jpg", description="A mother bird tries to teach her little one how to find food by herself. In the process, she encounters a traumatic experience that she must overcome in order to survive.", collection=collection1)

session.add(movieItem6)
session.commit()

# collection for John
collection3 = Collection(name="John")

session.add(collection3)
session.commit()

movieItem1 = MovieItem(title="Mortal Kombat", year="1995",
                     img="https://image.tmdb.org/t/p/w342/bdXWixjWVA7Y03PvW74xufrROiJ.jpg", description="For nine generations an evil sorcerer has been victorious in hand-to-hand battle against his mortal enemies. If he wins a tenth Mortal Kombat tournament, desolation and evil will reign over the multiverse forever. To save Earth, three warriors must overcome seemingly insurmountable odds, their own inner demons, and superhuman foes in this action/adventure movie based on one of the most popular video games of all time.", collection=collection1)

session.add(movieItem1)
session.commit()

movieItem2 = MovieItem(title="Heat", year="1995",
                     img="https://image.tmdb.org/t/p/w342/zMyfPUelumio3tiDKPffaUpsQTD.jpg", description="Obsessive master thief, Neil McCauley leads a top-notch crew on various daring heists throughout Los Angeles while determined detective, Vincent Hanna pursues him without rest. Each man recognizes and respects the ability and the dedication of the other even though they are aware their cat-and-mouse game may end in violence.", collection=collection1)

session.add(movieItem2)
session.commit()

movieItem3 = MovieItem(title="Howard the Duck", year="1986",
                     img="https://image.tmdb.org/t/p/w342/f2pj3SSj1GdFSrS5bUojT56umL6.jpg", description="A scientific experiment unknowingly brings extraterrestrial life forms to the Earth through a laser beam. First is the cigar smoking drake Howard from the duck's planet. A few kids try to keep him from the greedy scientists and help him back to his planet. But then a much less friendly being arrives through the beam...", collection=collection1)

session.add(movieItem3)
session.commit()

movieItem4 = MovieItem(title="The Last Dragon", year="1985",
                     img="https://image.tmdb.org/t/p/w342/6vyYudiSKpJq2kuRCDAWhZlbOEW.jpg", description="A young man searches for the master to obtain the final level of martial arts mastery known as the glow. Along the way he must fight an evil martial arts expert and rescue a beautiful singer from an obsessed music promoter.", collection=collection1)

session.add(movieItem4)
session.commit()

movieItem5 = MovieItem(title="The Golden Child", year="1986",
                     img="https://image.tmdb.org/t/p/w342/auDjIWIUob3yKfL78SthUl4Cy4z.jpg", description="A detective specializing in missing children is on a madcap mission to save a youth with mystical powers who's been abducted by an evil cult. He battles a band of super-nasties, scrambles through a booby-trapped chamber of horrors and traverses Tibet to obtain a sacred dagger.", collection=collection1)
session.add(movieItem5)
session.commit()

movieItem6 = MovieItem(title="Spaceballs", year="1987",
                     img="https://image.tmdb.org/t/p/w342/kNbaxEsnCyWBTfANVPHayujBsxp.jpg", description="When the nefarious Dark Helmet hatches a plan to snatch Princess Vespa and steal her planet's air, space-bum-for-hire Lone Starr and his clueless sidekick fly to the rescue. Along the way, they meet Yogurt, who puts Lone Starr wise to the power of The Schwartz. Can he master it in time to save the day?", collection=collection1)

session.add(movieItem6)
session.commit()





print ("added movie items!")
