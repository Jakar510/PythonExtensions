@echo off

rmdir /Q /S dist
rmdir /Q /S build
mkdir dist

python setup.py build sdist bdist_wheel

pause

python -m twine upload dist/*



