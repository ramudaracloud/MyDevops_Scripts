from fastapi import Body, FastAPI
from ollama import Client
from pprint import pprint

ollama_client = Client(host="http://host.docker.internal:11434",)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI, Uvicorn, UV, boto3, tiktoken, and Ollama are ready!"}



@app.post("/chat")
def chatbot(message : str = Body(..., description="The message")):
    pprint(ollama_client)
    response = ollama_client.chat(model="gemma:2b" , messages = [
        {"role":"user", "content": message}
    ])
    
    return { "response": response.message.content}
