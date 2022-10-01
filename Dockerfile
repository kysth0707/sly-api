FROM python:3.7.8

RUN pip install fastapi
RUN pip install uvicorn[standard]
RUN pip install requests
RUN mkdir -p /test
WORKDIR /test

ENTRYPOINT ["python", "app.py"]