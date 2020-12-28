# -*- coding: utf-8 -*-
from pydantic import BaseModel
from models.director import Director


class Movie(BaseModel):
    isan: str
    name: str
    director: Director
    year: int
