import os
from dataclasses import dataclass

@dataclass
class Config:
    # db_host: str
    # db_server_port: str
    db_user: str = os.environ["DB_USER"]
    db_password: str = os.environ["DB_PASS"]
    db_name: str = os.environ["DB_NAME"]
    instance_connection_name: str = os.environ["INSTANCE_CONNECTION_NAME"]
    db_socket_dir: str = "/cloudsql"

    environment: str = os.environ["ENV"]

config = Config()

import sqlalchemy
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
# db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
db_socket_dir = "/cloudsql"
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
# production_config = Config(db)

# host_server = os.environ.get('host_server', 'localhost')
# db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
# database_name = os.environ.get('database_name', 'fastapi')
# db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
# db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'secret')))
# ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
# DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)
# host_server = os.environ.get('host_server', 'localhost')
# db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
# database_name = os.environ.get('database_name', 'fastapi')
# db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
# db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'secret')))
# ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
# DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)
# db = SessionLocal()
# def get_db():
#     return db
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# Remember - storing secrets in plaintext is potentially unsafe. Consider using
# something like https://cloud.google.com/secret-manager/docs/overview to help keep
# secrets secret.


