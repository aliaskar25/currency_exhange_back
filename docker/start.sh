#!/bin/bash

exec uvicorn --factory app.main:create_app --host 0.0.0.0 --port 8000 --reload
