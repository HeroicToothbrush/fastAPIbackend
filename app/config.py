import os
from dataclasses import dataclass


@dataclass
class DBConfig:
    # db_host: str
    # db_server_port: str
    user: str = os.environ["DB_USER"]
    password: str = os.environ["DB_PASS"]
    name: str = os.environ["DB_NAME"]
    instance_connection_name: str = os.environ["INSTANCE_CONNECTION_NAME"]
    socket_dir: str = "/cloudsql"

@dataclass
class AuthConfig:
    # to get a string like this run:
# openssl rand -hex 32
    # todo move to secrets
    SECRET_KEY = "5dcacb58f1f4ad2c857343564e7ab4f9155ea65624973318f43f1f4bef8a3015"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60 * 1


@dataclass
class Config:
    db: DBConfig = DBConfig()
    auth: AuthConfig = AuthConfig()
    env: str = os.environ["ENV"]


config = Config()
