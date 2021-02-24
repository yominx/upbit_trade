import os
import jwt
import uuid
import hashlib
import json
import userInfo
from urllib.parse import urlencode

def makeToken(access_key, secret_key, query=None):
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }
    if query != None:
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        payload['query_hash'] = query_hash
        payload['query_hash_alg'] = 'SHA512'
        
    encoded_token = jwt.encode(payload, secret_key,'HS512').encode()
    jwt_token = encoded_token.decode('utf-8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    return headers
