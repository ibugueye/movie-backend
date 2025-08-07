from database import SessionLocal
from query_helpers import *

db = SessionLocal()

#movies = get_movies(db,limit=5)
#for film in movies:
#    print((f"ID : {film.movieId}, Titre:{film.title}, Genre:{film.genres}"))


rating = get_rating(db,movie_id=1, user_id=1) # type: ignore
print(f"User ID:{rating.userId}, Movie ID: {rating.movieId}, Rating : {rating.rating}, Timestamp: {rating.timestamp}") # type: ignore

db.close()
