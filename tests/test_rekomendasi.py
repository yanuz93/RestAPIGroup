import json
from . import app, client, cache

class TestRekomendasi():


    def test_get_rekomendasi(self, client):
        # token = create_token_int()
        param = {
            "mood" : "senang",
            "usia" : 12
            }
        res = client.get('/anime',query_string=param)
        # res = client.get('/anime',params=param, headers={'Authorization': 'Bearer '+ token})

        # res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_rekomendasi_invalid(self,client):
        # token = create_token_int()
        param = {
            "mood" : "senangnyahatiku",
            "usia" : 12
            }
        res = client.get('/anime',query_string=param)
        # res = client.get('/anime',params=param, headers={'Authorization': 'Bearer '+ token})

        # res_json = json.loads(res.data)
        assert res.status_code == 400