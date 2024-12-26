from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlmodel import Session, select
from db import get_session
from schema import AuthorInput, Author, AuthorOutput, BookInput, Book

router = APIRouter(prefix="/api/authors")

@router.post("/", status_code=201) 
def add_author(author: AuthorInput, session: Session = Depends(get_session)) -> Author:
    new_author = Author.model_validate(author)
    session.add(new_author)
    session.commit()
    session.refresh(new_author)
    return new_author

@router.get("/")
def get_authors(session: Session = Depends(get_session)) -> list[Author]:
    statement = select(Author)
    return session.exec(statement).all()

@router.get("/{author_id}, response_model=AuthorOutput")
def get_author_by_id(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.post("/{author_id}/books", status_code=201)
def add_book_by_author_id(author_id: int, book: BookInput, session: Session = Depends(get_session)) -> Book:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_book = Book.model_validate(book)
    new_book.auth_id = author_id
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book