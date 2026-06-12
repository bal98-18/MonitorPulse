@echo off
cd /d "%~dp0"

echo [PROCESO] Activando el entorno virtual de forma relativa...
call venv\Scripts\activate

echo [PROCESO] Ejecutando purga e higienizacion de entornos previos...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo [PROCESO] Iniciando compilacion monolitica mediante PyInstaller...
pyinstaller --noconfirm --onefile --windowed --uac-admin --name "MonitorRendimiento" --icon="assets/icono.ico" --exclude-module venv --add-data "libs;libs" --add-data "gui;gui" --add-data "core;core" main.py

echo [PROCESO] Ejecutando inyeccion fisica de dependencias dinamicas...
if exist libs (
    xcopy /s /i /y "libs" "dist\libs"
) else (
    echo [ALERTA] La carpeta 'libs' no existe en la raiz. Creando estructura...
    mkdir dist\libs
)

echo =======================================================================
echo [PROCESO TERMINADO] Revisa si se generaron los archivos arriba.
echo =======================================================================
pause