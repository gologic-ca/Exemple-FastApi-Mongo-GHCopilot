#!/bin/bash
source .venv/Scripts/activate
uvicorn --app-dir ./src/ api:app --reload
