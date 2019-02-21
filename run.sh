git pull --recurse-submodules
cd dapi
git checkout gh-pages
cd ..


echo 'Run insight_weather'
python pipelines/insight_weather.py
echo 'End insight_weather'

cd dapi
git add .
git commit -m 'update data'
git push