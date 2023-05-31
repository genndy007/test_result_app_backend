#!/bin/sh
exec poetry run gunicorn -b :5003 --access-logfile - --error-logfile - main:app
