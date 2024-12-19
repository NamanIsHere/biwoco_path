"""
Main application file for FastAPI.
This module sets up the FastAPI app and includes movie-related endpoints.
"""

import sys
from fastapi import FastAPI
from imdb_fastapi.routes.route import endPoints

sys.path.append(".")
app = FastAPI()
app.include_router(endPoints, prefix="/api/movies")

@app.get('/')
def root():
    """
    Root endpoint.

    :return: A welcome message indicating that the API is running.
    """
    return{'message': 'Fast API is running!'}
