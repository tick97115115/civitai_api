import httpx
from urllib.parse import urljoin
from typing import Any, List,Dict
from .models.creators import Creators_API_Opts, Response_Creaters
from .models.images import Images_API_Opts, Response_Images
# API endpoints references: https://github.com/civitai/civitai/wiki/REST-API-Reference

API_URL_V1 = "https://civitai.com/api/v1/"
API_URL_V1_Creators = urljoin(API_URL_V1, "creators") # https://civitai.com/api/v1/creators
API_URL_V1_Images = urljoin(API_URL_V1, "images") # https://civitai.com/api/v1/images
API_URL_V1_Models = urljoin(API_URL_V1, "models") # https://civitai.com/api/v1/models
API_URL_V1_Model_By_Id = urljoin(API_URL_V1, "models/") # "https://civitai.com/api/v1/models/:modelId"
API_URL_ModelVersion_By_VersionId = urljoin(API_URL_V1, "model-versions/")  # "https://civitai.com/api/v1/model-versions/:modelVersionId"
API_URL_ModelVersion_By_Hash = urljoin(API_URL_V1, "model-versions/by-hash/") # "https://civitai.com/api/v1/model-versions/by-hash/:hash"
API_URL_Tags = urljoin(API_URL_V1, "tags") # https://civitai.com/api/v1/tags

def construct_query_params_from_dict(params: Dict[str, List[Any]]):
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

def creators(
        httpx_client:httpx.Client,
        opts: Creators_API_Opts | None = None
        ) -> Response_Creaters:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx.get(API_URL_V1_Creators, params=query_params)
    return Response_Creaters(**response.json())

async def async_creators(
        httpx_async_client:httpx.AsyncClient,
        opts: Creators_API_Opts | None = None
        ) -> Response_Creaters:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await httpx_async_client.get(API_URL_V1_Creators, params=query_params)
    return Response_Creaters(**response.json())

def images(
        httpx_client:httpx.Client,
        opts: Images_API_Opts | None = None
        ) -> Response_Images:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx_client.get(API_URL_V1_Images, params=query_params)
    return Response_Images(**response.json())

async def async_images(
        httpx_async_client:httpx.AsyncClient,
        opts: Images_API_Opts | None = None
) -> Response_Images:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await httpx_async_client.get(API_URL_V1_Images, params=query_params)
    return Response_Images(**response.json())
