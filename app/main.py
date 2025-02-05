from fastapi import FastAPI, Depends, HTTPException

from app.api.v1.router import router

app = FastAPI()


app.include_router(router)