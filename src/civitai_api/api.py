import enum
from typing import List, Optional, Coroutine, Dict
import anyio.from_thread
import httpx
from civitai_api.models.creators import Response_Creaters
from civitai_api.models.images import NsfwLevel, Sort, Period, Response_Images
from civitai_api.models.models import Response_Models_Type
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

def get_params(params: dict) -> dict:
    params.pop("self", None)
    return {k: str(v) for k, v in params.items() if v is not None}

class Sort(enum.Enum):
    Highest_Rated = 'Highest Rated'
    Most_Downloaded = 'Most Downloaded'
    Newest = 'Newest'

class AllowCommercialUse(enum.Enum):
    None_ = 'None'
    Image = 'Image'
    Rent = 'Rent'
    Sell = 'Sell'

class CivitaiAPI:
    def __init__(self, api_key: Optional[str] = None, proxy: Optional[str] = None):
        self.api_key = api_key
        self.proxy = proxy
        self.headers: Dict | None = None
        if api_key is not None:
            self.headers = {
                "Authorization": f"Bearer {self.api_key}"
            }

        if (proxy != None):
            self.client = httpx.Client(proxy=proxy, event_hooks={"request": []}, headers=self.headers)
            self.async_client = httpx.AsyncClient(proxy=proxy, event_hooks={"request": []}, headers=self.headers)
        else:
            self.client = httpx.Client(event_hooks={"request": []}, headers=self.headers)
            self.async_client = httpx.AsyncClient(event_hooks={"request": []}, headers=self.headers)

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
            ) -> Response_Creaters:
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
    ) -> Response_Images:
        query_params = get_params(locals())
        response = await self.async_client.get(API_URL_V1_Images, params=query_params)

        return Response_Images(**response.json())
    
    def get_models(
            self,
            limit: 	Optional[int], 	# The number of results to be returned per page. This can be a number between 1 and 100. By default, each page will return 100 results
            page: 	Optional[int], 	# The page from which to start fetching models
            query: 	Optional[str], 	# Search query to filter models by name
            tag: 	Optional[str], 	# Search query to filter models by tag
            username: 	Optional[str], 	# Search query to filter models by user
            types: List[Response_Models_Type], 	# The type of model you want to filter with. If none is specified, it will return all types
            sort: 	Sort, 	# The order in which you wish to sort the results
            period: Period, 	# The time frame in which the models will be sorted
            # rating: 	Optional[int], 	# (Deprecated) The rating you wish to filter the models with. If none is specified, it will return models with any rating
            favorites: Optional[bool], 	# (AUTHED) Filter to favorites of the authenticated user (this requires an API token or session cookie)
            hidden: Optional[bool], 	# (AUTHED) Filter to hidden models of the authenticated user (this requires an API token or session cookie)
            primaryFileOnly: Optional[bool], 	# Only include the primary file for each model (This will use your preferred format options if you use an API token or session cookie)
            allowNoCredit: Optional[bool], 	# Filter to models that require or don't require crediting the creator
            allowDerivatives: Optional[bool], 	# Filter to models that allow or don't allow creating derivatives
            allowDifferentLicenses: Optional[bool], # Filter to models that allow or don't allow derivatives to have a different license
            allowCommercialUse: AllowCommercialUse, 	# Filter to models based on their commercial permissions
            nsfw: Optional[bool], # If false, will return safer images and hide models that don't have safe images
            supportsGeneration: Optional[bool] 	# If true, will return models that support generation
    ):
        if (favorites or hidden):
            if not (self.api_key):
                raise ValueError("If the \'favorites\' and the \'hidden\' params were set, The api_key must be provided while initialize CivitaiAPI class.")
            