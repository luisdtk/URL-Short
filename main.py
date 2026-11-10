from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "URL short is working"}