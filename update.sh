#!/usr/bin/env zsh

set -e

cd /home/felipemfp/Workspace/covid19-data
/home/linuxbrew/.linuxbrew/bin/pipenv run python scrape.py
git add .
git commit -m "Scheduled updates ($(date +'%F %T %Z'))"
git push