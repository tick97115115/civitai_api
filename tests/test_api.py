
from civitai_api.api import CivitaiAPI
import pytest
import anyio
pytestmark = pytest.mark.anyio


proxy = "http://127.0.0.1:17890"
api_key = "d250ad5b931cd1ab4895b66ae2d42149"


# client = CivitaiAPI(proxy=proxy, api_key=api_key)
@pytest.fixture
def client():
    return CivitaiAPI(proxy=proxy, api_key=api_key)

class TestCivitaiAPI_V1:
    def test_get_creatros(self, client):
        response = client.get_creators_v1()
        assert True

class TestCivitaiAPI_V1_Async:
    async def test_async_get_creatros(self, client):
        response = await client.async_get_creators_v1()
        assert True