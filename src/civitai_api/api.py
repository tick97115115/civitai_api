from typing import Optional
import anyio.from_thread
import httpx
from civitai_api.models.creators import Response_Creaters
import anyio

API_URL_Creators = "https://civitai.com/api/v1/creators"
API_URL_Images = "https://civitai.com/api/v1/images"
API_URL_Models = "https://civitai.com/api/v1/models"
API_URL_Model = "https://civitai.com/api/v1/models/" # "https://civitai.com/api/v1/models/:modelId"
API_URL_ModelVersion_By_VersionId = "https://civitai.com/api/v1/model-versions/" # "https://civitai.com/api/v1/model-versions/:modelVersionId"
API_URL_ModelVersion_By_Hash = "https://civitai.com/api/v1/model-versions/by-hash/" # "https://civitai.com/api/v1/model-versions/by-hash/:hash"
API_URL_Tags = "https://civitai.com/api/v1/tags"

api_key: str | None = None

def check_request_bearer(request: httpx.Request):
    if api_key:
        request.headers["Authorization"] = f"Bearer {api_key}"
    # else:
    #     raise ValueError("No API key provided")

async def check_request_bearer_async(request: httpx.Request):
    if api_key:
        request.headers["Authorization"] = f"Bearer {api_key}"

class CivitaiAPI:
    def __init__(self, api_key: Optional[str] = None, proxy: Optional[str] = None):
        self.api_key = api_key
        if (proxy != None):
            self.client = httpx.Client(proxy=proxy, event_hooks={"request": [check_request_bearer]})
            self.async_client = httpx.AsyncClient(proxy=proxy, event_hooks={"request": [check_request_bearer_async]})
        else:
            self.client = httpx.Client(event_hooks={"request": [check_request_bearer]})
            self.async_client = httpx.AsyncClient(event_hooks={"request": [check_request_bearer_async]})

    def __del__(self):
        self.client.close()
        anyio.from_thread.run(self.async_client.aclose)

    def get_creators_v1_construct_query_params(
            self, 
            limit: Optional[int] = None, 
            page: Optional[int] = None, 
            query: Optional[str] = None
            ) -> dict:
        query_params = {
            "limit": str(limit) if limit is not None else None,
            "page": str(page) if page is not None else None,
            "query": query if query is not None else None,
        }
        filtered_params = {k: v for k, v in query_params.items() if v is not None}
        if len(filtered_params) == 0:
            filtered_params = None
        return filtered_params

    def get_creators_v1(
            self, 
            limit: Optional[int] = None, 
            page: Optional[int] = None, 
            query: Optional[str] = None
            ) -> Response_Creaters:
        query_params = self.get_creators_v1_construct_query_params(limit, page, query)
        response = self.client.get(API_URL_Creators, params=query_params)

        return Response_Creaters(**response.json())
     
    async def async_get_creators_v1(
            self, 
            limit: Optional[int] = None, 
            page: Optional[int] = None, 
            query: Optional[str] = None
            ) -> Response_Creaters:
        query_params = self.get_creators_v1_construct_query_params(limit, page, query)
        response = await self.async_client.get(API_URL_Creators, params=query_params)

        return Response_Creaters(**response.json())
