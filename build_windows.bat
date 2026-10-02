@echo off
REM Builds dist\VJ Bridge\VJ Bridge.exe and a zip you can share. Run from this folder.
setlocal
python -m venv .venv-build || goto :fail
call .venv-build\Scripts\activate || goto :fail
python -m pip install --upgrade pip || goto :fail
pip install -r requirements.txt pyinstaller || goto :fail
pyinstaller --noconfirm --clean vj_bridge.spec || goto :fail
powershell -NoProfile -Command "Compress-Archive -Path 'dist\VJ Bridge' -DestinationPath 'dist\VJ-Bridge-windows.zip' -Force" || goto :fail
echo.
echo Done:  dist\VJ Bridge\VJ Bridge.exe
echo Share: dist\VJ-Bridge-windows.zip
exit /b 0
:fail
echo.
echo Build failed - see the messages above.
exit /b 1
