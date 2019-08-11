FROM python:3.7-alpine

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# Python, don't write bytecode!
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update \
	&& apk upgrade --no-cache \
	&& apk add --no-cache git curl \
	&& pip install --no-cache-dir pipenv \
	&& mkdir /app

WORKDIR /app

COPY Pipfile* /app/

RUN pipenv install --deploy --system

COPY . .

HEALTHCHECK --interval=10s --timeout=3s CMD curl --fail http://localhost:5000/health || exit 1
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
