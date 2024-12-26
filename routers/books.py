from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlmodel import Session, select
from db import get_session
from schema import BookInput, Book

router = APIRouter(prefix="/api/books")


@router.get("/")
def get_books(
    session: Session = Depends(get_session),
    genre: str | None = None,
    book_id: int | None = None
) -> list[Book]:
    statement = select(Book)
    if genre:
        statement = statement.where(Book.genre == genre)
    if book_id:
        statement = statement.where(Book.book_id == book_id)
    return session.exec(statement).all()

@router.get("/{book_id}")
def get_book_by_id(book_id: int, session: Session = Depends(get_session))-> Book:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", status_code=201)
def add_book(book: BookInput, session:Session = Depends(get_session))-> Book:
    new_book = Book.model_validate(book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        session.commit()
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@router.put("/{book_id}")
def update_book(book_id: int, book_input: BookInput, session: Session = Depends(get_session))-> Book:
    book = session.get(Book, book_id)
    if book:
        for key, value in book_input.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    raise HTTPException(status_code=404, detail="Book not found")