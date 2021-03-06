# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.4-slim

EXPOSE 8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY .devcontainer/requirements.txt .
RUN python -m pip install -r requirements.txt

# Install Linux tools
RUN apt-get update -y && \
    apt-get install git -y && \
    apt-get install -y tree 

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--bind", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "src.main:app"]
#CMD python3 src/main.py
# CMD gunicorn src.main:app -c src/gunicorn_config.py
# Run the web service on container startup using gunicorn webserver.
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app
