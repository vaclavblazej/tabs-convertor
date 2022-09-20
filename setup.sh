#!/usr/bin/env bash

if [ $# -ne 0 ]; then
    echo "usage: $0"
    exit
fi

# echo "pulling the newest version of the tabs repository"
# cd tabs
# git pull
# cd ..

echo "converting tabs to html"
\find tabs/ -name "*.tab" -exec ./code/convert.py < {} > sub.{/tab/html} \;

