from fastapi import FastAPI
from fastapi import HTTPException
import uvicorn

from db import load_book, save_book
from schema import BookInput, BookOutput


app = FastAPI(
    title="Book API",
    version="1.0",
    description="A simple book API",
    docs_url="/docs",  # 自定义文档URL
    redoc_url="/redoc"  # 自定义 ReDoc URL
)


books = load_book()


# @app.get("/")
# def hello_world():
#     return {"Hello": "FastAPI"}

# @app.get("/test")
# def test():
#     return {"Test": "Test"}

@app.get("/api/books")
def get_books(genre: str|None = None, book_id: int|None = None) -> list[BookOutput]:
    book_list = books
    if genre:
        book_list = [book for book in books if book.genre == genre]

    if book_id:
        return [book for book in book_list if book.book_id == book_id]
    return book_list

@app.get("/api/books/{book_id}")
def get_book_by_id(book_id: int)-> BookOutput:
    for book in books:
        if book.book_id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/api/books")
def add_book(book: BookInput)-> BookOutput:
    new_book = BookOutput(
        book_id=len(books) + 1,
        title=book.title,
        author=book.author,
        genre=book.genre,
        ISBN=book.ISBN,
        pages=book.pages,
        publisher=book.publisher,
        published_year=book.published_year,
        language=book.language,
        rating=book.rating,
        price=book.price,
        availability=book.availability,
    )
    books.append(new_book)
    save_book(books)
    return new_book

@app.delete("/api/books/{book_id}")
def delete_book(book_id: int):
    match = [book for book in books if book.book_id == book_id]
    if not match:
        raise HTTPException(status_code=404, detail="Book not found")
    books.remove(match[0])
    save_book(books)
    return {"message": "Book deleted successfully"}

@app.put("/api/books/{book_id}")
def update_book(book_id: int, book: BookInput)-> BookOutput:
    for b in books:
        if b.book_id == book_id:
            b.title = book.title
            b.author = book.author
            b.genre = book.genre
            b.ISBN = book.ISBN
            b.pages = book.pages
            b.publisher = book.publisher
            b.published_year = book.published_year
            b.language = book.language
            b.rating = book.rating
            b.price = book.price
            b.availability = book.availability
            save_book(books)
            return b
    raise HTTPException(status_code=404, detail="Book not found")

# Run the FastAPI application using Uvicorn
if __name__ == "__main__":
    uvicorn.run("book:app", reload=True)
