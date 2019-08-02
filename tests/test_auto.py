import json
from . import app, client

class TestAutoCrud():
    def test_auto_ok(self,client):
        data ={
            "client_key":"admin",
            "client_secret" : "shinjitsuwahitotsu",
            "mood" : 'senang',
            "limit" : 1
        }
        res = client.get('/auto', query_string=data,content_type='application/json')
        assert res.status_code == 200

    def test_auth_unauthor(self,client):
        data ={
            "client_secret" : "shinjitsuwahitotsu",
            "mood" : "galau",
            "limit" : 1
        }
        res = client.get('/auto', query_string=data,content_type='application/json')
        assert res.status_code == 500