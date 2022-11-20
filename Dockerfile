FROM python:3.10.8-slim

RUN mkdir /code
COPY . /code
WORKDIR /code


RUN pip install -r requirements.txt


ENTRYPOINT ["/code/entrypoint.sh"]
