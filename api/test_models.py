# %%
from database import SessionLocal
from models import Movie, Rating, Link,Tag

db = SessionLocal()

# %%
# Tester la récuperation de quelques films
movies = db.query(Movie).limit(10).all()

for movie in movies:
    print(f"ID: {movie.movieId}, Titre : {movie.title},Genres: {movie.genres}")
else :
    print("no movies found.")
    
# %%
# Récuperer les films du genre Action

action_movies = db.query(Movie).filter(Movie.genres.contains("Action")).limit(5) 
for movie in action_movies:
    print(f"ID: {movie.movieId}, Titre : {movie.title},Genres: {movie.genres}")
else:
    print("no action movies found.")
    
action_movies = db.query(Movie).filter(Movie.genres.like("%Action%")).limit(5) 
for movie in action_movies:
    print(f"ID: {movie.movieId}, Titre : {movie.title},Genres: {movie.genres}")
else:
    print("no action movies found.")
    
    
# %%
# Tester la récupération de quelques évaluations (rating)
Ratings =db.query(Rating).limit(5).all()

for rating in Ratings:
    print(f"User ID:{rating.userId}, Movie ID: {rating.movieId},RAting: {rating.rating},Timestamp:{rating.timestamp}")
    
 # %%   
    
hight_rated_movies = (
    db.query(Movie.title, Rating.rating)
    .join(Rating)
    .filter(Rating.rating >= 4)
    .limit(5)
    .all()
    
)
print(hight_rated_movies)

for title, rating in hight_rated_movies:
    print(title, rating)

 


#%% 

hight_rated_movies = (
    db.query(Movie.title, Rating.rating)
    .join(Rating)
    .filter(Rating.rating >= 4,Movie.movieId == Rating.movieId)
    .limit(5)
    .all()
    
)
print(hight_rated_movies)

for title, rating in hight_rated_movies:
    print(title, rating)


# %%

# Recuparation des tags associés aux films
tags =db.query(Tag).limit(5).all()

for tag in tags:
    print(f"User ID: {tag.userId}, Movie ID: {tag.movieId}, tag: {tag.tag},Timestamp : {tag.timestamp}")

# %%

# Recuparation des links associés aux films

links = db.query(Link).limit(5).all()

for link in links:
    print(f"Movie ID : {link.movieId}, IMDB ID: {link.imdbId},TMDB ID:{link.tmdbId}")
# %%
# Fermer la session 
db.close()
# %%
