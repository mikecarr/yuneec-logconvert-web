#!/bin/sh

. venv/bin/activate

nohup python application.py &

deactivate
