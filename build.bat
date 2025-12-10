@echo off
echo Limpando build antigo...
rmdir /s /q build
rmdir /s /q dist
del main.spec

echo Gerando EXE...
python -m PyInstaller main.py ^
    --onefile ^
    --windowed ^
    --add-data "assets;assets" ^
    --add-data "data;data" ^
    --add-data "engine;engine" ^
    --add-data "config.py;."

echo Copiando pastas para dist...
xcopy assets dist\assets /E /I
xcopy data dist\data /E /I
xcopy engine dist\engine /E /I
copy config.py dist\

pause
