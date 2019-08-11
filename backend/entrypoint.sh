#!/usr/bin/env bash
sleep 10
gunicorn -c gunicorn_config.py app:app
