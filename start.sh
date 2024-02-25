#!/bin/bash

echo "Running migrations for DB..."
alembic -c alembic.ini upgrade head

echo "Starting the application..."
# python main.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
