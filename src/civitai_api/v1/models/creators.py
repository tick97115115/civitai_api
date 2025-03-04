from typing import Annotated, List
from annotated_types import Len
from pydantic import BaseModel, Field, StrictInt

class Response_Creaters_Item(BaseModel):
    username: str
    modelCount: int | None = None # if the creator have no models, this field will not exist in the response
    link: str
    image: str | None = None # URL to the creator's avatar

class Response_Creaters_Metadata(BaseModel):
    totalItems: int
    currentPage: int
    pageSize: int
    totalPages: int
    nextPage: str | None = None # only exists if currentPage < totalPages
    prevPage: str | None = None # only exists if currentPage > 1

class Response_Creaters(BaseModel):
    items: List[Response_Creaters_Item]
    metadata: Response_Creaters_Metadata


LimitInt = Annotated[int, Field(strict=True, ge=1, le=200)]
Limit = Annotated[List[LimitInt], Len(1, 1)]
class Creators_API_Opts(BaseModel):
    limit: None | Limit = None # The number of results to be returned per page. This can be a number between 0 and 200. By default, each page will return 20 results. If set to 0, it'll return all the creators
    page: None | Annotated[List[StrictInt], Len(1,1)] = None  # The page from which to start fetching creators
    query: None | Annotated[List[str], Len(1,1)] = None # Search query to filter creators by username