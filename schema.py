from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class BookInput(SQLModel):
    title: str
    author: str
    published_year: int
    genre: str
    ISBN: str
    pages: int
    publisher: str
    language: str
    rating: float
    price: float
    in_stock: bool
    copies_available: int
    
    
    class Config:
        json_schema_extra = {
            "example": {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "published_year": 1925,
            "genre": "Fiction",
            "ISBN": "9780743273565",
            "pages": 180,
            "publisher": "Scribner",
            "language": "English",
            "rating": 3.9,
            "price": 45,
            "in_stock": True,
            "copies_available": 5
            }
        }


class Book(BookInput, table=True):
    book_id: int = Field(default=None, primary_key=True)
    auth_id: int = Field(foreign_key="author.author_id")
    author: "Author" = Relationship(back_populates="books")


class AuthorInput(SQLModel):
    name: str
    birth_year: int
    nationality: str

class AuthorOutput(AuthorInput):
    author_id: int
    books: list[Book] = []

class Author(AuthorInput, table=True):
    author_id: int = Field(default=None, primary_key=True)
    books: list[Book] = Relationship(back_populates="author")
    
    
class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(VARCHAR(30), unique=True, index=True))
    password_hash: str = ''
    
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password_hash)

class UserOutput(SQLModel):
    user_id: int
    username: str