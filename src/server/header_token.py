from datetime import datetime, timedelta
import secrets
import jwt


class TokenGenerator:
    def __init__(self):
        self._secret = secrets.token_urlsafe()

    def make_token(self, username):
        expiration = datetime.now() + timedelta(hours=1)
        payload = {
            'user': username,
            'expiration': expiration.timestamp()
        }
        token = jwt.encode(payload=payload, key=self._secret, algorithm="HS256")
        return token

    def check_token(self, token):
        try:
            payload = jwt.decode(token, key=self._secret, algorithms="HS256")
            user = payload['user']
            expiration = payload['expiration']
            if datetime.now().timestamp() > expiration:
                return False
            return user
        except Exception:
            return False


