#!/bin/bash
cd /home/tapocki
exec /home/ari-clothes/venv/bin/python run.py >> /tmp/tapocki.log 2>&1
