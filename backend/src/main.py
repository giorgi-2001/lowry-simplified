from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .users.router import router as user_router
from .standards.router import router as standard_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "localhost"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


@app.get("/", tags=["Greeting"])
def greeting():
    return {"greeting": "Hello"}


app.include_router(router=user_router, prefix="/api/v1")

app.include_router(router=standard_router, prefix="/api/v1")