rm -r dist/*
python setup.py sdist
API_TOKEN=$(cat ~/.pypirc | grep password | cut -d' ' -f3)
echo $API_TOKEN
twine upload -u __token__ -p $API_TOKEN  dist/*