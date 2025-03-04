import pytest
import httpx
import os
pytestmark = pytest.mark.anyio

from src.civitai_api.v1 import creators, async_creators, images, async_images
from src.civitai_api.v1.models.creators import Response_Creaters, Creators_API_Opts
from src.civitai_api.v1.models.images import Images_API_Opts, Response_Images
from dotenv import load_dotenv
load_dotenv()
proxy = os.environ.get('PROXY', None)
api_key = os.environ.get('API_KEY', None)
print(f"Proxy: {proxy}")
print(f"API Key: {api_key}")

@pytest.fixture
def httpx_client():
    with httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy) as client:
        yield client

@pytest.fixture
async def httpx_async_client():
    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy) as async_client:
        yield async_client

@pytest.fixture
def creators_request_queru_params():
    return Creators_API_Opts(limit=[20], page=[1], query=["Elesico"])

@pytest.fixture
def images_request_query_params():
    from src.civitai_api.v1.models.images import NsfwLevel, Sort, Period
    return Images_API_Opts(limit=[2], postId=[9178972], modelId=[949620], modelVersionId=[1063193], username=["Elesico"], nsfw=[NsfwLevel.X], sort=[Sort.Newest], period=[Period.AllTime], page=[2], total=[api_key])

class TestAPI_V1:
    def test_creators(self, httpx_client, creators_request_queru_params):
        query_params = creators_request_queru_params
        response = creators(httpx_client)
        for item in response.items:
            if item.username == "Elesico":
                assert item.link == "https://civitai.com/api/v1/models?username=Elesico"
    
    async def test_async_creators(self, httpx_async_client, creators_request_queru_params):
        query_params = creators_request_queru_params
        response = await async_creators(httpx_async_client)
        for item in response.items:
            if item.username == "Elesico":
                assert item.link == "https://civitai.com/api/v1/models?username=Elesico"

    def test_images(self, httpx_client, images_request_query_params):
        response = images(httpx_client, images_request_query_params)
        assert len(response.items) == 2
        assert response.metadata.pageSize == 2
        assert response.metadata.currentPage == 2

    async def test_async_images(self, httpx_async_client, images_request_query_params):
        response = await async_images(httpx_async_client, images_request_query_params)
        assert len(response.items) == 2
        assert response.metadata.pageSize == 2
        assert response.metadata.currentPage == 2