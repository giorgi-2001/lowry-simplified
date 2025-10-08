from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .users.router import router as user_router
from .standards.router import router as standard_router
from .projects.router import router as project_router
from .experiments.router import router as exp_router
from .aws import s3


BASE_URL = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("APP started...")
    s3.setup_bucket()
    yield
    print("App is shutting down")


app = FastAPI(lifespan=lifespan)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_methods=["POST", "PUT", "DELETE", "GET"],
#     allow_headers=["*"],
#     allow_credentials=True
# )


app.include_router(router=user_router, prefix=BASE_URL)

app.include_router(router=standard_router, prefix=BASE_URL)

app.include_router(router=project_router, prefix=BASE_URL)

app.include_router(router=exp_router, prefix=BASE_URL)
