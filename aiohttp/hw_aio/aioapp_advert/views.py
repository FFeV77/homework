from aiohttp.web import View, json_response
from aiohttp_security import (authorized_userid, check_authorized,
                              check_permission, forget, remember)

from aioapp_advert.model import Advertisement, Session, User
from aioapp_advert.schema import (ValidateGetItem, validate_create_item,
                                  validate_create_user)
from aioapp_advert.security import check_password_hash, generate_password_hash


class AdvertisementView(View):

    async def get(self):
        item_id = self.request.match_info['item_id']

        async with Session() as sess:
            stmt = await Advertisement.get(item_id, sess)
            serialized = ValidateGetItem.from_orm(stmt).json()
        return json_response(serialized)

    async def post(self):
        await check_authorized(self.request)
        user_id = await authorized_userid(self.request)
        data = await self.request.json()
        data['owner_id'] = int(user_id)
        validated_data = validate_create_item(data)

        async with Session() as sess:
            await Advertisement.add(validated_data, sess)
        return json_response({'method': 'post', 'status': 'OK'})

    async def delete(self):
        await check_authorized(self.request)
        item_id = self.request.match_info['item_id']

        async with Session() as sess:
            stmt = await Advertisement.get(item_id, sess)
            await check_permission(self.request, str(stmt.owner_id))
            await Advertisement.delete(stmt, sess)
        return json_response({'method': 'delete', 'status': 'ok'})

    async def patch(self):
        await check_authorized(self.request)
        data = await self.request.json()
        item_id = self.request.match_info['item_id']

        async with Session() as sess:
            stmt = await Advertisement.get(item_id, sess)
            await check_permission(self.request, str(stmt.owner_id))
            await Advertisement.patch(stmt, data, sess)
        return json_response({'method': 'patch', 'status': 'ok'})


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
        return json_response({'status': 'ok', 'message': 'user registered'})

    async def login(self, request):
        data = await request.json()

        async with Session() as sess:
            user = await User.get(sess, data["name"])
            if check_password_hash(data["pwd"], user.pwd):
                response = json_response({"status": "ok", 'message': 'authorized'})
                await remember(request, response, str(user.id))
                return response
            return json_response({'status': 'error', 'message': 'not permitted for user'})

    async def logout(self, request):
        response = json_response({'status': 'ok', 'message': 'user logout'})
        await forget(request, response)
        return response
