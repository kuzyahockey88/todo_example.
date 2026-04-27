from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=['*'],
)


class Task(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreate(BaseModel):
    title: str


tasks: list[Task] = []


@app.get('/tasks', response_model=list[Task])
def get_tasks():
    return tasks 


@app.post('/tasks', response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task

class Bookin(BaseModel):
    book: str


book: str = ""


@app.get('/book', response_model=str)
def get_books():
    return f"Любимая книга: {book}"

@app.post('/books', status_code=status.HTTP_201_CREATED)
def post_books(payload: Bookin):
    global book
    book = payload.book
    return {'message': 'Книга сохранена', 'book': book}
