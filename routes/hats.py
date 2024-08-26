import logging
from fastapi import FastAPI, Request, HTTPException, APIRouter
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from db.database import get_database
from models.hats_model import Hat, HatCreate, HatUpdate
from utils import get_next_id

logging.basicConfig(
    filename='system_audit.log', 
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("Hats")

app = FastAPI()
router = APIRouter()

@router.post("/create/", response_model=HatCreate)
def create_hat(hat: HatCreate):
    db = get_database()
    collection = db['hats']

    hat_id = get_next_id("hat_id")
    new_hat = hat.dict()
    new_hat['hat_id'] = hat_id
    new_hat['data_criacao'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    collection.insert_one(new_hat)

    logger.info(f"Hat created with ID: {hat_id}")

    return new_hat

@router.patch("/{hat_id}", response_model=Hat)
def update_hat(hat_id: int, hat_data: HatUpdate):
    db = get_database()
    collection = db['hats']

    existing_hat = collection.find_one({"hat_id": hat_id})
    if not existing_hat:
        logger.warning(f"Failed update attempt: Hat with ID {hat_id} not found")
        raise HTTPException(status_code=404, detail="Hat not found")

    updated_data = {k: v for k, v in hat_data.dict().items() if v is not None}

    if updated_data:
        collection.update_one({"hat_id": hat_id}, {"$set": updated_data})
        logger.info(f"Hat with ID {hat_id} updated")

    updated_hat = collection.find_one({"hat_id": hat_id})
    return updated_hat

@router.delete("/{hat_id}", response_model=dict)
def delete_hat(hat_id: int):
    db = get_database()
    collection = db['hats']

    existing_hat = collection.find_one({"hat_id": hat_id})
    if not existing_hat:
        logger.warning(f"Failed delete attempt: Hat with ID {hat_id} not found")
        raise HTTPException(status_code=404, detail="Hat not found")

    result = collection.delete_one({"hat_id": hat_id})

    if result.deleted_count == 1:
        logger.info(f"Hat with ID {hat_id} deleted")
        return {"status": "success", "message": f"Hat with id {hat_id} has been deleted"}
    else:
        logger.error(f"Failed to delete hat with ID {hat_id}")
        raise HTTPException(status_code=500, detail="Failed to delete the hat")

@router.get("/get_all/", response_model=list[Hat])
def get_hats():
    db = get_database()  
    collection = db['hats']  
    
    try:
        hats = list(collection.find())  
        if not hats:
            logger.warning("No hats found")
            raise HTTPException(status_code=404, detail="Nenhum chapéu encontrado.")
        return hats
    except Exception as e:
        logger.error(f"Error accessing database: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados: " + str(e))

@router.get("/collection/{collection_id}", response_model=list[Hat])
def get_hats_by_collection(collection_id: int): 
    db = get_database()
    collection = db['hats']
    
    try:
        hats = list(collection.find({"collection_id": collection_id}, {"_id": 0}))
        if not hats:
            logger.warning(f"No hats found for collection ID {collection_id}")
            raise HTTPException(status_code=404, detail="Nenhum chapéu encontrado para esta coleção.")
        return hats
    except Exception as e:
        logger.error(f"Error accessing database for collection ID {collection_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados: " + str(e))
    
app.include_router(router)