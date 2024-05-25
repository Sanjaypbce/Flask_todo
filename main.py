from fastapi import FastAPI

from route.router import router

app = FastAPI()

app.include_router(router)

