from tests import create_token_int
import requests
import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
# from flask_jwt_extended import jwt_required, get_jwt_claims
# import datetime

bp_auto = Blueprint('auto',__name__)
api = Api(bp_auto)

class AutoResource(Resource):
    host = 'https://api.jikan.moe/v3/search/anime'

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('client_key',location='args')
        parser.add_argument('client_secret', location='args')
        parser.add_argument('mood', location='args', required=True,choices=('galau', 'sedih' , 'senang' , 'inlove' , 'depresi'))
        parser.add_argument('max_eps', location='args', type=int, default=1000)
        parser.add_argument('limit', location='args', type=int, default=5)

        args = parser.parse_args()

        key = args['client_key']
        secret = args['client_secret']
        mood = args['mood'] 
        max_eps = args['max_eps']
        limit = args['limit']

        #################
        # login
        #################

        login_data ={
            "client_key" : key,
            "client_secret" : secret
        }
        tembak_login = requests.get('http://0.0.0.0:6000/auth', params=login_data)
        token = tembak_login.json()["token"]

        ##############
        # rekomen
        #############

        data_anime = {
            "mood" : mood,
            "max_eps" : max_eps,
            "limit" : limit
        }

        tembak_rekomen = requests.get('http://0.0.0.0:6000/anime', params= data_anime,headers={'Authorization': 'Bearer '+ token})

        hasil = tembak_rekomen.json()
        return hasil,200

api.add_resource(AutoResource,'')