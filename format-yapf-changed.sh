#!/bin/bash
FILES=`git status --porcelain | grep -E "*\.py$" | grep -v migration | grep -v "^D  " | grep -v "^ D " | grep -v "^R  " | awk '{print $2}'`
if [ -z "$FILES" ]
then
    echo "No Python changes detected."
else
    echo "Checking: $FILES"
    yapf --in-place --recursive $FILES
fi
