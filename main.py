import logging
from time import perf_counter
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from api.routers import api_router
from core.config import settings
from core.logging import configure_logging

configure_logging()
request_counter = 0
settings = settings
app = FastAPI()
logger = logging.getLogger("app.middleware")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origin,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    global request_counter
    request_counter += 1
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    response.headers["X-Request-Number"] = str(request_counter)

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response

@app.get("/stats")
def get_stats():
    return {"total_requests": request_counter}

app.include_router(api_router)







# app = FastAPI()
# app.include_router(router=task_router)
# app.include_router(router=category_router)
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_methods=['*'],
# )

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
