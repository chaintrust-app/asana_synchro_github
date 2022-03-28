#!/bin/sh -l
export ASANA_ACCESS_TOKEN=$ASANA_ACCESS_TOKEN
export NAME_PR=${{ github.event.commits[0].message}}
echo ${{ github.event.commits[0].message}}
echo 'rtejk'
echo $ASANA_ACCESS_TOKEN
python asanaProject.py