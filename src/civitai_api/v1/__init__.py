import httpx
from urllib.parse import urljoin
from typing import Any, List, Dict, Type, TypeVar

from .models.models import Models_API_Opts, Response_Models, Response_Models_modelVersion
from .models.models_by_id import Response_Model_ById
from .models.creators import Creators_API_Opts, Response_Creaters
from .models.images import Images_API_Opts, Response_Images
from .models.tags import Response_Tags, Tags_API_Opts
# API endpoints references: https://github.com/civitai/civitai/wiki/REST-API-Reference

API_URL_V1 = "https://civitai.com/api/v1/"
API_URL_V1_Creators = urljoin(API_URL_V1, "creators") # https://civitai.com/api/v1/creators
API_URL_V1_Images = urljoin(API_URL_V1, "images") # https://civitai.com/api/v1/images
API_URL_V1_Models = urljoin(API_URL_V1, "models") # https://civitai.com/api/v1/models
API_URL_V1_Model_By_Id = urljoin(API_URL_V1, "models/") # "https://civitai.com/api/v1/models/:modelId"
API_URL_ModelVersion_By_VersionId = urljoin(API_URL_V1, "model-versions/")  # "https://civitai.com/api/v1/model-versions/:modelVersionId"
API_URL_ModelVersion_By_Hash = urljoin(API_URL_V1, "model-versions/by-hash/") # "https://civitai.com/api/v1/model-versions/by-hash/:hash"
API_URL_Tags = urljoin(API_URL_V1, "tags") # https://civitai.com/api/v1/tags

class QueryParamsError(Exception):
    def __init__(self, response_json: str):
        self.response_json = response_json

    def __str__(self):
        return f"{self.response_json}"
T = TypeVar('T')

def response_check(response: httpx.Response, response_type: Type[T]) -> T:
    obj = response.json()
    if hasattr(obj, "items"):
        return response_type(**obj)
    else:
        raise QueryParamsError(response.text)

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
    result = response_check(response, Response_Creaters)
    return result

async def async_creators(
        httpx_async_client:httpx.AsyncClient,
        opts: Creators_API_Opts | None = None
        ) -> Response_Creaters:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await httpx_async_client.get(API_URL_V1_Creators, params=query_params)
    result = response_check(response, Response_Creaters)
    return result

def images(
        httpx_client:httpx.Client,
        opts: Images_API_Opts | None = None
        ) -> Response_Images:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx_client.get(API_URL_V1_Images, params=query_params)
    result = response_check(response, Response_Images)
    return result

async def async_images(
        httpx_async_client:httpx.AsyncClient,
        opts: Images_API_Opts | None = None
) -> Response_Images:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await httpx_async_client.get(API_URL_V1_Images, params=query_params)
    result = response_check(response, Response_Images)
    return result

def models(
        httpx_client:httpx.Client,
        opts: Models_API_Opts | None = None
) -> Response_Models:
    if (opts):
        if (opts.favorites or opts.hidden):
            if not (httpx_client.headers):
                raise ValueError("If the \'favorites\' and the \'hidden\' params were set, The api_key must be provided while initialize CivitaiAPI class.")
            
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx_client.get(API_URL_V1_Models, params=query_params)
    result = response_check(response, Response_Models)
    return result

async def async_models(
        httpx_async_client:httpx.AsyncClient,
        opts: Models_API_Opts | None = None
) -> Response_Models:
    if (opts):
        if (opts.favorites or opts.hidden):
            if not (httpx_async_client.headers):
                raise ValueError("If the \'favorites\' and the \'hidden\' params were set, The api_key must be provided while initialize CivitaiAPI class.")
            
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await httpx_async_client.get(API_URL_V1_Models, params=query_params)
    result = response_check(response, Response_Models)
    return result

def get_model_by_id(
        httpx_client:httpx.Client,
        modelId: int
) -> Response_Model_ById:
    response = httpx_client.get(urljoin(API_URL_V1_Model_By_Id, str(modelId)))
    obj = response.json()
    if hasattr(obj, "error"):
        FileNotFoundError(obj)
    return Response_Model_ById(**obj)

async def async_get_model_by_id(
        httpx_async_client:httpx.AsyncClient,
        modelId: int
) -> Response_Model_ById:
    response = await httpx_async_client.get(urljoin(API_URL_V1_Model_By_Id, str(modelId)))
    obj = response.json()
    if hasattr(obj, "error"):
        FileNotFoundError(obj)
    return Response_Model_ById(**obj)

def get_model_by_versionId(
        httpx_client:httpx.Client,
        modelVersionId: int
) -> Response_Models_modelVersion:
    response = httpx_client.get(urljoin(API_URL_ModelVersion_By_VersionId, str(modelVersionId)))
    obj = response.json()
    if hasattr(obj, "error"):
        FileNotFoundError(obj)
    return Response_Models_modelVersion(**obj)

async def async_get_model_by_versionId(
        httpx_async_client:httpx.AsyncClient,
        modelVersionId: int
) -> Response_Models_modelVersion:
    response = await httpx_async_client.get(urljoin(API_URL_ModelVersion_By_VersionId, str(modelVersionId)))
    obj = response.json()
    if hasattr(obj, "error"):
        FileNotFoundError(obj)
    return Response_Models_modelVersion(**obj)

def get_model_by_hash(
        httpx_client:httpx.Client,
        hash: str
) -> Response_Models_modelVersion:
    response = httpx_client.get(urljoin(API_URL_ModelVersion_By_Hash, hash))
    obj = response.json()
    if hasattr(obj, "error"):
        FileNotFoundError(obj)
    return Response_Models_modelVersion(**obj)

async def async_get_model_by_hash(
        httpx_async_client:httpx.AsyncClient,
        hash: str
) -> Response_Models_modelVersion:
    response = await httpx_async_client.get(urljoin(API_URL_ModelVersion_By_Hash, hash))
    obj = response.json()
    if hasattr(obj, "error"):
        FileNotFoundError(obj)
    return Response_Models_modelVersion(**obj)

def tags(
        httpx_client:httpx.Client,
        opts: Tags_API_Opts | None = None
) -> Response_Tags:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx_client.get(API_URL_Tags, params=query_params)
    result = response_check(response, Response_Tags)
    return result

async def async_tags(
        httpx_async_client:httpx.AsyncClient,
        opts: Tags_API_Opts | None = None
) -> Response_Tags:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await httpx_async_client.get(API_URL_Tags, params=query_params)
    result = response_check(response, Response_Tags)
    return result
