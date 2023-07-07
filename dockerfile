FROM python:3.10-alpine

RUN apk update

RUN apk add git

ENV FLASK_APP=main.py

WORKDIR /biblioflask

COPY ./requirements.txt /biblioflask

RUN pip install -r requirements.txt

COPY . /biblioflask

CMD [ "flask", "run", "--host=0.0.0.0", "--debug"]