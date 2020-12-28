# -*- coding: utf-8 -*-
from fastapi import FastAPI
from models.user import User
from starlette.status import HTTP_201_CREATED

app_v2 = FastAPI(root_path="/v2")


@app_v2.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User):
    return {"request body (v2)": user}
