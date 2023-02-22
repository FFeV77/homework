from flask import Flask, jsonify, request
from flask.views import MethodView

import model
from schema import validate_create_advert, GetAdvert
from http_errors import HttpError

from sqlalchemy.orm import Session


app = Flask('advt')
Session = Session(model.engine)


def get_advert(advert_id, session):
    response = session.get(model.Advertisement, advert_id)
    if not response:
        raise HttpError(400, f'Advertisement with id {advert_id} Not found')
    return response


@app.errorhandler(HttpError)
def error_handler(error):
    return jsonify({'message': error.message}), error.code


class AdvertView(MethodView):

    def get(self, advert_id):
        with Session as session:
            response = get_advert(advert_id, session)
            response_json = GetAdvert.from_orm(response).dict()
        return jsonify(response_json)


    def post(self):
        with Session as session:
            validated_data = validate_create_advert(request.json)
            user = session.get(model.User, 1)
            advert = model.Advertisement(
                **validated_data,
                owner_id=user.id
            )
            session.add(advert)
            session.commit()
        return jsonify({'method': 'POST', 'status': 'OK'})


    def delete(self, advert_id):
        with Session as session:
            stmt = get_advert(advert_id, session)
            session.delete(stmt)
            session.commit()
        return {'method': 'DELETE', 'resonse': 'ok'}


    def patch(self, advert_id):
        with Session as session:
            stmt = get_advert(advert_id, session)
            for key, val in request.json.items():
                setattr(stmt, key, val)
            session.commit()
        return {'method': 'PATCH', 'resonse': 'ok'}


app.add_url_rule('/advert/<int:advert_id>/', view_func=AdvertView.as_view('rest_advt'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/advert/', view_func=AdvertView.as_view('post_advt'), methods=['POST'])