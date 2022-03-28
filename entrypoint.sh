#!/bin/sh -l
export ASANA_ACCESS_TOKEN=$ASANA_ACCESS_TOKEN
echo 'rtejk'
echo ${ secrets.ASANA_ACCESS_TOKEN }
echo ${ steps.hello.outputs.time }
echo $ASANA_ACCESS_TOKEN
python asanaProject.py