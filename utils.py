from fastapi import FastAPI
from db.database import get_database

app = FastAPI()

def get_next_id(sequence_name: str) -> int:
    db = get_database()
    collection_name = sequence_name.replace('_id', 's')
    
    if not db.counters.find_one({"_id": sequence_name}):
        db.counters.insert_one({"_id": sequence_name, "sequence_value": 0})

    max_id_document = db[collection_name].find_one(sort=[(sequence_name, -1)])
    max_id = max_id_document[sequence_name] if max_id_document else 0

    result = db.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$set": {"sequence_value": max_id + 1}},
        return_document=True
    )

    if result is None:
        raise ValueError(f"Could not find and update the sequence: {sequence_name}")

    return result["sequence_value"]


