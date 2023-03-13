from aiohttp import web
from aiohttp_security import setup as setup_policy, CookiesIdentityPolicy
from aiohttp_session import session_middleware, SimpleCookieStorage

from advert import setup_routes
from users import SimplePolicy, user_setup_routes


def init():
    middleware = session_middleware(SimpleCookieStorage())
    app = web.Application(middlewares=[middleware])
    setup_policy(app, CookiesIdentityPolicy(), SimplePolicy())
    setup_routes(app)
    user_setup_routes(app)
    return app


web.run_app(init())
