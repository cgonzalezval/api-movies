# -*- coding: utf-8 -*-
from fastapi import FastAPI, Body
from models.user import User
from models.director import Director

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


@app.patch("/director/name")
async def patch_director_name(name: str = Body(..., embed=True)):
    # Embed permite enviar el contenido en json (best practice).
    # En caso contrario hay que enviar el parámetro como texto plano
    return {"name in body": name}


@app.post("/user/director")
async def post_user_and_director(user: User, director: Director):
    # Hay que proporcionar los parametros con su key
    # {"author": {...}, "director": {...}}
    return {"user": user, "director": director}
