#!/bin/bash
cd /code/app && \
    alembic upgrade head && \
    python -m aiohttp.web -H 0.0.0.0 -P 8000 main:init_func
