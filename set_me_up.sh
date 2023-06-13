#!/bin/bash

pip install -r requirements.txt

source .local_settings

PYTHONPATH=src pytest

