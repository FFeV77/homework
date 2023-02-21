import asyncio
from datetime import datetime
from aiohttp import ClientSession
# import models


# Session = models.Session_db

async def get_person(id, session):
    print(f'Загрузка id {id} начато')
    async with session.get(f'https://swapi.dev/api/people/{id}/') as response:
        person_json = await response.json()
        person_json['id'] = id
        print(f'Зазгрузка id {id} завершено')
        return person_json


async def get_people(people_range):
    async with ClientSession() as session:
        for i in range(1, people_range):
            coros = [get_person(id, session) for id in range(1, people_range + 1)]
            results = await asyncio.gather(*coros)
            print(f'Скачивание группы из {people_range} завершено!')
            await session.close()
            return results


async def main():
    people = await get_people(3)
    # asyncio.create_task(add_to_db(people))


async def add_to_db(result):
    async with models.Session_db() as session:
        async with session.begin():
            # people_list = []
            for item in result:
                print(f"{item['id']} отправлено в БД")
                people = models.People(
                    id = item['id'],
                    birth_year = str(item['birth_year']),
                    eye_color = str(item['eye_color']),
                    gender = str(item['gender']),
                    hair_color = str(item['hair_color']),
                    height = str(item['height']),
                    homeworld = str(item['homeworld']),
                    mass = str(item['mass']),
                    name = str(item['name']),
                    skin_color = str(item['skin_color']),
                    films = str(item['films']),
                    species = str(item['species']),
                    starships = str(item['starships']),
                    vehicles = str(item['vehicles']),
                )
                # people_list.append(people)
                session.add(people)
                print(f"{people} отправлено в БД")
                print(f"Cохранено в БД")
            await session.commit()


def serialaizer(data):
    ...


if __name__ == '__main__':
    start = datetime.now()
    data =asyncio.run(main())
    # print(data)
    print(datetime.now() - start)

