from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field
from fastapi import HTTPException
from app import models, schemas

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello FastAPI!"}

@app.get("/hello")
def hello():
    return {"message": "Hello, Dymitr!"}


# @app.get("/books")
# def get_books():
#     return {
#         "books": [
#             {"id": 1, "title": "Gdzie kończy się imię"},
#             {"id": 2, "title": "Metro 2033"},
#         ]
#     }

@app.get("/books/{book_id}")
def get_book(book_id: int):
    return {
        "book_id": book_id,
        "title": "Gdzie kończy się imię",
        "author": "Dymitr Dworakowski",
        "year": 2022,
        "available": True

    }



@app.get("/books")
def get_books(limit: int = 10, available: bool = True):
    return {
        "limit": limit,
        "available": available
    }

@app.get("/about")
def about():
    return {"name": "Dymitr", "role": "Network Administrator", "learning": "FastAPI"}


@app.get("/search")
def search_books(query: str | None = None):
    return {
        "query": query
    }




class Book(BaseModel):
    title: str
    author: str
    year: int
    available: bool = True


@app.post("/books")
def create_book(book: Book):
    return {
        "message": f"Книгу {book.title} створено ",
        "author": book.author
    }


class Movie(BaseModel):
        title: str
        director: str
        year: int
        available: bool = True
        
movies = [
    {
        "id": 1,
        "title": "Inception",
        "director": "Christopher Nolan",
        "year": 2010
    },
    {
        "id": 2,
        "title": "Interstellar",
        "director": "Christopher Nolan",
        "year": 2014
    }
]

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
   
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Фільм не знайдено"
    )

@app.get("/movies")
def get_movies(limit: int = 10, available: bool = True):
    return {
        "limit": limit,
        "available": available
    }

@app.delete("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)

            return {
                "message": f"Фільм {movie['title']} видалено"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Фільм не знайдено"
    )

@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: schemas.MoviesCreate,
    db: Session = Depends(get_db)
):
    db_movie = models.Movie(
        title=movie.title,
        overview=movie.overview,
        year=movie.year,
        rating=movie.rating,
        category=movie.category
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return {
        "message": f"Фільм {db_movie.title} створено",
        "id": db_movie.id
    }

@app.put("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def update_movie(
    movie_id: int,
    movie: schemas.MoviesUpdate,
    db: Session = Depends(get_db)
):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фільм не знайдено"
        )

    db_movie.title = movie.title
    db_movie.overview = movie.overview
    db_movie.year = movie.year
    db_movie.rating = movie.rating
    db_movie.category = movie.category

    db.commit()
    db.refresh(db_movie)

    return {
        "message": f"Фільм {db_movie.title} оновлено",
        "id": db_movie.id
    }
