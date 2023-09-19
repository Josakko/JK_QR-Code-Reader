#!/bin/bash


cd src/ || exit

mkdir build/

rm -rf venv
python -m venv venv
source venv/bin/activate

curl -o req.txt https://raw.githubusercontent.com/Josakko/JK_QR-Code-Reader/main/requirements.txt
pip install -r req.txt

python -m nuitka main.py --clang --enable-plugins=tk-inter --disable-console --clean-cache=all --remove-output --output-dir=build --onefile --standalone


deactivate
rm -rf venv
rm -rf req.txt
echo "Compiling finished!"

