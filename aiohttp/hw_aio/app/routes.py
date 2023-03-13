from views import AdvertisementView, UserView
from aiohttp import web


def setup_routes(app):
    user_handler = UserView()
    
    app.add_routes([
        web.get('/advert/{item_id:\d+}', AdvertisementView),
        web.post('/advert', AdvertisementView),
        web.patch('/advert/{item_id:\d+}', AdvertisementView),
        web.delete('/advert/{item_id:\d+}', AdvertisementView),
    ])
    app.add_routes([
        web.post('/user/register', user_handler.register),
        web.post('/user/login', user_handler.login),
        web.post('/user/logout', user_handler.logout),
    ])
