#!/usr/bin/env sh
wait-for postgres:5432 -- flask db init
gunicorn -c gunicorn_config.py app:app
