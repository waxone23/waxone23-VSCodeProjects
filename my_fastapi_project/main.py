import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()
DATA_FILE = "database.json"


# --- MODELS ---
class EntryCreate(BaseModel):
    food: str
    calories: int
    notes: Optional[str] = None


class EntryResponse(BaseModel):
    id: int
    food: str
    calories: int
    notes: Optional[str] = None


# --- DATABASE HELPERS ---
def load_db():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        # Reconstruct Pydantic objects from the file
        return {int(k): EntryCreate(**v) for k, v in data.items()}


def save_db(data):
    with open(DATA_FILE, "w") as f:
        json.dump({k: v.model_dump() for k, v in data.items()}, f)


db = load_db()


# --- ROUTES ---
@app.get("/")
def root():
    return {"message": "Health Tracker API is Online"}


@app.post("/entries", response_model=EntryResponse, status_code=201)
def create_entry(entry: EntryCreate):
    new_id = max(db.keys()) + 1 if db else 1
    db[new_id] = entry
    save_db(db)
    return {"id": new_id, **entry.model_dump()}


@app.get("/entries", response_model=List[EntryResponse])
def list_entries(food: Optional[str] = None):
    results = [{"id": eid, **entry.model_dump()} for eid, entry in db.items()]
    if food:
        results = [e for e in results if food.lower() in e["food"].lower()]
    return results


@app.get("/entries/{entry_id}", response_model=EntryResponse)
def get_entry(entry_id: int):
    if entry_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": entry_id, **db[entry_id].model_dump()}


@app.put("/entries/{entry_id}", response_model=EntryResponse)
def update_entry(entry_id: int, updated: EntryCreate):
    if entry_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    db[entry_id] = updated
    save_db(db)
    return {"id": entry_id, **updated.model_dump()}


@app.delete("/entries/{entry_id}", status_code=204)
def delete_entry(entry_id: int):
    if entry_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    del db[entry_id]
    save_db(db)
    return None
