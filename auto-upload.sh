echo "准备开始构建和发布..."
echo "清理dist目录..."
rm -r dist/*
echo "构建..."
python setup.py sdist
API_TOKEN=$(cat ~/.pypirc | grep password | cut -d' ' -f3)
echo $API_TOKEN
echo "上传..."
# python3.8可用，3.11对应的版本 参数变了
python -m twine upload -u __token__ -p $API_TOKEN  dist/*
echo "完成√"