from aiohttp.web import Application, run_app
from aiohttp_security import CookiesIdentityPolicy
from aiohttp_security import setup as setup_policy
from aiohttp_session import SimpleCookieStorage, session_middleware

from aioapp_advert.routes import setup_routes
from aioapp_advert.security import SimplePolicy


async def init():
    middleware = session_middleware(SimpleCookieStorage())
    app = Application(middlewares=[middleware])
    setup_policy(app, CookiesIdentityPolicy(), SimplePolicy())
    setup_routes(app)
    return app


if __name__ == '__main__':
    run_app(init())
