from aiohttp.web import json_response, HTTPNotAcceptable, middleware, View
from aiohttp_security import authorized_userid, check_permission, forget, remember, check_authorized
from security import check_password_hash, generate_password_hash

from model import Session, Advertisement, User
from schema import validate_create_item, ValidateGetItem, validate_create_user


class AdvertisementView(View):

    async def get(self):
        async with Session() as sess:
            item_id = self.request.match_info['item_id']
            stmt = await Advertisement.get(item_id, sess)
            serialized = ValidateGetItem.from_orm(stmt).json()
        return json_response(serialized)

    async def post(self):
        await check_authorized(self.request)
        async with Session() as sess:
            user_id = await authorized_userid(self.request)
            data = await self.request.json()
            data['owner_id'] = int(user_id)
            validated_data = validate_create_item(data)
            await Advertisement.add(validated_data, sess)
        return json_response({'method': 'POST', 'status': 'OK'})

    async def delete(self):
        await check_authorized(self.request)
        async with Session() as sess:
            item_id = self.request.match_info['item_id']
            stmt = await Advertisement.get(item_id, sess)
            await check_permission(self.request, str(stmt.owner_id))
            await Advertisement.delete(stmt, sess)
            return json_response({'method': 'DELETE', 'resonse': 'ok'})

    async def patch(self):
        await check_authorized(self.request)
        async with Session() as sess:
            data = await self.request.json()
            item_id = self.request.match_info['item_id']
            stmt = await Advertisement.get(item_id, sess)
            await check_permission(self.request, str(stmt.owner_id))
            await Advertisement.patch(stmt, data, sess)
            return json_response({'method': 'PATCH', 'resonse': 'ok'})


class UserView:
    def _init__(self):
        pass

    async def register(self, request):
        data = await request.json()
        validated_data = validate_create_user(data)
        validated_data['pwd'] = generate_password_hash(validated_data.get('pwd'))
        async with Session() as sess:
            stmt = await User.get(sess, validated_data['name'])
            if stmt:
                return json_response({'status': 'error', 'message': 'already exists'})
            await User.add(sess, validated_data)
        return json_response({'status': 'user added'})

    async def login(self, request):
        async with Session() as sess:
            data = await request.json()
            user = await User.get(sess, data["name"])
            if check_password_hash(data["pwd"], user.pwd):
                response = json_response({"status": "authenticated", "user": str(user.id)})
                await remember(request, response, str(user.id))
                return response
            raise HTTPNotAcceptable()

    async def logout(self, request):
        response = json_response({'status': 'not authenticated'})
        await forget(request, response)
        return response
