from pydantic import BaseModel, StrictInt as StrictInt

class Response_Tags_Metadata(BaseModel):
    totalItems: StrictInt
    currentPage: StrictInt
    pageSize: StrictInt
    totalPages: StrictInt
    nextPage: str | None
    prevPage: str | None

class Response_Tags_Items(BaseModel):
    name: str
    link: str

class Response_Tags(BaseModel):
    items: list[Response_Tags_Items]
    metadata: Response_Tags_Metadata

class Tags_API_Opts(BaseModel):
    limit: list[StrictInt]
    page: list[StrictInt]
    query: list[str]
