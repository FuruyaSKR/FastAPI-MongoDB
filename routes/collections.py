from fastapi import APIRouter, FastAPI, HTTPException, logger
from typing import List
from models.collections_model import Collection, CollectionCreate, CollectionUpdate
from db.database import get_database
from utils import get_next_id
from datetime import datetime
import logging

router = APIRouter()
app = FastAPI()

logging.basicConfig(
    filename='system_audit.log', 
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("Collections")

@router.post("/create/", response_model=CollectionCreate)
def create_collection(collection_data: CollectionCreate):
    db = get_database()
    collection = db['collections']

    collection_id = get_next_id("collection_id")
    
    new_collection = collection_data.dict()
    new_collection['collection_id'] = collection_id
    new_collection['data_criacao'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    collection.insert_one(new_collection)

    logger.info(f"Collection created with ID {collection_id}")
    return new_collection

@router.patch("/{collection_id}", response_model=Collection)
def update_collection(collection_id: int, collection_data: CollectionUpdate):
    db = get_database()
    collection = db['collections']

    existing_collection = collection.find_one({"collection_id": collection_id})
    if not existing_collection:
        logger.warning(f"Attempted to update non-existent collection with ID {collection_id}")
        raise HTTPException(status_code=404, detail="Collection not found")

    updated_data = {k: v for k, v in collection_data.dict().items() if v is not None}

    if updated_data:
        collection.update_one({"collection_id": collection_id}, {"$set": updated_data})
        logger.info(f"Collection with ID {collection_id} updated with data {updated_data}")

    updated_collection = collection.find_one({"collection_id": collection_id})
    return updated_collection

@router.delete("/{collection_id}", response_model=dict)
def delete_collection(collection_id: int):
    db = get_database()
    collection = db['collections']

    existing_collection = collection.find_one({"collection_id": collection_id})
    if not existing_collection:
        logger.warning(f"Attempted to delete non-existent collection with ID {collection_id}")
        raise HTTPException(status_code=404, detail="Collection not found")

    result = collection.delete_one({"collection_id": collection_id})

    if result.deleted_count == 1:
        logger.info(f"Collection with ID {collection_id} has been deleted")
        return {"status": "success", "message": f"Collection with id {collection_id} has been deleted"}
    else:
        logger.error(f"Failed to delete collection with ID {collection_id}")
        raise HTTPException(status_code=500, detail="Failed to delete the collection")

@router.get("/get_all/", response_model=List[Collection])
def get_collections():
    db = get_database()
    collection = db['collections']
    
    try:
        collections = list(collection.find({}))
        if not collections:
            logger.warning("No collections found")
            raise HTTPException(status_code=404, detail="Nenhuma coleção encontrada.")
        logger.info("Collections retrieved successfully")
        return collections
    except Exception as e:
        logger.error(f"Error accessing database: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados: " + str(e))

app.include_router(router)
