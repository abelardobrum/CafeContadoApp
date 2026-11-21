@echo off
rem Instala o motor do kit (precisa de Node.js 18+ e de Chrome ou Edge).
cd /d "%~dp0"
call npm install
if not exist "motor\tools" mkdir "motor\tools"
where ffmpeg >nul 2>nul && (echo ffmpeg encontrado no PATH) || (if exist "motor\tools\ffmpeg.exe" (echo ffmpeg OK) else (echo ATENCAO: baixe o ffmpeg em https://www.gyan.dev/ffmpeg/builds/ e coloque ffmpeg.exe e ffprobe.exe em motor\tools))
echo Kit pronto.
pause
