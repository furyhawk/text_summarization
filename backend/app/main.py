import uvicorn
from logging.config import dictConfig
import logging


from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.core.config import LogConfig, get_settings
from app.api.routers import model_router


dictConfig(LogConfig().dict())
logger = logging.getLogger("app")

app = FastAPI(title=get_settings().PROJECT_NAME)

app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=False,
                   allow_methods=['*'],
                   allow_headers=['*'])

# Routers
app.include_router(
    model_router,
    # prefix="/api/v1",
    # tags=["users"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
