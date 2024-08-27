from typing import List
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from pymongo import MongoClient
from datetime import datetime
from models.user_model import User, UserCreate

router = APIRouter()

# Configuração para criptografia de senha
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_database():
    client = MongoClient("mongodb://localhost:27017/")
    return client['hats_store']

@router.post("/create/", response_model=UserCreate)
def create_user(user: UserCreate):
    db = get_database()
    users_collection = db['users']
    password_hash = pwd_context.hash(user.password)

    new_user = {
        "username": user.username,
        "password_hash": password_hash,
    }
    
    users_collection.insert_one(new_user)

    return {"username": user.username, "password": "****"} 

@router.get("/users", response_model=List[User])
def get_users():
    db = get_database()
    users_collection = db['users']

    try:
        users = list(users_collection.find({}, {"_id": 0})) 
        if not users:
            raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
        
        users = [User(**user) for user in users]
        
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados: " + str(e))