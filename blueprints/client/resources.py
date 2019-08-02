from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Clients
from sqlalchemy import desc
from blueprints import app, db, internal_required
from flask_jwt_extended import jwt_required

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):
    def __init__(self):
        pass
    
    @internal_required
    def get(self, id): # get by id
        qry = Clients.query.get(id)
        if qry is not None:
            return marshal(qry, Clients.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'Client Not Found'}, 404, {'Content-Type': 'application/json'}

    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json')
        parser.add_argument('client_secret', location='json')
        parser.add_argument('birth_date', location='json')
        data = parser.parse_args()

        client = Clients(data['client_key'], data['client_secret'], data['birth_date'])
        db.session.add(client)
        db.session.commit()

        app.logger.debug('DEBUG : %s', client)

        return marshal(client, Clients.response_fields), 200, {'Content-Type': 'application/json'}

    @internal_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json')
        parser.add_argument('client_secret', location='json')
        parser.add_argument('birth_date', location='json')
        args = parser.parse_args()

        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'Client Not Found'}, 404, {'Content-Type': 'application/json'}

        qry.client_key = args['client_key']
        qry.client_secret = args['client_secret']
        qry.birth_date = args['birth_date']
        db.session.commit()

        return marshal(qry, Clients.response_fields), 200, {'Content-Type': 'application/json'}

    @internal_required
    def delete(self, id):
        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'Client Not Found'}, 404, {'Content-Type': 'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'Client Deleted'}, 200, {'Content-Type': 'application/json'}

    def patch(self):
        return 'Not yet implemented', 501

class ClientList(Resource):

    def __init__(self):
        pass


    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Clients.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Clients.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(ClientList, '')
api.add_resource(ClientResource, '', '/<id>')
