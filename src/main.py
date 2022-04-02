import uvicorn
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from . import models
from .api.api import api_router
from .auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_user, create_access_token, \
    get_current_active_user
from .database import engine
from .database import get_db
from .schemas import Token, User, UserCreate

app = FastAPI()
app.include_router(api_router)
# todo - needf to replace this with alembic migrations, eg here https://fastapi.tiangolo.com/tutorial/sql-databases/
# todo - add alerts, add docs, logging, sentry, mypy and flake8/black, tests, endpoints folder: https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/core/security.py
models.Base.metadata.create_all(bind=engine)

# todo allow_origins=[*] is not recommended for Production purposes. It is recommended to have specified list of origins
# eg allow_origins=['client-facing-example-app.com', 'localhost:5000']
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])

"""
FastAPI can be run on multiple worker process with the help of Gunicorn server with the help of uvicorn.workers.UvicornWorker worker class. Every worker process starts its instance of FastAPI application on its own Process Id. In order to ensure every instance of application communicates to the database, we will connect and disconnect to the database instance in the FastAPI events  startup and shutdown respectively.
"""


# @app.on_event("startup")
# async def startup(db: Session = Depends(get_db)):
#     await db.connect()

# @app.on_event("shutdown")
# async def shutdown(db: Session = Depends(get_db)):
#     await db.disconnect()


# todo refactor these routes away
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
