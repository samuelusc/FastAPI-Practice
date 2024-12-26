from fastapi import FastAPI
import uvicorn
from sqlmodel import  SQLModel
from db import engine
from routers import books, authors


app = FastAPI(
    title="Book API",
    version="1.0",
    description="A simple book API",
    docs_url="/docs",  
    redoc_url="/redoc"  
)

app.include_router(books.router)
app.include_router(authors.router)

# init session
async def on_startup():
    # create table
    SQLModel.metadata.create_all(engine)
app.add_event_handler("startup", on_startup)







# Run the FastAPI application using Uvicorn
if __name__ == "__main__":
    uvicorn.run("book:app", reload=True)
