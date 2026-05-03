from uuid import uuid4

from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from contextlib import asynccontextmanager


DATABASE_URL = "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)

class CategoryORM(Base):
    __tablename__ = "categories"
    name: Mapped[str]


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def task_to_model(task_orm: TaskORM)-> Task:
    return Task(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

@app.get('/tasks')
def get_tasks(db: Session = Depends(get_db)):
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_to_model(task) for task in tasks_from_db]


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()

    return task_to_model(new_task)

@app.patch('/tasks/{task_id}', response_model=Task)
def update_tasks(task_id: str, payload: TaskPatch, db: Session = Depends(get_db)) -> Task:
    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed:
        task_for_update.completed = payload.completed

    db.commit()
    return task_for_update

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_tasks(task_id: str, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()


class Books(BaseModel):
    book: str


book: str = ""


@app.get('/book', response_model=str)
def get_books():
    return f"Любимая книга: {book}"

@app.post('/books', status_code=status.HTTP_201_CREATED)
def post_books(payload: Books):
    global book
    book = payload.book
    return {'message': 'Книга сохранена', 'book': book}



class Category(BaseModel):
    id: str
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str | None


def categories_to_model(categories: CategoryORM) -> Category:
    return Category(id=categories.id, name=categories.name)


@app.post('/categories', response_model=Category, status_code=status.HTTP_201_CREATED)
def post_categories(payload: CategoryCreate, db: Session = Depends(get_db)):
    categories = CategoryORM(name=payload.name)

    db.add(categories)
    db.commit()
    return categories_to_model(categories)

@app.get('/categories', response_model=list[Category])
def get_categories(db: Session = Depends(get_db)) -> list[Category]:
    categories_orm = db.scalars(select(CategoryORM)).all()
    return [categories_to_model(categories) for categories in categories_orm]

@app.patch('/categories/{category_id}', response_model=Category)
def update_categories(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)) -> Category:
    categories = db.get(CategoryORM, category_id)
    if categories is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    categories.name = payload.name if payload.name is not None else categories.name
    db.commit()
    return categories_to_model(categories)



@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_categories(category_id: str, db: Session = Depends(get_db)):
    categories = db.get(CategoryORM, category_id)
    if categories is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    db.delete(categories)
    db.commit()