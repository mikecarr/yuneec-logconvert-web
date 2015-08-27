#!/bin/sh

. venv/bin/activate

nohup python index.py &

deactivate
