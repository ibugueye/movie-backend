from fastapi import FastAPI, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
import query_helpers as helpers
import schemas

api_description = """ Bienvenue dans l'API MoviesLens"""

# --- Initialisation de l'application FastApi ---
app= FastAPI(
    title = "MovueLens API", # type: ignore
    description = api_description,
    version = "0.1"
    
)

# --- Dépendance pour la session de base de données ---

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally: 
        db.close()
# Endpoint pour tester la santer de l'api

@app.get(
    "/",
    summary="Vérificatio, de la Santé de l'API",
    description=  "Vérification que l'API fonctionne correctement"  ,
    response_description="Status de l'API",
    operation_id="health_check_movies_api",
    tags=["monitoring"]
    
    
)

async def root():
    return {"message":"APIMovielens operationnelle"}
    

@app.get(
    "/movies/{movie_id}",  
    summary="Obtenir un film par son ID",
    description="Retourne les informations d’un film en utilisant son `movieId`.",
    response_description="Détails du film",
    response_model=schemas.MovieDetailed,
    tags=["films"],
)
def read_movie(movie_id: int = Path(..., description="L'identifiant unique du film"), db: Session = Depends(get_db)):
    movie = helpers.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Film avec l'ID {movie_id} non trouvé")
    return movie

# Endpoint pour obtenir une liste de films (avec pagination et filttres dacultatifs titre , genre n skip, limit)

@app.get("/movies/",
         summary="Lister les films",
         description="Retourne une liste de films avec pagination et filtres optionnels par titre ou genre",
         response_description='Liste de films',
         response_model=List[schemas.MovieSimple],
         tags=["films"]
)
def list_movies(
    skip: int = Query(0,ge=0,description="Nombre de résultats à ignorer"), 
    limit: int = Query(100,le=1000, description= "Nombre maxima de resultats" ),
    title:str = Query(None,description="Filtre par titre"),
    genre: str = Query(None,description= "Filtre par genre"),
    db: Session = Depends(get_db)):

    movies = helpers.get_movies(db,skip,limit=limit,title=title,genre=genre)

    return movies


# Endpoint pour obtenir obtenir une évaluation par utilisation et film 
@app.get(
    "/ratings/{user_id}/{movi_id}",
    summary="Obtenir une évaluation par utilisateur et film",
    description="Retounr l'évalution note donnée par un utilisateur à un film donné.",
    response_description=" Détail de l'évalution",
    response_model=schemas.RatingSimple,
    tags=["évalutions"],
)
def read_rating(
    user_id: int = Path(..., description="ID de l'utilisateur"),
    movie_id: int = Path(..., description="ID du film"),
    db: Session=Depends(get_db)
):
    rating =  helpers.get_ratings(db,user_id=user_id,movie_id=movie_id)
    if rating is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Aucune évaluation trouvé pour l'utilisateur {user_id} et le film {movie_id}",
            )
    return rating 

