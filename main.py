
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api.routers.task import router as task_router
from api.routers.category import router as category_router


app = FastAPI()
app.include_router(router=task_router)
app.include_router(router=category_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=['*'],
)

# book: str = ""
#
#
# @app.get('/book', response_model=str)
# def get_books():
#     return f"Любимая книга: {book}"
#
# @app.post('/books', status_code=status.HTTP_201_CREATED)
# def post_books(payload: Books):
#     global book
#     book = payload.book
#     return {'message': 'Книга сохранена', 'book': book}
