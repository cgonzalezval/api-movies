# -*- coding: utf-8 -*-
from pydantic import BaseModel
import enum
from fastapi import Query


class Role(str, enum.Enum):
    admin: str = "admin"
    personel: str = "personel"


class User(BaseModel):
    name: str
    password: str
    # ... Indica que es un parámetro obligatorio. Se puede sustituir por un valor por defecto
    mail: str = Query(..., regex="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")
    role: Role
