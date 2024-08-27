from fastapi import FastAPI
from middleware.auth import BasicAuthMiddleware
from db.database import get_database
from routes import hats, collections, users
from utils import get_next_id
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para restringir a domínios específicos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)
# app.add_middleware(BasicAuthMiddleware, db=get_database())

app.include_router(hats.router, prefix="/hats", tags=["Hats"])
app.include_router(collections.router, prefix="/collections", tags=["Collections"])
app.include_router(users.router, prefix="/users", tags=["Users"])

def initialize_counter(sequence_name: str):
    db = get_database()  
    if not db.counters.find_one({"_id": sequence_name}):
        db.counters.insert_one({"_id": sequence_name, "sequence_value": 0})

@app.on_event("startup")
def startup_event():
    initialize_counter("hat_id")
    initialize_counter("collection_id")


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
