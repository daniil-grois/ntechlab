#!/bin/bash
cd /code && \
    python alembic_upgrade_head.py && \
    python -O -m aiohttp.web -H 0.0.0.0 -P 8000 main:init_func
