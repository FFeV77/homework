from aiohttp import web
from aiohttp_security import authorized_userid, check_permission, login_required

from model import Session, Advertisement
from schema import validate_create_item, ValidateGetItem


async def get_item(item_id, session):
    item_id = int(item_id)
    item = await session.get(Advertisement, item_id)
    if not item:
        raise web.HTTPNotFound(text='item not found')
    return item


async def add_item(data, session):
    new_item = Advertisement(**data)
    session.add(new_item)
    await session.commit()


async def patch_item(stmt, data, session):
    for key, val in data.items():
        setattr(stmt, key, val)
    await session.commit()


async def delete_item(stmt, session):
    await session.delete(stmt)
    await session.commit()


async def get(request):
    async with Session() as sess:
        item_id = request.match_info['item_id']
        stmt = await get_item(item_id, sess)
        serialized = ValidateGetItem.from_orm(stmt).json()
    return web.json_response(serialized)


@login_required
async def post(request):
    async with Session() as sess:
        user_id = await authorized_userid(request)
        data = await request.json()
        data['owner_id'] = int(user_id)
        validated_data = validate_create_item(data)
        await add_item(validated_data, sess)
    return web.json_response({'method': 'POST', 'status': 'OK'})


@login_required
async def delete(request):
    async with Session() as sess:
        item_id = request.match_info['item_id']
        stmt = await get_item(item_id, sess)
        await check_permission(request, str(stmt.owner_id))
        await delete_item(stmt, sess)
        return web.json_response({'method': 'DELETE', 'resonse': 'ok'})


@login_required
async def patch(request):
    async with Session() as sess:
        data = await request.json()
        item_id = request.match_info['item_id']
        stmt = await get_item(item_id, sess)
        await check_permission(request, str(stmt.owner_id))
        await patch_item(stmt, data, sess)
        return web.json_response({'method': 'PATCH', 'resonse': 'ok'})


def setup_routes(app):
    app.router.add_get('/advert/{item_id}', get)
    app.router.add_post('/advert', post)
    app.router.add_patch('/advert/{item_id}', patch)
    app.router.add_delete('/advert/{item_id}', delete)
