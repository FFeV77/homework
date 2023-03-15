from datetime import datetime

from aiohttp.web import HTTPBadRequest
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError


class ValidateLoginUser(BaseModel):

    name: str
    pwd: str


class ValidateCreateUser(BaseModel):

    name: str
    email: str
    pwd: str


class ValidateCreateItem(BaseModel):

    title: str
    description: str
    owner_id: int


class ValidateGetItem(BaseModel):

    id: int
    title: str
    description: str
    date: datetime
    owner_id: int

    class Config:
        orm_mode = True


def validate_create_item(data):
    try:
        advert = ValidateCreateItem(**data)
        return advert.dict()
    except ValidationError as er:
        raise HTTPBadRequest(text=er.json())


async def validate_create_user(data):
    try:
        user = ValidateCreateUser(**data)
        return user.dict()
    except ValidationError as er:
        raise HTTPBadRequest(text=er.json())


async def validate_login_user(data):
    try:
        user = ValidateLoginUser(**data)
        return user.dict()
    except ValidationError as er:
        raise HTTPBadRequest(text=er.json())
