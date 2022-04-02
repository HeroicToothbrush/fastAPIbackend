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
class Config:
    db: DBConfig = DBConfig()
    env: str = os.environ["ENV"]


config = Config()
