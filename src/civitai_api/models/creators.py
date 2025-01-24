from typing import List
from pydantic import BaseModel

class Response_Creaters_Item(BaseModel):
    username: str
    modelCount: int | None = None
    link: str

class Response_Creaters_Metadata(BaseModel):
    totalItems: int
    currentPage: int
    pageSize: int
    totalPages: int
    nextPage: str

class Response_Creaters(BaseModel):
    items: List[Response_Creaters_Item]
    metadata: Response_Creaters_Metadata

class Creators_API_Opts(BaseModel):
    limit: None | List[int] = None, 
    page: None | List[int] = None, 
    query: None | List[str] = None