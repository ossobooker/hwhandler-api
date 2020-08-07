FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install -r requirements.txt

COPY ./hwhandler_api /app