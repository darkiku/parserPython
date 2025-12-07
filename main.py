from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    try:
        with open('restaurants_2gis.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

@app.get("/")
def root():
    return {"message": "api ресторанов астаны", "total": len(load_data())}

@app.get("/restaurants")
def get_restaurants(skip: int = 0, limit: int = 10):
    data = load_data()
    return data[skip:skip+limit]

@app.get("/restaurants/{id}")
def get_restaurant(id: int):
    data = load_data()
    return data[id] if id < len(data) else {"error": "not found"}

@app.get("/stats")
def stats():
    data = load_data()
    return {"total": len(data)}