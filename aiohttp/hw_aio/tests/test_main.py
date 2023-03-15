import pytest

from aioapp_advert.main import init

URL = '0.0.0.0'
PORT = '8080'
link = ''.join(['http://', URL, ':', PORT])


@pytest.fixture
async def client(aiohttp_client):
    app = await init()
    # async with aiohttp_client(app) as client:
    #     yield client
    return await aiohttp_client(app)


# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#         ["json", "expected_code"],
#         (
#             ({"name": "seven", "pwd": "test"}, 200),
#             ({"name": "wrong", "pwd": "test"}, 200),
#             ({"name": "seven", "pwd": "wrong"}, 200),
#             ({"name": None, "pwd": None}, 400),
#         )
# )
# async def test_login_paramed(client, json, expected_code):
#     response = await (await client).post('/user/login', json=json)
#     assert response.status == expected_code


@pytest.mark.asyncio
async def test_login(aiohttp_client):
    client = await aiohttp_client(await init())
    response = await client.post('/user/login', json={"name": "seven", "pwd": "test"})
    assert response.status == 200
    response = await client.post('/user/login', json={"name": "wrong", "pwd": "test"})
    assert response.status == 200
    response = await client.post('/user/login', json={"name": "seven", "pwd": "wrong"})
    assert response.status == 200
    response = await client.post('/user/login', json={"name": None, "pwd": None})
    assert response.status == 400


@pytest.mark.asyncio
async def test_patch(aiohttp_client):
    client = await aiohttp_client(await init())
    # client.app['user_id'] = 6
    response = await client.post('/advert', json={"description": "five desc"})
    assert response.status == 200
