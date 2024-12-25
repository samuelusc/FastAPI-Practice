from pydantic import BaseModel
from typing import Dict

class Availability(BaseModel):
    in_stock: bool
    copies_available: int


class BookInput(BaseModel):
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
    availability: Availability
    
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
                "availability": {"in_stock": True, "copies_available": 5}
            }
        }

class BookOutput(BookInput):
    book_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "book_id": 1,
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
                "availability": {"in_stock": True, "copies_available": 5}
            }
        }
    

if __name__ == "__main__":
    book = BookOutput(
        book_id=11,
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        published_year=1925,
        genre="Fiction",
        ISBN="9780743273565",
        pages=180,
        publisher="Scribner",
        language="English",
        rating=3.9,
        price=45,
        availability={"in_stock": True, "copies_available": 5}
    )
    print(book)
    print("-----------------")
    print(book.model_dump())
    print(book.model_dump_json())
    print(book.ISBN)
    print(book.book_id)