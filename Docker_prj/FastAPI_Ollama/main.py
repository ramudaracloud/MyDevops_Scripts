from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI, Uvicorn, UV, boto3, tiktoken, and Ollama are ready!"}
