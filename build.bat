@echo off

rmdir /Q /S dist
rmdir /Q /S build
mkdir dist

python setup.py build sdist bdist_wheel





