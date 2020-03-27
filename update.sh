#!/usr/bin/env zsh

set -e

mkdir -p ./tmp
cd /home/felipemfp/Workspace/covid19-data
/home/linuxbrew/.linuxbrew/bin/pipenv run python scrape.py > ./tmp/update-output.txt
git add .
git commit -m "Scheduled updates ($(date +'%F %T %Z'))" -m "$(cat ./tmp/update-output.txt)"
git push