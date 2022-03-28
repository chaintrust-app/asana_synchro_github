#!/bin/sh -l
export ASANA_ACCESS_TOKEN=$ASANA_ACCESS_TOKEN
echo 'rtejk'
echo $ASANA_ACCESS_TOKEN
export test_name=$PR_NAME
python asanaProject.py