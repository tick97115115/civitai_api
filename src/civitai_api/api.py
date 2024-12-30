from typing import Optional, Coroutine
import anyio.from_thread
import httpx
from civitai_api.models.creators import Response_Creaters
from civitai_api.models.images import NsfwLevel, Sort, Period, Response_Images
import anyio
import os
from urllib.parse import urljoin

# API endpoints references: https://github.com/civitai/civitai/wiki/REST-API-Reference

API_URL_V1 = "https://civitai.com/api/v1/"
API_URL_V1_Creators = urljoin(API_URL_V1, "creators") # https://civitai.com/api/v1/creators
API_URL_V1_Images = urljoin(API_URL_V1, "images") # https://civitai.com/api/v1/images
API_URL_V1_Models = urljoin(API_URL_V1, "models") # https://civitai.com/api/v1/models
API_URL_V1_Model_By_Id = urljoin(API_URL_V1, "models/") # "https://civitai.com/api/v1/models/:modelId"
API_URL_ModelVersion_By_VersionId = urljoin(API_URL_V1, "model-versions/")  # "https://civitai.com/api/v1/model-versions/:modelVersionId"
API_URL_ModelVersion_By_Hash = urljoin(API_URL_V1, "model-versions/by-hash/") # "https://civitai.com/api/v1/model-versions/by-hash/:hash"
API_URL_Tags = urljoin(API_URL_V1, "tags") # https://civitai.com/api/v1/tags

API_KEY: str | None = None

def check_request_bearer(request: httpx.Request):
    if API_KEY:
        request.headers["Authorization"] = f"Bearer {API_KEY}"
    # else:
    #     raise ValueError("No API key provided")

async def check_request_bearer_async(request: httpx.Request):
    if API_KEY:
        request.headers["Authorization"] = f"Bearer {API_KEY}"

def get_params(params: dict) -> dict:
    params.pop("self", None)
    return {k: str(v) for k, v in params.items() if v is not None}

class CivitaiAPI:
    def __init__(self, api_key: Optional[str] = None, proxy: Optional[str] = None):
        API_KEY = api_key
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
        response = self.client.get(API_URL_V1_Creators, params=query_params)

        return Response_Creaters(**response.json())
     
    async def async_get_creators_v1(
            self, 
            limit: Optional[int] = None, 
            page: Optional[int] = None, 
            query: Optional[str] = None
            ) -> Coroutine[Response_Creaters]:
        query_params = self.get_creators_v1_construct_query_params(limit, page, query)
        response = await self.async_client.get(API_URL_V1_Creators, params=query_params)

        return Response_Creaters(**response.json())

    def get_images_v1(
            self,
            limit: Optional[int] = None, # The number of results to be returned per page. This can be a number between 0 and 200. By default, each page will return 100 results.
            postId: Optional[int] = None, # The ID of a post to get images from
            modelId: Optional[int] = None, # The ID of a model to get images from (model gallery)
            modelVersionId: Optional[int] = None, # The ID of a model version to get images from (model gallery filtered to version)
            username: Optional[str] = None, # Filter to images from a specific user
            nsfw: Optional[bool | NsfwLevel] = None, # Filter to images that contain mature content flags or not (undefined returns all)
            sort: Optional[Sort] = None, # The order in which you wish to sort the results
            period: Optional[Period] = None, # The time frame in which the images will be sorted
            page: Optional[int] = None, # The page from which to start fetching creators
            ) -> Response_Images:
        query_params = get_params(locals())
        response = self.client.get(API_URL_V1_Images, params=query_params)

        return Response_Images(**response.json())
    
    async def async_get_images_V1(
            self,
            limit: Optional[int] = None, # The number of results to be returned per page. This can be a number between 0 and 200. By default, each page will return 100 results.
            postId: Optional[int] = None, # The ID of a post to get images from
            modelId: Optional[int] = None, # The ID of a model to get images from (model gallery)
            modelVersionId: Optional[int] = None, # The ID of a model version to get images from (model gallery filtered to version)
            username: Optional[str] = None, # Filter to images from a specific user
            nsfw: Optional[bool | NsfwLevel] = None, # Filter to images that contain mature content flags or not (undefined returns all)
            sort: Optional[Sort] = None, # The order in which you wish to sort the results
            period: Optional[Period] = None, # The time frame in which the images will be sorted
            page: Optional[int] = None, # The page from which to start fetching creators
    ) -> Coroutine[Response_Images]:
        query_params = get_params(locals())
        response = await self.async_client.get(API_URL_V1_Images, params=query_params)

        return Response_Images(**response.json())