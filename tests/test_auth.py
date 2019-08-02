import json
from . import app, client

class TestAuthCrud():
    def test_auth_ok(self,client):
        data ={
            "client_key":"admin",
            "client_secret" : "shinjitsuwahitotsu"
        }
        res = client.get('/auth', query_string=data,content_type='application/json')
        assert res.status_code == 200

    def test_auth_unauthor(self,client):
        data ={
            "client_key":"hatarakuhh",
            "client_secret" : "maou"
        }
        res = client.get('/auth', query_string=data,content_type='application/json')
        assert res.status_code == 401