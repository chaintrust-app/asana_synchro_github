#!/bin/sh -l
export ASANA_ACCESS_TOKEN=$ASANA_ACCESS_TOKEN
export PR_NAME="$PR_NAME"
export PR_MERGE="$PR_MERGE"
python /code/asanaProject.py