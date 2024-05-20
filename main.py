import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pymongo import MongoClient
import bson

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    database_name: str = ""
    mongo_uri: str = ""
    vizinhos: list[str] = []

def get_environment() -> Environment:
    return Environment()


app = FastAPI()

client = TestClient(app)


@app.get("/api/{_id}")
def get_review(_id: str):
    env = get_environment()
    mongo_client = MongoClient(env.mongo_uri)
    database = mongo_client[env.database_name]
    collection = database["Entidade"]
    has_local_id = collection.find_one({"_id": _id})

    if not has_local_id:
        visited = set()
        stack = list(env.vizinhos)

        while stack:
            vizinho = stack.pop()
            if vizinho not in visited:
                visited.add(vizinho)
                try:
                    response = requests.get(f"http://{vizinho}:8000/api/{_id}")
                    if response.status_code == 200:
                        return JSONResponse(content=response.json())
                    elif response.status_code != 200:
                        continue

                except requests.exceptions.RequestException as e:
                    print(f"Erro ao chamar vizinho={vizinho}: {e}")
                    continue

        raise HTTPException(status_code=404, detail="Item não encontrado")
    else:
        return JSONResponse(content=bson.json_util.dumps(has_local_id))


