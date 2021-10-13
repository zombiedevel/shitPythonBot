FROM python:3.9-alpine3.14
LABEL maintainer="ZombieDevel <valery.s.msk@icloud.com>"

RUN apk update \
    && apk add --virtual build-deps python3-dev musl-dev gcc g++ pkgconfig bash \
    && apk add --no-cache mariadb-dev


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install mysqlclient

RUN apk del build-deps gcc g++ pkgconfig bash
COPY . .

CMD ["python3", "main.py"]
