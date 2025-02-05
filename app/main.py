from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
