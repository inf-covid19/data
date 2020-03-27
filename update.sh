#!/usr/bin/env zsh

set -e

cd /home/felipemfp/Workspace/covid19-data
/home/linuxbrew/.linuxbrew/bin/pipenv run python scrape.py
git add .
git commit -m "Updates"
git push