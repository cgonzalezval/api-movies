# -*- coding: utf-8 -*-
from fastapi import FastAPI, Body, Header, File
from models.user import User
from models.director import Director
from models.movie import Movie
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response

app_v1 = FastAPI(root_path="/v1")


@app_v1.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User):
    return {"request body": user}


# Se proporciona el valor como parámetro tras la ?
@app_v1.get("/user")
async def get_user_validation(password: str, x_custom: str = Header("default")):
    return {"query parameter": password, "request custom header": x_custom}


# En llaves porque es un parámetro variable. Aparece en la url tras una /
@app_v1.get("/movie/{isan}", response_model=Movie, response_model_exclude=["director"])
async def get_movie_with_isan(isan: str):
    director_dict = {
        "name": "director1",
        "movies": ["movie1", "movie2"],
    }
    director1 = Director(**director_dict)
    movie_dict = {
        "isan": "isan2",
        "name": "movie1",
        "director": director1,
        "year": 2019
    }
    movie = Movie(**movie_dict)
    return movie


@app_v1.get("/director/{id}/movie")
async def get_author_books(id: int, category: str, order: str = "asc"):
    return {"query parameter": order + category + str(id)}


@app_v1.patch("/director/name")
async def patch_director_name(name: str = Body(..., embed=True)):
    # Embed permite enviar el contenido en json (best practice).
    # En caso contrario hay que enviar el parámetro como texto plano
    return {"name in body": name}


@app_v1.post("/user/director")
async def post_user_and_director(user: User, director: Director):
    # Hay que proporcionar los parametros con su key
    # {"author": {...}, "director": {...}}
    return {"user": user, "director": director}


@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    # Headers solo pueden ser strings
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    return {"file size": len(profile_photo)}
