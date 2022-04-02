from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import config


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if config.env == 'dev':
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

elif config.env == 'production':
    POSTGRES_DATABASE_URL = f"postgresql+pg8000://{config.db.user}:{config.db.password}@/{config.db.name}" \
                            f"?unix_sock={config.db.socket_dir}/{instance_connection_name}/.s.PGSQL.5432"
    engine = create_engine(POSTGRES_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()
