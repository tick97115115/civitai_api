import httpx
from urllib.parse import urljoin
from typing import Any, Dict, Type, TypeVar
from pydantic import BaseModel

from .models.models import Models_API_Opts, Response_Models, Response_Model, Response_Models_modelVersion
from .models.creators import Creators_API_Opts, Response_Creaters
from .models.images import Images_API_Opts, Response_Images
from .models.tags import Tags_API_Opts, Response_Tags
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
    def __init__(self, response_json: str, *args):
        super().__init__(*args)
        self.response_json = response_json

    def __str__(self):
        return f"{self.response_json}"

class LoraNotExistsError(Exception):
    def __init__(self, response_json: str, *args):
        super().__init__(*args)
        self.response_json = response_json
    
    def __str__(self):
        return f"{self.response_json}"

class ReachRequestLimitationError(Exception):
    def __init__(self, response_json: str, *args):
        super().__init__(*args)
        self.response_json = response_json

    def __str__(self):
        return f"{self.response_json}"

T = TypeVar('T')

def response_check_for_multi_results(response: httpx.Response, response_type: Type[T]) -> T:
    obj = response.json()
    if hasattr(obj, "error"): # notice that for those api endpoints that return a single result, the error message is different
        raise QueryParamsError(response.text)
    if hasattr(obj, "message"):
        raise ReachRequestLimitationError(response.text) # Server connection limitation reached
    return response_type(**obj)

def response_check_for_single_result(response: httpx.Response, response_type: Type[T]) -> T:
    obj = response.json()
    if hasattr(obj, "error"): # only no result matches will return error msg.
        raise LoraNotExistsError(response.text)
    if hasattr(obj, "message"):
        raise ReachRequestLimitationError(response.text)
    return response_type(**obj)

def construct_query_params_from_dict(params: Dict[str, Any]):
    query_params: Dict[str, Any] = {}
    for k,v in params.items():
        if params[k] != None:
            query_params[k] = v
    return query_params

def construct_query_params_from_model(model: BaseModel):
    dictionary = model.model_dump()



def creators(
        httpx_client:httpx.Client,
        opts: Creators_API_Opts | None = None
        ) -> Response_Creaters:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx_client.get(API_URL_V1_Creators, params=query_params)
    result = response_check_for_multi_results(response, Response_Creaters)
    return result

async def async_creators(
        async_httpx_client:httpx.AsyncClient,
        opts: Creators_API_Opts | None = None
        ) -> Response_Creaters:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await async_httpx_client.get(API_URL_V1_Creators, params=query_params)
    result = response_check_for_multi_results(response, Response_Creaters)
    return result

def images(
        httpx_client:httpx.Client,
        opts: Images_API_Opts | None = None
        ) -> Response_Images:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    response = httpx_client.get(API_URL_V1_Images, params=query_params)
    result = response_check_for_multi_results(response, Response_Images)
    return result

async def async_images(
        async_httpx_client:httpx.AsyncClient,
        opts: Images_API_Opts | None = None
) -> Response_Images:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await async_httpx_client.get(API_URL_V1_Images, params=query_params)
    result = response_check_for_multi_results(response, Response_Images)
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
    result = response_check_for_multi_results(response, Response_Models)
    return result

async def async_models(
        async_httpx_client:httpx.AsyncClient,
        opts: Models_API_Opts | None = None
) -> Response_Models:
    if (opts):
        if (opts.favorites or opts.hidden):
            if not (async_httpx_client.headers):
                raise ValueError("If the \'favorites\' and the \'hidden\' params were set, The api_key must be provided while initialize CivitaiAPI class.")
            
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await async_httpx_client.get(API_URL_V1_Models, params=query_params)
    result = response_check_for_multi_results(response, Response_Models)
    return result

def get_model_by_id(
        httpx_client:httpx.Client,
        modelId: int
) -> Response_Model:
    response = httpx_client.get(urljoin(API_URL_V1_Model_By_Id, str(modelId)))
    result = response_check_for_single_result(response, Response_Model)
    return result

async def async_get_model_by_id(
        async_httpx_client:httpx.AsyncClient,
        modelId: int
) -> Response_Model:
    response = await async_httpx_client.get(urljoin(API_URL_V1_Model_By_Id, str(modelId)))
    result = response_check_for_single_result(response, Response_Model)
    return result

def get_model_by_versionId(
        httpx_client:httpx.Client,
        modelVersionId: int
) -> Response_Models_modelVersion:
    response = httpx_client.get(urljoin(API_URL_ModelVersion_By_VersionId, str(modelVersionId)))
    result = response_check_for_single_result(response, Response_Models_modelVersion)
    return result

async def async_get_model_by_versionId(
        async_httpx_client:httpx.AsyncClient,
        modelVersionId: int
) -> Response_Models_modelVersion:
    response = await async_httpx_client.get(urljoin(API_URL_ModelVersion_By_VersionId, str(modelVersionId)))
    result = response_check_for_single_result(response, Response_Models_modelVersion)
    return result

def get_model_by_hash(
        httpx_client:httpx.Client,
        hash: str
) -> Response_Models_modelVersion:
    response = httpx_client.get(urljoin(API_URL_ModelVersion_By_Hash, hash))
    result = response_check_for_single_result(response, Response_Models_modelVersion)
    return result

async def async_get_model_by_hash(
        async_httpx_client:httpx.AsyncClient,
        hash: str
) -> Response_Models_modelVersion:
    response = await async_httpx_client.get(urljoin(API_URL_ModelVersion_By_Hash, hash))
    result = response_check_for_single_result(response, Response_Models_modelVersion)
    return result

def tags(
        httpx_client:httpx.Client,
        opts: Tags_API_Opts | None = None
) -> Response_Tags:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = httpx_client.get(API_URL_Tags, params=query_params)
    result = response_check_for_multi_results(response, Response_Tags)
    return result

async def async_tags(
        async_httpx_client:httpx.AsyncClient,
        opts: Tags_API_Opts | None = None
) -> Response_Tags:
    if opts:
        query_params = construct_query_params_from_dict(opts.model_dump())
    else:
        query_params = None
    response = await async_httpx_client.get(API_URL_Tags, params=query_params)
    result = response_check_for_multi_results(response, Response_Tags)
    return result

class CiviClient:
    def __init__(self, api_key: str, httpx_client: httpx.Client = httpx.Client(), async_httpx_client: httpx.AsyncClient = httpx.AsyncClient()):
        self.httpx_client = httpx_client
        self.async_httpx_client = async_httpx_client

    def creators(self, opts: Creators_API_Opts):
        return creators(self.httpx_client, opts)

    async def async_creators(self, opts: Creators_API_Opts):
        return await async_creators(self.async_httpx_client, opts)

    def images(self, opts: Images_API_Opts):
        return images(self.httpx_client, opts)

    async def async_images(self, opts: Images_API_Opts):
        return await async_images(self.async_httpx_client, opts)

    def models(self, opts: Models_API_Opts):
        return models(self.httpx_client, opts)

    async def async_models(self, opts: Models_API_Opts):
        return await async_models(self.async_httpx_client, opts)

    def get_model_by_id(self, modelId: int):
        return get_model_by_id(self.httpx_client, modelId)

    async def async_get_model_by_id(self, modelId: int):
        return await async_get_model_by_id(self.async_httpx_client, modelId)

    def get_model_by_versionId(self, versionId: int):
        return get_model_by_versionId(self.httpx_client, versionId)

    async def async_get_model_by_versionId(self, versionId: int):
        return await async_get_model_by_versionId(self.async_httpx_client, versionId)

    def get_model_by_hash(self, hash: str):
        return get_model_by_hash(self.httpx_client, hash)
    
    async def async_get_model_by_hash(self, hash: str):
        return await async_get_model_by_hash(self.async_httpx_client, hash)
    
    def tags(self, opts: Tags_API_Opts):
        return tags(self.httpx_client, opts)
    
    async def async_tags(self, opts: Tags_API_Opts):
        return await async_tags(self.async_httpx_client, opts)
