# -*- coding: utf-8 -*-
from typing import List
from pydantic import BaseModel


class Director(BaseModel):
    name: str
    movies: List[str]
