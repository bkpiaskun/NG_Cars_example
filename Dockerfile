FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"

RUN mkdir /app
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app/cars
RUN mkdir /app/ng
COPY ./cars/ /app/cars/
COPY ./ng/ /app/ng/
COPY ./manage.py /app/manage.py

COPY ./scripts /scripts
RUN chmod +x /scripts/*


RUN adduser -D user
USER user

WORKDIR /app

CMD ["entrypoint.sh"]