cd D:\WorkSpace\PyDebug> 

Get-ChildItem -Path "./dist" -Include *.* -File -Recurse | foreach { $_.Delete()}
Get-ChildItem -Path "./build" -Include *.* -File -Recurse | foreach { $_.Delete()}

pause

python setup.py build sdist bdist_wheel

python -m twine upload dist/*

pause
