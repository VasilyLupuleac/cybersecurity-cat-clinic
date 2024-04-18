import jwt
from datetime import datetime, timedelta

access_rights = {'admin': 'admin'}  # TODO DB table with users

secret = "Secret" # TODO change

def make_token(username):
    rights = access_rights[username]
    expiration = datetime.now() + timedelta(hours=1)
    payload = {
        'user': username,
        'rights': rights,
        'expiration': expiration.timestamp()
        # TODO more fields idk
    }
    token = jwt.encode(payload=payload, key=secret, algorithm="HS256")
    return token


t = make_token('admin')


def check_token(token):
    try:
        payload = jwt.decode(t, key=secret, algorithms="HS256")
        user = payload['user']
        rights = payload['rights']
        expiration = payload['expiration']
        if datetime.now().timestamp() > expiration:
            return False
        return user, rights
    except jwt.exceptions.InvalidSignatureError:
        # print('Invalid signature')
        return False


check_token(make_token('admin'))
