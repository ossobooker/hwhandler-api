#!/usr/bin/env bash

gunicorn hwhandler_api.main:hwhandler_api -k uvicorn.workers.UvicornWorker
