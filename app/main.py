import asyncio
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, RequestValidationError
from app.router.api_router import router as api_router
from app.core.config import settings
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.core.containers import Container

templates = Jinja2Templates(directory="./app/templates")


def create_app() -> FastAPI:
    container = Container()

    _app = FastAPI(title=settings.PROJECT_NAME)
    _app.container = container

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.add_exception_handler(HTTPException, http_error_handler)
    _app.add_exception_handler(RequestValidationError, http422_error_handler)

    _app.include_router(api_router)

    return _app


app = create_app()


@app.on_event("startup")
async def on_startup():
    await app.container.db().create_database()


@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.route("/")
async def _index(request: Request):
    title = settings.PROJECT_NAME
    description = "A simple inventory api written in python using FastAPI"
    color = "#ADD911"
    repo = "https://github.com/danjaniell/inventory-api/"

    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "title": title,
            "description": description,
            "color": color,
            "repo": repo,
            "status_code": 200,
        },
    )
