from datetime import datetime, timedelta

import jwt

access_rights = {'admin': 'admin'}  # TODO DB table with users

secret = "Secret"  # TODO change


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


def check_token(token):
    try:
        payload = jwt.decode(token, key=secret, algorithms="HS256")
        user = payload['user']
        rights = payload['rights']
        expiration = payload['expiration']
        if datetime.now().timestamp() > expiration:
            return False
        return user, rights
    except Exception:
        # print('Invalid signature')
        return False


#print(make_token('admin'))
