from datetime import datetime
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from http_errors import HttpError


class CreateAdvert(BaseModel):

    title: str
    description: str


class GetAdvert(BaseModel):

    id: int
    title: str
    description: str
    date: datetime
    owner_id: int

    class Config:
        orm_mode = True


def validate_create_advert(data):
    try:
        advert = CreateAdvert(**data)
        return advert.dict()
    except ValidationError as er:
        raise HttpError(400, er.errors())
    

print(validate_create_advert({'title': 'second', 'description': 1}))