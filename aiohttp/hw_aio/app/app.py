from aiohttp.web import Application, run_app
from aiohttp_security import setup as setup_policy, CookiesIdentityPolicy
from aiohttp_session import session_middleware, SimpleCookieStorage

from routes import setup_routes
from security import SimplePolicy


def init():
    middleware = session_middleware(SimpleCookieStorage())
    app = Application(middlewares=[middleware])
    setup_policy(app, CookiesIdentityPolicy(), SimplePolicy())
    setup_routes(app)
    return app


run_app(init())
