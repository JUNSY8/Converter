@echo off
setlocal
cd /d %~dp0

if not exist vendor\ffmpeg\ffmpeg.exe (
  echo Descargando ffmpeg essentials...
  powershell -NoProfile -ExecutionPolicy Bypass -File %~dp0scripts\fetch_ffmpeg.ps1
  if errorlevel 1 exit /b 1
)

python -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --name DescargadorCanciones ^
  --icon assets\icon.ico ^
  --add-data assets\icon.ico;assets ^
  --add-data assets\icon.png;assets ^
  --collect-all customtkinter ^
  --collect-all yt_dlp ^
  --add-binary vendor\ffmpeg\ffmpeg.exe;ffmpeg ^
  --add-binary vendor\ffmpeg\ffprobe.exe;ffmpeg ^
  app.py

echo.
echo Listo: dist\DescargadorCanciones.exe
