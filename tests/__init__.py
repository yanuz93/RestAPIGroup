import pytest, json, logging
from flask import Flask, request

from blueprints import app
from app import cache

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture

def client(request):
    return call_client(request)

# def create_token_int():
#     token = cache.get('test-token-int')
#     # supaya tokennya bisa diambil lagi
#     if token is None:
#         data = {
#             'client_key' : 'internal',
#             'client_secret' : 'th1s1s1nt3rn4lcl13nt'
#         }
#         # do request
#         req = call_client(request)
#         res = req.get('/auth', query_string=data,content_type='application/json')

#         # store response
#         res_json = json.loads(res.data)

#         logging.warning('RESULT : %s', res_json )
#         # assert if the result is as expected
#         assert res.status_code == 200

#         # save token into cache
#         cache.set('test_token-int',res_json['token'], timeout=60)

#         return res_json['token']
#     else:
#         return token
