# -*- coding: utf-8 -*-
from fastapi import FastAPI
from models.user import User

app = FastAPI()


@app.post("/user")
async def post_user(user: User):
    return {"request body": user}


# Se proporciona el valor como parámetro tras la ?
@app.get("/user")
async def get_user_validation(password: str):
    return {"query parameter": password}


# En llaves porque es un parámetro variable. Aparece en la url tras una /
@app.get("/movie/{isan}")
async def get_movie_with_isan(isan: str):
    return {"query changable parameter": isan}


@app.get("/director/{id}/movie")
async def get_author_books(id: int, category: str, order: str = "asc"):
    return {"query parameter": order + category + str(id)}
