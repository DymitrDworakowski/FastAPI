from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    overview: Mapped[str] = mapped_column(String(1000))
    year: Mapped[int]
    rating: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(100))