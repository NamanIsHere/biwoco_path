from fastapi import FastAPI
from imdb_fastapi.routes.route import endPoints
import sys

sys.path.append(".")
app = FastAPI()
app.include_router(endPoints, prefix="/api/movies")

@app.get('/')
def root():
    return{'message': 'Fast API is running!'}