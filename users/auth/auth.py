from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from config import conf

cookie_transport = CookieTransport(
    cookie_name="space_stats",
    cookie_max_age=3600
)

SECRET = conf.auth.jwt_token


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
