import requests
import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

bp_anime = Blueprint('anime',__name__)
api = Api(bp_anime)

class AnimeResource(Resource):
    host = 'https://api.jikan.moe/v3/search/anime'

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('mood', location='args', required=True,choices=('galau', 'sedih' , 'senang' , 'inlove' , 'depresi'))
        parser.add_argument('max_eps', location='args', type=int, default=1000)
        parser.add_argument('limit', location='args', type=int, default=5)

        args = parser.parse_args()

        mood = args['mood']
        tl = get_jwt_claims()["date"]
        usia = datetime.date.today().year-datetime.datetime.strptime(tl,'%d-%m-%Y').date().year 
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
        
        daftar_genre = {
            1 : "action",
            2 : "adventure",
            4 : "comedy",
            8 : "drama",
            13 : "historical",
            10 : "fantasy",
            18 : "mecha",
            20 : "parody",
            22 : "romance",
            24 : "sci-fi",
            36 : "slice 0f life"
        }
        

        hasil=[]
        id_hasil=[]
        score_anime=[]
        for genre in genres:
            param = {
                'genre' : genre,
                'rated' : rated,
                'limit' :limit,
                'order_by' : 'score'
            }
            tembak = requests.get(self.host,params=param)
            quote = requests.get('https://warm-mesa-82751.herokuapp.com/api/quotes')
            quote = quote.json()

            calon = tembak.json()
            for anime in calon["results"]:
                if anime["mal_id"] not in id_hasil and anime["episodes"]<= max_eps:
                    animenya = {"judul" : anime["title"], "score" : anime["score"], "genre":daftar_genre[genre], "url":anime["url"]}
                    hasil.append(animenya)
                    id_hasil.append(anime["mal_id"])
                    score_anime.append(animenya["score"])

        
        n = len(hasil)
 
        for i in range(n):
 
            for j in range(0, n-i-1):
 
                if score_anime[j] < score_anime[j+1] :
                    hasil[j], hasil[j+1] = hasil[j+1], hasil[j]
                    score_anime[j], score_anime[j+1] = score_anime[j+1], score_anime[j]        

        return {"quotes": quote["quo"]+"~~"+quote["character"]+"-"+quote["anime"], "your result":hasil[:limit]}, 200
    

api.add_resource(AnimeResource,'')        




