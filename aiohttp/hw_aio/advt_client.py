# import asyncio
# from aiohttp import ClientSession
import requests


URL = '127.0.0.1'
PORT = '8080'
link = ''.join(['http://', URL, ':', PORT])

# async def main():
#     async with ClientSession(link) as session:
#         response = await session.get('/advert/11')
#         print(response.status)
#         print(await response.text())
#         respsonse = await session.post('/user/login', json={'name': 'six', 'pwd': 'test'})
#         print(respsonse.status)
#         print(await respsonse.text())
#         print(respsonse.headers)
#         # respsonse = await session.post('/user/register', json={'name': 'six', 'email': 'test@test.ru', 'pwd': 'test'})
#         # print(respsonse.status)
#         # print(await respsonse.text())
#         respsonse = await session.post('/advert', json={'title': 'authorized', 'description': 'first test post'})
#         print(respsonse.status)
#         print(respsonse.headers)
#         print(await respsonse.text())

# asyncio.run(main())


with requests.Session() as s:
    # respsonse = s.post(link + '/user/register', json={'name': 'seven', 'email': 'test@test.ru', 'pwd': 'test'})
    # print(respsonse.status_code)
    # print(respsonse.text)

    respsonse = s.post(link + '/user/login', json={"name": "seven", "pwd": "test"})
    print(respsonse.status_code)
    print(respsonse.text)

    respsonse = s.post(link + '/advert', json={"description": "five desc"})
    print(respsonse.status_code)
    print(respsonse.text)

    respsonse = s.get(link + '/advert/18')
    print(respsonse.status_code)
    print(respsonse.text)

    # respsonse = s.patch(link + '/advert/10', json={'description': 'new six desc'})
    # print(respsonse.status_code)
    # print(respsonse.text)

    # respsonse = s.patch(link + '/advert/19', json={'description': 'new six desc'})
    # print(respsonse.status_code)
    # print(respsonse.text)

    # respsonse = s.get(link + '/advert/19')
    # print(respsonse.status_code)
    # print(respsonse.text)

    # respsonse = s.delete(link + '/advert/15')
    # print(respsonse.status_code)
    # print(respsonse.text)

    # respsonse = s.delete(link + '/advert/19')
    # print(respsonse.status_code)
    # print(respsonse.text)

    # # respsonse = s.get(link + '/advert/17')
    # # print(respsonse.status_code)
    # # print(respsonse.text)

    respsonse = s.post(link + '/user/logout')
    print(respsonse.status_code)
    print(respsonse.text)
