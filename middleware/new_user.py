from passlib.context import CryptContext
from pymongo import MongoClient

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_database():
    client = MongoClient("mongodb://localhost:27017/")
    return client['hats_store']

def create_user(username: str, password: str):
    db = get_database()
    users = db['users']
    password_hash = pwd_context.hash(password)
    
    users.insert_one({"username": username, "password_hash": password_hash})

# Exemplo de criação de um usuário
create_user("admin", "admin_password")
