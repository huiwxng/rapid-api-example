from typing import Union
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

with open('./data/seed_movies.json') as f:
    data = json.load(f)


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/*",
    "https://main--bespoke-praline-02c2f4.netlify.app",
    "https://main--bespoke-praline-02c2f4.netlify.app/*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Movie(BaseModel):
    title: str
    year: int
    director: str

@app.get("/movies")
def read_root():
    return data


@app.get("/movies/{movie_id}")
def read_item(movie_id: int, q: Union[str, None] = None):
    if movie_id >= len(data):
        raise HTTPException(status_code=404, detail="Item not found")
    return data[movie_id]

@app.put("/movies/{movie_id}")
def update_item(movie_id: int, movie: Movie):
    if movie_id >= len(data):
        raise HTTPException(status_code=404, detail="Item not found")
    data[movie_id] = movie
    return {"movie": movie, "movie_id": movie_id}

@app.post("/movies/{movid_id}")
def add_item(movie: Movie):
    data.append(movie)
    return {"movie": movie, "movie_id": len(data)-1}