# civitai_api

![Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen)

This project provide a easy way to communicating with Civitai-API.

It supports both Sync and Async request implementation, and both Async implementation (AsyncIO and Trio) by using Anyio.

**See usage example in : [/tests/test_v1.py](./tests/test_v1.py).**

## Intro

this was designed to be a flexale library, which only need you initialize an httpx library as the function's first argument.

To register your own api key, see [here](https://github.com/civitai/civitai/wiki/REST-API-Reference#authorization).

### initialize an httpx client (or async httpx client) and use with functions.

for Sync Clinet:

```python
import httpx

proxy = "http://127.0.0.1:7890"

# setting up your civitai api key and proxy
client = httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy)
# or 
with httpx.Client(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy) as client:
    ......
```

For Async Client:

```python
async_client = httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy)
# or 
async with httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"}, proxy = proxy) as async_client:
    ......
```

> for more info please checkout [httpx official website](https://www.python-httpx.org/advanced/clients/).

### 2. request for certain endpoint

```python
from civitai_api.v1 import models, async_models
from civitai_api.v1.models.models import Models_API_Opts, Sort, Period, Response_Models_Type, AllowCommercialUse

@pytest.fixture
def models_request_query_params():
    from civitai_api.v1.models.models import Models_API_Opts, Sort, Period, Response_Models_Type, AllowCommercialUse
    return Models_API_Opts(
        limit=[20],
        page=[1],
        query=["VSK-94 | Girls' Frontline"],
        tag=["girls_frontline"],
        username=["LeonDoesntDraw"],
        types=[Response_Models_Type.LORA],
        sort=[Sort.Newest],
        period=[Period.AllTime],
        rating=[5],
        favorites=[False],
        hidden=[False],
        primaryFileOnly=[False],
        # allowNoCredit=[True],
        # allowDerivatives=[True],
        allowDifferentLicenses=[True],
        allowCommercialUse=[AllowCommercialUse.Image, AllowCommercialUse.Rent, AllowCommercialUse.Sell],
        nsfw=[True],
        supportsGeneration=[True],
    )

# sync
def test_models(httpx_client, models_request_query_params):
    response = models(httpx_client, models_request_query_params)
    assert len(response.items) == 1
    assert response.metadata.pageSize == 20
    assert response.items[0].id == 11821

# async
async def test_async_models(httpx_async_client, models_request_query_params):
    response = await async_models(httpx_async_client, models_request_query_params)
    assert len(response.items) == 1
    assert response.metadata.pageSize == 20
    assert response.items[0].id == 11821
    
```

For a certain endpoint, there will have two functions for both sync and async implementation. And the only two differences between them were:

1. the async implementation's first argument takes async httpx client instance.
2. async implementation's function name will have 'async_' as the prefix to differenciate whether it's Sync or Async.

### 3. how to correctly write arguments

For endpoints: creators, images and models, there are 3 functions (and 3 async implementatons) takes function arguments to construct request query paramters.

and every argument value have to be enclosed by a list:

```python
opts: Images_API_Opts = Images_API_Opts(limit=[1], nsfw=[NsfwLevel.X], postId=[11059742])
response = api.get_images_v1(httpx_client,opts=opts)
```

Because that's how the httpx library construct query paramters.

> for more info: [query-parameters](https://www.python-httpx.org/compatibility/#query-parameters)

#### for some arguments those takes List[strEnum] type as input

You should always take care of when an argument takes a specific strEnum type as input.
For example the ["images"](https://github.com/civitai/civitai/wiki/REST-API-Reference#response-fields-1) endpoint can take nsfw as input, And I make every nsfw level option into a NsfwLevel strEnum type, when you want specific the nsfw level filter you should write like this: 

```python
from civitai_api.v1.models.images import NsfwLevel

......# after initialize httpx client

opts: Images_API_Opts = Images_API_Opts(limit=[1], nsfw=[NsfwLevel.X], postId=[11059742]) 
# Do This: nsfw=[NsfwLevel.X]
```

### 4. Exception handling

There are 3 types of Exception you should care of

1. QueryParamsError
    - only for the endpoints which could return multiple results.
2. FileNotFoundError
    - only for the endpoints which could return single results.
3. ConnectionAbortedError
    - every endpoint could trigger this Exception when the number of requests reach Civitai server's limitation.

```python

```
