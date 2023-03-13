from aiohttp import web
from aiohttp_security import AbstractAuthorizationPolicy, forget, remember
from sqlalchemy import select

from model import Session, User
from schema import validate_create_user
from security import generate_password_hash, check_password_hash


class SimplePolicy(AbstractAuthorizationPolicy):
    async def authorized_userid(self, identity):
        return identity

    async def permits(self, identity, permission, context=None):
        if identity == permission:
            return True
        return False


async def user_get(sess, name):
    stmt = await sess.scalar(select(User).where(User.name == name))
    return stmt


async def user_add(sess, data):
    user = User(**data)
    sess.add(user)
    await sess.commit()


async def user_register(request):
    data = await request.json()
    validated_data = validate_create_user(data)
    validated_data['pwd'] = generate_password_hash(validated_data.get('pwd'))
    async with Session() as sess:
        stmt = await user_get(sess, validated_data['name'])
        if stmt:
            return web.json_response({'status': 'error', 'message': 'alrady exists'})
        await user_add(sess, validated_data)
    return web.json_response({'status': 'user added'})


async def user_login(request):
    async with Session() as sess:
        data = await request.json()
        user = await user_get(sess, data["name"])
        if check_password_hash(data["pwd"], user.pwd):
            response = web.json_response({"status": "authenticated", "user": str(user.id)})
            await remember(request, response, str(user.id))
            # session.update({'user': user.id})
            return response
        raise web.HTTPNotAcceptable()


async def user_logout(request):
    response = web.json_response({'status': 'not authenticated'})
    await forget(request, response)
    return response


def user_setup_routes(app):
    app.router.add_post('/user/register', user_register)
    app.router.add_post('/user/login', user_login)
    app.router.add_post('/user/logout', user_logout)
