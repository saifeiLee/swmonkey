#!/bin/bash
SETUP_FILE_FOR_ARMOR="setup.armor"
UPLOAD_SCRIPT_FOR_ARMOR="auto-upload.armor"
DIST_ARMOR="dist-armor"

clean_dist() {
  echo "清理dist目录..."
  if [ -d "dist" ]; then
    rm -rf dist/*
  fi
}

upload_package() {
  # 需要配置仓库源的TOKEN
  API_TOKEN=$(cat ~/.pypirc | grep password | cut -d' ' -f3)
  echo $API_TOKEN
  echo "上传..."
  # python3.8可用，3.11对应的版本 参数变了
  python -m twine upload --verbose -u __token__ -p $API_TOKEN dist/* --verbose
}

echo "准备开始构建和发布..."
clean_dist

update_version() {
  # Initialize an empty variable for storing the version
  version=""

  # Read the file line by line
  while read -r line; do
    # Check if the line starts with "__version__"
    if [[ $line == __version__* ]]; then
      # Extract the version using awk, trim leading and trailing quotes
      version=$(echo $line | awk -F "=" '{print $2}' | tr -d " '" | tr -d "' ")
      # Break the loop once the version is found
      break
    fi
  done <"src/swmonkey/main.py"

  # Print the extracted version
  echo "版本号: $version"
  # change version
  sed -i "s/version = .*/version = '$version'/" $DIST_ARMOR/setup.py
}

# check for '--armor' parameter
if [[ "$@" == *"--armor"* ]]; then
  echo "代码混淆构建..."
  pyarmor gen -O $DIST_ARMOR -r -i src/swmonkey
  cp $SETUP_FILE_FOR_ARMOR $DIST_ARMOR/setup.py
  cp README.md $DIST_ARMOR/README.md
  update_version
  cp $UPLOAD_SCRIPT_FOR_ARMOR $DIST_ARMOR/auto-upload.sh
  chmod +x $DIST_ARMOR/auto-upload.sh
  # execute upload script under $DIST_ARMOR
  cd $DIST_ARMOR
  ./auto-upload.sh
  cd ..
else
  echo "非混淆构建..."
  python setup.py sdist
  upload_package
  if [ $? -ne 0 ]; then
    echo "上传失败,检查版本号是否已更新"
    exit 1
  fi
  echo "完成√"
fi
