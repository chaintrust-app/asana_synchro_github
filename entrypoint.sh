#!/bin/sh -l
export ASANA_ACCESS_TOKEN=$ASANA_ACCESS_TOKEN
export PR_NAME="$PR_NAME"
export PR_MERGE="$PR_MERGE"
export PR_NB_FOR_DEPLOY="$PR_NB_FOR_DEPLOY"
python /code/asanaProject.py