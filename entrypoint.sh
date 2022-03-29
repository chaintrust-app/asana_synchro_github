#!/bin/sh -l
export ASANA_ACCESS_TOKEN=$ASANA_ACCESS_TOKEN
export PR_NAME="$PR_NAME"
echo "test"
python asanaProject.py
echo "test2"