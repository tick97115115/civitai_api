import enum
from typing import Any, List, Optional, Coroutine, Dict
import anyio.from_thread
import httpx
from civitai_api.models.creators import Response_Creaters
from civitai_api.models.images import NsfwLevel, Sort, Period, Response_Images
from civitai_api.models.models import Response_Models, Response_Models_Type, Response_Models_modelVersion
from civitai_api.models.model_by_version_id import Response_ModelByVersionId
import anyio
import os
from urllib.parse import urljoin

from civitai_api.models.models_by_id import Response_Model_ById

# API endpoints references: https://github.com/civitai/civitai/wiki/REST-API-Reference

API_URL_V1 = "https://civitai.com/api/v1/"
API_URL_V1_Creators = urljoin(API_URL_V1, "creators") # https://civitai.com/api/v1/creators
API_URL_V1_Images = urljoin(API_URL_V1, "images") # https://civitai.com/api/v1/images
API_URL_V1_Models = urljoin(API_URL_V1, "models") # https://civitai.com/api/v1/models
API_URL_V1_Model_By_Id = urljoin(API_URL_V1, "models/") # "https://civitai.com/api/v1/models/:modelId"
API_URL_ModelVersion_By_VersionId = urljoin(API_URL_V1, "model-versions/")  # "https://civitai.com/api/v1/model-versions/:modelVersionId"
API_URL_ModelVersion_By_Hash = urljoin(API_URL_V1, "model-versions/by-hash/") # "https://civitai.com/api/v1/model-versions/by-hash/:hash"
API_URL_Tags = urljoin(API_URL_V1, "tags") # https://civitai.com/api/v1/tags

# def construct_header_from_dict(params: dict) -> dict:
    # params.pop("self", None)
    # params.pop("httpx_client", None)
    # params.pop("httpx_async_client", None)
    # return {k: str(v) for k, v in params.items() if v is not None}

def construct_query_params_from_dict(params: Dict[str, List[Any]]):
    params.pop("self", None)
    params.pop("httpx_client", None)
    params.pop("httpx_async_client", None)
    query_params: Dict[str, List[Any]] = {}

    for k,v in params.items():
        if params[k] == None:
            continue
        query_params[k] = []
        for item in v:
            if isinstance(item, bool):
                query_params[k].append(str(item).lower())
            else:
                query_params[k].append(str(item))
    
    return query_params
    

def is_running_anyio_loop():
    try:
        # Attempt to get the current task
        anyio.get_current_task()
        return True  # If successful, an AnyIO event loop is running
    except RuntimeError:
        return False  # No running AnyIO event loop

class Sort(enum.Enum):
    Highest_Rated = 'Highest Rated'
    Most_Downloaded = 'Most Downloaded'
    Newest = 'Newest'

class AllowCommercialUse(enum.Enum):
    None_ = 'None'
    Image = 'Image'
    Rent = 'Rent'
    Sell = 'Sell'

def get_creators_v1(
        httpx_client:httpx.Client,
        limit: None | List[int] = None, 
        page: None | List[int] = None, 
        query: None | List[str] = None
        ) -> Response_Creaters:
    query_params = construct_query_params_from_dict(locals())
    response = httpx.get(API_URL_V1_Creators, params=query_params)
    return Response_Creaters(**response.json())

async def async_get_creators_v1(
        httpx_async_client:httpx.AsyncClient,
        limit: None | List[int] = None, 
        page: None | List[int] = None, 
        query: None | List[str] = None
        ) -> Response_Creaters:
    query_params = construct_query_params_from_dict(locals())
    response = await httpx_async_client.get(API_URL_V1_Creators, params=query_params)
    return Response_Creaters(**response.json())

def get_images_v1(
        httpx_client:httpx.Client,
        limit: None | List[int] = None, # The number of results to be returned per page. This can be a number between 0 and 200. By default, each page will return 100 results.
        postId: None | List[int] = None, # The ID of a post to get images from
        modelId: None | List[int] = None, # The ID of a model to get images from (model gallery)
        modelVersionId: None | List[int] = None, # The ID of a model version to get images from (model gallery filtered to version)
        username: None | List[str] = None, # Filter to images from a specific user
        nsfw: None | List[NsfwLevel] = None, # Filter to images that contain mature content flags or not (undefined returns all)
        sort: None | List[Sort] = None, # The order in which you wish to sort the results
        period: None | List[Period] = None, # The time frame in which the images will be sorted
        page: None | int = None, # The page from which to start fetching creators
        ) -> Response_Images:
    query_params = construct_query_params_from_dict(locals())
    response = httpx_client.get(API_URL_V1_Images, params=query_params)
    return Response_Images(**response.json())

async def async_get_images_v1(
        httpx_async_client:httpx.AsyncClient,
        limit: None | List[int] = None, # The number of results to be returned per page. This can be a number between 0 and 200. By default, each page will return 100 results.
        postId: None | List[int] = None, # The ID of a post to get images from
        modelId: None | List[int] = None, # The ID of a model to get images from (model gallery)
        modelVersionId: None | List[int] = None, # The ID of a model version to get images from (model gallery filtered to version)
        username: None | List[str] = None, # Filter to images from a specific user
        nsfw: None | List[NsfwLevel] = None, # Filter to images that contain mature content flags or not (undefined returns all)
        sort: None | List[Sort] = None, # The order in which you wish to sort the results
        period: None | List[Period] = None, # The time frame in which the images will be sorted
        page: None | List[int] = None, # The page from which to start fetching creators
) -> Response_Images:
    query_params = construct_query_params_from_dict(locals())
    response = await httpx_async_client.get(API_URL_V1_Images, params=query_params)
    return Response_Images(**response.json())

def get_models_v1(
        httpx_client:httpx.Client,
        limit: 	None | List[int] = None, 	# The number of results to be returned per page. This can be a number between 1 and 100. By default, each page will return 100 results
        page: 	None | List[int] = None, 	# The page from which to start fetching models
        query: 	None | List[str] = None, 	# Search query to filter models by name
        tag: 	None | List[str] = None, 	# Search query to filter models by tag
        username: 	Optional[str] = None, 	# Search query to filter models by user
        types: List[Response_Models_Type] | None = None, 	# The type of model you want to filter with. If none is specified, it will return all types
        sort: 	None | List[Sort] = None, 	# The order in which you wish to sort the results
        period: None | List[Period] = None, 	# The time frame in which the models will be sorted
        # rating: 	Optional[int], 	# (Deprecated) The rating you wish to filter the models with. If none is specified, it will return models with any rating
        favorites: None | List[bool] = None, 	# (AUTHED) Filter to favorites of the authenticated user (this requires an API token or session cookie)
        hidden: None | List[bool] = None, 	# (AUTHED) Filter to hidden models of the authenticated user (this requires an API token or session cookie)
        primaryFileOnly: None | List[bool] = None, 	# Only include the primary file for each model (This will use your preferred format options if you use an API token or session cookie)
        allowNoCredit: None | List[bool] = None, 	# Filter to models that require or don't require crediting the creator
        allowDerivatives: None | List[bool] = None, 	# Filter to models that allow or don't allow creating derivatives
        allowDifferentLicenses: None | List[bool] = None, # Filter to models that allow or don't allow derivatives to have a different license
        allowCommercialUse: List[AllowCommercialUse] | None = None, 	# Filter to models based on their commercial permissions
        nsfw: None | List[bool] = None, # If false, will return safer images and hide models that don't have safe images
        supportsGeneration: None | List[bool] = None 	# If true, will return models that support generation
) -> Response_Models:
    if (favorites or hidden):
        if not (httpx_client.headers):
            raise ValueError("If the \'favorites\' and the \'hidden\' params were set, The api_key must be provided while initialize CivitaiAPI class.")
            
    query_params = construct_query_params_from_dict(locals())
    response = httpx_client.get(API_URL_V1_Models, params=query_params)
    return Response_Models(**response.json())

async def async_get_models_v1(
        httpx_async_client:httpx.AsyncClient,
        limit: 	None | List[int] = None, 	# The number of results to be returned per page. This can be a number between 1 and 100. By default, each page will return 100 results
        page: 	None | List[int] = None, 	# The page from which to start fetching models
        query: 	None | List[str] = None, 	# Search query to filter models by name
        tag: 	None | List[str] = None, 	# Search query to filter models by tag
        username: 	Optional[str] = None, 	# Search query to filter models by user
        types: List[Response_Models_Type] | None = None, 	# The type of model you want to filter with. If none is specified, it will return all types
        sort: 	None | List[Sort] = None, 	# The order in which you wish to sort the results
        period: None | List[Period] = None, 	# The time frame in which the models will be sorted
        # rating: 	Optional[int], 	# (Deprecated) The rating you wish to filter the models with. If none is specified, it will return models with any rating
        favorites: None | List[bool] = None, 	# (AUTHED) Filter to favorites of the authenticated user (this requires an API token or session cookie)
        hidden: None | List[bool] = None, 	# (AUTHED) Filter to hidden models of the authenticated user (this requires an API token or session cookie)
        primaryFileOnly: None | List[bool] = None, 	# Only include the primary file for each model (This will use your preferred format options if you use an API token or session cookie)
        allowNoCredit: None | List[bool] = None, 	# Filter to models that require or don't require crediting the creator
        allowDerivatives: None | List[bool] = None, 	# Filter to models that allow or don't allow creating derivatives
        allowDifferentLicenses: None | List[bool] = None, # Filter to models that allow or don't allow derivatives to have a different license
        allowCommercialUse: List[AllowCommercialUse] | None = None, 	# Filter to models based on their commercial permissions
        nsfw: None | List[bool] = None, # If false, will return safer images and hide models that don't have safe images
        supportsGeneration: None | List[bool] = None 	# If true, will return models that support generation
) -> Response_Models:
    if (favorites or hidden):
        if not (httpx_async_client.headers):
            raise ValueError("If the \'favorites\' and the \'hidden\' params were set, The api_key must be provided while initialize CivitaiAPI class.")
            
    query_params = construct_query_params_from_dict(locals())
    response = await httpx_async_client.get(API_URL_V1_Models, params=query_params)
    return Response_Models(**response.json())

def get_model_by_id_v1(
        httpx_client:httpx.Client,
        modelId: int
) -> Response_Model_ById:
    response = httpx_client.get(urljoin(API_URL_V1_Model_By_Id, str(modelId)))
    return Response_Model_ById(**response.json())

async def async_get_model_by_id_v1(
        httpx_async_client:httpx.AsyncClient,
        modelId: int
) -> Response_Model_ById:
    response = await httpx_async_client.get(urljoin(API_URL_V1_Model_By_Id, str(modelId)))
    return Response_Model_ById(**response.json())

def get_model_by_versionId_v1(
        httpx_client:httpx.Client,
        modelVersionId: int
) -> Response_Models_modelVersion:
    response = httpx_client.get(urljoin(API_URL_ModelVersion_By_VersionId, str(modelVersionId)))
    return Response_Models_modelVersion(**response.json())

async def async_get_model_by_versionId_v1(
        httpx_async_client:httpx.AsyncClient,
        modelVersionId: int
) -> Response_Models_modelVersion:
    response = await httpx_async_client.get(urljoin(API_URL_ModelVersion_By_VersionId, str(modelVersionId)))
    return Response_Models_modelVersion(**response.json())

def get_model_by_hash_v1(
        httpx_client:httpx.Client,
        hash: str
) -> Response_Models_modelVersion:
    response = httpx_client.get(urljoin(API_URL_ModelVersion_By_Hash, hash))
    return Response_Models_modelVersion(**response.json())

async def async_get_model_by_hash_v1(
        httpx_async_client:httpx.AsyncClient,
        hash: str
) -> Response_Models_modelVersion:
    response = await httpx_async_client.get(urljoin(API_URL_ModelVersion_By_Hash, hash))
    return Response_Models_modelVersion(**response.json())
