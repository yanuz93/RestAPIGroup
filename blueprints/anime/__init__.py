import requests
import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required


bp_anime = Blueprint('anime',__name__)
api = Api(bp_anime)

class AnimeResource(Resource):
    host = 'https://api.jikan.moe/v3/search/anime'
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('mood', location='args', required=True,choices=('galau', 'sedih' , 'senang' , 'inlove' , 'depresi'))
        parser.add_argument('usia', location='args', type=int, required=True)
        parser.add_argument('max_eps', location='args', type=int, default=30)
        parser.add_argument('limit', location='args', type=int, default=5)

        args = parser.parse_args()

        mood = args['mood']
        usia = args['usia'] 
        max_eps = args['max_eps']
        limit = args['limit']
        
        if usia >=21:
            rated='r'
        elif usia >= 17:
            rated='r17'
        elif usia >= 13:
            rated='pg13'
        else:
            rated='pg'
        
        if mood == 'galau':
            genres = [22,8,36]
        elif mood == 'sedih':
            genres = [20,4,10]
        elif mood == 'senang':
            genres = [1, 13, 18]
        elif mood == 'inlove':
            genres = [2,8,22]
        elif mood == 'depresi':
            genres = [24, 4, 2]
        

        hasil=[]
        id_hasil=[]
        for genre in genres:
            param = {
                'genre' : genre,
                'rated' : rated,
                'limit' :limit,
                'order_by' : 'score'
            }
            tembak = requests.get(self.host,params=param)

            calon = tembak.json()
            for anime in calon["results"]:
                if anime["mal_id"] not in id_hasil and anime["episodes"]<= max_eps:
                    hasil.append(anime)
                    id_hasil.append(anime["mal_id"])


        return hasil[:limit], 200
    

api.add_resource(AnimeResource,'')        




