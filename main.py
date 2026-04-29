from uuid import uuid4

from fastapi import FastAPI, status, HTTPException
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

class TaskPatch(BaseModel):
    title: str | None = None
    completed: bool | None = None

tasks: list[Task] = []


@app.get('/tasks', response_model=list[Task])
def get_tasks():
    return tasks


@app.post('/tasks', response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task

@app.patch('/tasks/{task_id}', response_model=Task)
def update_tasks(task_id: str, payload: TaskPatch):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_tasks(task_id: str) -> None:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


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




class Category(BaseModel):
    id: str
    title: str
    complete: bool

class CategoryCreate(BaseModel):
    title: str

class CategoryUpdate(BaseModel):
    title: str | None
    complete: bool | None


categories: list [Category] = []


@app.post('/categories', response_model=Category, status_code=status.HTTP_201_CREATED)
def post_categories(payload: CategoryCreate):
    category = Category(id=str(uuid4()), title=payload.title, complete=False)
    categories.append(category)
    return category

@app.get('/categories', response_model=list[Category])
def get_categories():
    return categories

@app.patch('/categories/{category_id}', response_model=Category)
def patch_categories(category_id: str, payload: CategoryUpdate):
    for category in categories:
        if category.id == category_id:
            if payload.title:
                category.title = payload.title
            if payload.complete is not None:
                category.complete = payload.complete
            return category

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_categories(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

