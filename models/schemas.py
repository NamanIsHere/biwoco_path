"""
Movie models module.
This module defines Pydantic models for Movie-related data,
including schemas for creation, updates, and responses.
"""
from typing import List, Optional
from pydantic import BaseModel

class Movie(BaseModel):
    """
    Base model for a movie.

    Attributes:
        release_date: The release date of the movie (default: Jan 01, 2001).
        title: The title of the movie (default: None title).
        tags: A list of tags associated with the movie (default: empty list).
        actors: A list of actors in the movie (default: empty list).
        country: The country where the movie was produced (default: Unknown Country).
        image_url: The URL for the movie's image (default: N/A).
    """
    release_date: Optional[str] = 'Jan 01, 2001'
    title: Optional[str] = 'None title'
    tags: Optional[List[str]] = []
    actors: Optional[List[str]] = []
    country: Optional[str] = 'Unknown Country'
    image_url: Optional[str] = 'N/A'

class MovieUpdate(Movie):
    """
    Schema for updating an existing movie.
    Inherits all attributes from the Movie model.
    """
    release_date: Optional[str] = 'Jan 01, 2001'
    title: Optional[str] = 'None title'
    tags: Optional[List[str]] = []
    actors: Optional[List[str]] = []
    country: Optional[str] = 'Unknown Country'
    image_url: Optional[str] = 'N/A'

class MovieResponse(Movie):
    """
    Response schema for a movie.

    Attributes:
        id: The unique identifier of the movie.
    """
    id: str

class Movies(BaseModel):
    """
    Another response schema for a movie.
    """
    release_date: str
    title: str
    tags: List[str]
    actors: List[str]
    country: str

class ActorMovies(BaseModel):
    """
    Schema for actor with list of movies that actor has joined
    """
    actor_name: Optional[str] = 'None'
    movies: Optional[list[Movies]] = []
