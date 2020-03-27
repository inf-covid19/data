#!/usr/bin/env bash

cd /home/felipemfp/Workspace/covid19-data
pipenv run python scrape.py
git add .
git commit -m "Updates"
git push