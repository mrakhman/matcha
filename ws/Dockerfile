FROM python:3.7-alpine

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# Python, don't write bytecode!
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update \
	&& apk upgrade --no-cache \
	&& apk add --no-cache git build-base \
	&& pip install --no-cache-dir pipenv \
	&& mkdir /app

WORKDIR /app

COPY Pipfile* /app/

RUN pipenv install --deploy --system

COPY . .
RUN chmod u+x app.py

EXPOSE 8888
ENTRYPOINT ["python3", "/app/app.py"]
