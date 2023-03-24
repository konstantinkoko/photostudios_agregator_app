FROM python:3.10

WORKDIR /fastapi_app

COPY . .

RUN pip install -r requirements.txt

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
