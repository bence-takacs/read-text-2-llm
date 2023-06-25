#!/bin/bash

pip install -r requirements.txt

source .local_settings

PYTHONPATH=src pytest

echo "In order to set up the app, you should run:"
echo "export OPENAI_API_KEY=$OPENAI_API_KEY"