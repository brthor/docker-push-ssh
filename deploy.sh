#!/usr/bin/env bash
pypiUsername="$1"
pypiPassword="$2"

rm -r dist

. ./venv/bin/activate

#pip install twine wheel
python setup.py sdist bdist_wheel
twine upload -u "$1" -p "$2" dist/*