import json
from . import app, client, cache, create_token_int, create_token_admin

class TestClientCrud():

    temp_client = 0

    def test_client_list(self, client):
        token = create_token_admin()
        res = client.get('/client', headers={'Authorization': 'Bearer '+ token})

        # res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_client_list_invalid_token(self, client):
        res = client.get('/client', headers={'Authorization': 'Bearer abc'})
        assert res.status_code == 500

    def test_client_post(self,client):
        
        inputan = {
            "client_key" : "trykey8",
            "client_secret" : "trysecret",
            "birth_date" : "23-02-2001"
        }
        res = client.post('/client', data=json.dumps(inputan), content_type='application/json')

        res_json = json.loads(res.data)
        TestClientCrud.temp_client = res_json['id']
        assert res.status_code == 200
    
    def test_client_duplicate_post(self,client):
        inputan = {
            "client_key" : "trykey8",
            "client_secret" : "trysecret",
            "birth_date" : "23-02-2001" 
        }
        res = client.post('/client', data=json.dumps(inputan), content_type='application/json')

        assert res.status_code == 500
    
    def test_client_put(self, client):
        token=create_token_admin()
        inputan = {
            "client_key" : "monyet",
            "client_secret" : "kuda",
            "birth_date" : "23-02-2001"
        }
        res = client.put('/client/'+str(TestClientCrud.temp_client), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200
    def test_client_invalid_put(self,client):
        token=create_token_admin()
        inputan = {
            "client_key" : "monyet",
            "client_secret" : "kuda",
            "birth_date" : "23-02-2001"
        }
        res = client.put('/client/baka', data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 404

    def test_client_get_one(self, client):
        token = create_token_admin()
        res = client.get('/client/'+str(TestClientCrud.temp_client), headers={'Authorization': 'Bearer '+ token})

        # res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_client_invalid_get_one(self, client):
        token = create_token_admin()
        res = client.get('/client/baka', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 404

    def test_client_delete(self,client):
        token=create_token_admin()
        res = client.delete('/client/'+str(TestClientCrud.temp_client), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200

    def test_client_invalid_delete(self,client):
        token=create_token_admin()
        res = client.delete('/client/baka', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 404