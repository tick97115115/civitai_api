from dotenv import load_dotenv
from civitai_api.api import CivitaiAPI
import pytest
import anyio
import os
pytestmark = pytest.mark.anyio

load_dotenv()

proxy = os.environ.get('PROXY', None)
api_key = os.environ.get('API_KEY', None)

@pytest.fixture
def client():
    return CivitaiAPI(proxy=proxy, api_key=api_key)

class TestCivitaiAPI_V1:
    def test_get_creatros(self, client):
        response = client.get_creators_v1()
        assert True

class TestCivitaiAPI_V1_Async:
    async def test_async_get_creators(self, client):
        response = await client.async_get_creators_v1()
        assert True