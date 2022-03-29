#!/bin/sh -l
export ASANA_ACCESS_TOKEN=$ASANA_ACCESS_TOKEN
export PR_NAME="$PR_NAME"
export PR_IS_MERGE=$PR_IS_MERGE
echo $ASANA_ACCESS_TOKEN
python asanaProject.py