from pydantic import BaseModel, EmailStr


class MoviesCreate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


class MoviesUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


class MoviesPatch(BaseModel):
    title: str | None = None
    overview: str | None = None
    year: int | None = None
    rating: float | None = None
    category: str | None = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr