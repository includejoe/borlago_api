import jwt as JWT
import environ

env = environ.Env()
environ.Env.read_env()


def decode_jwt(token):
    # slicing the authorization header to get jwt without "Bearer "
    jwt = token[7:]
    payload = JWT.decode(jwt, env("JWT_SECRET_KEY"), env("JWT_ALGORITHM"))
    return payload["user_id"]
