#!/bin/sh -l
export ASANA_ACCESS_TOKEN=$ASANA_ACCESS_TOKEN
echo 'rtejk'
echo github.event.commits[0].message
echo $ASANA_ACCESS_TOKEN
python asanaProject.py