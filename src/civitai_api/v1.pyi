import httpx
from .models.creators import Creators_API_Opts as Creators_API_Opts, Response_Creaters as Response_Creaters
from .models.images import Images_API_Opts as Images_API_Opts, Response_Images as Response_Images
from .models.models import Models_API_Opts as Models_API_Opts, Response_Models as Response_Models, Response_Models_modelVersion as Response_Models_modelVersion
from .models.models_by_id import Response_Model_ById as Response_Model_ById
from .models.tags import Response_Tags as Response_Tags, Tags_API_Opts as Tags_API_Opts
from _typeshed import Incomplete as Incomplete
from typing import Any, TypeVar

API_URL_V1: str
API_URL_V1_Creators: Incomplete
API_URL_V1_Images: Incomplete
API_URL_V1_Models: Incomplete
API_URL_V1_Model_By_Id: Incomplete
API_URL_ModelVersion_By_VersionId: Incomplete
API_URL_ModelVersion_By_Hash: Incomplete
API_URL_Tags: Incomplete

class QueryParamsError(Exception):
    response_json: Incomplete
    def __init__(self, response_json: str) -> None: ...
T = TypeVar('T')

def response_check_for_multi_results(response: httpx.Response, response_type: type[T]) -> T: ...
def response_check_for_single_result(response: httpx.Response, response_type: type[T]) -> T: ...
def construct_query_params_from_dict(params: dict[str, list[Any]]): ...
def creators(httpx_client: httpx.Client, opts: Creators_API_Opts | None = None) -> Response_Creaters: ...
async def async_creators(httpx_async_client: httpx.AsyncClient, opts: Creators_API_Opts | None = None) -> Response_Creaters: ...
def images(httpx_client: httpx.Client, opts: Images_API_Opts | None = None) -> Response_Images: ...
async def async_images(httpx_async_client: httpx.AsyncClient, opts: Images_API_Opts | None = None) -> Response_Images: ...
def models(httpx_client: httpx.Client, opts: Models_API_Opts | None = None) -> Response_Models: ...
async def async_models(httpx_async_client: httpx.AsyncClient, opts: Models_API_Opts | None = None) -> Response_Models: ...
def get_model_by_id(httpx_client: httpx.Client, modelId: int) -> Response_Model_ById: ...
async def async_get_model_by_id(httpx_async_client: httpx.AsyncClient, modelId: int) -> Response_Model_ById: ...
def get_model_by_versionId(httpx_client: httpx.Client, modelVersionId: int) -> Response_Models_modelVersion: ...
async def async_get_model_by_versionId(httpx_async_client: httpx.AsyncClient, modelVersionId: int) -> Response_Models_modelVersion: ...
def get_model_by_hash(httpx_client: httpx.Client, hash: str) -> Response_Models_modelVersion: ...
async def async_get_model_by_hash(httpx_async_client: httpx.AsyncClient, hash: str) -> Response_Models_modelVersion: ...
def tags(httpx_client: httpx.Client, opts: Tags_API_Opts | None = None) -> Response_Tags: ...
async def async_tags(httpx_async_client: httpx.AsyncClient, opts: Tags_API_Opts | None = None) -> Response_Tags: ...
