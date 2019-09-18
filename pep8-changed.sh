#!/bin/bash
FILES=`git status --porcelain | grep -E "*\.py$" | grep -v migration | grep -v " D " | awk '{print $2}'`
if [ -z "$FILES" ]
then
    echo "No Python changes detected."
else
    echo "Checking: $FILES"
    pylint --rcfile=pylint.rc $FILES
fi
