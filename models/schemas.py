from pydantic import BaseModel
from typing import List, Optional

class Movie(BaseModel):
    release_date: Optional[str] = 'Jan 01, 2001'
    title: Optional[str] = 'None title'
    tags: Optional[List[str]] = []
    actors: Optional[List[str]] = []
    country: Optional[str] = 'Unknown Country'
    image_url: Optional[str] = 'N/A'

class MovieCreate(Movie):
    pass #inherits everything from Movie model

class MovieUpdate(Movie):
    release_date: Optional[str] = 'Jan 01, 2001'
    title: Optional[str] = 'None title'
    tags: Optional[List[str]] = []
    actors: Optional[List[str]] = []
    country: Optional[str] = 'Unknown Country'
    image_url: Optional[str] = 'N/A'

class MovieResponse(Movie):
    id: str
