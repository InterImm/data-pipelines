#!/bin/sh

REPO_DIR=/home/itisme/git/interimm/data-pipelines
cd ${REPO_DIR}

pwd
git pull --recurse-submodules
cd ${REPO_DIR}/dapi
git checkout gh-pages
cd ${REPO_DIR}

echo 'Run insight_weather'
python ${REPO_DIR}/pipelines/insight_weather.py
echo 'End insight_weather'

cd ${REPO_DIR}/dapi
git add .
git commit -m 'update data'
git push
