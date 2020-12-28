# -*- coding: utf-8 -*-
import jwt
import time
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM
from starlette.status import HTTP_401_UNAUTHORIZED

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

jwt_user1_data = {
    "username": "user1",
    "password": "$2b$12$tnvGJ8iEKngfobwH/MMxPuEaaHx/lUs25y6jylLr3tmvvJV1mIPW6",
    "disabled": False, "role": "admin"}
jwt_user1 = JWTUser(**jwt_user1_data)


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        return False


# Authenticate username and password to give JWT token
def authenticate_user(user: JWTUser):
    if jwt_user1.username == user.username:
        if verify_password(user.password, jwt_user1.password):
            return True
    return False


# Create access JWT token
def create_jwt_token(user: JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {
        "sub": user.username,
        "role": user.role,
        "exp": expiration,
    }
    jwt_token = jwt.encode(payload=jwt_payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return jwt_token


# Check whether JWT token is correct
def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")

        if time.time() < expiration:
            if jwt_user1.username == username:
                return final_checks(role)
    except Exception:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

