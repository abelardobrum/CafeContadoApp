@echo off
rem Uso: RENDER-CAFE.bat <EP>   (ex.: RENDER-CAFE.bat ARABICA-X-ROBUSTA)
rem Renderiza com o motor do kit e copia o MP4 para a pasta final criada pelo cc.py entregar.
cd /d "%~dp0"
set "EP=%~1"
if "%EP%"=="" (echo Uso: RENDER-CAFE.bat EP & pause & exit /b 1)
if not exist "saida" mkdir "saida"
echo Renderizando %EP% ... (log em saida\%EP%-log.txt)
call renderizar.bat "%EP%" > "saida\%EP%-log.txt" 2>&1
if not exist "saida\%EP%.mp4" (echo ERRO no render: & type "saida\%EP%-log.txt" & pause & exit /b 1)
powershell -NoProfile -Command "$f=\"episodios\cafe-contado\%EP%\destino.txt\"; if (Test-Path $f) { $d=(Get-Content -Encoding UTF8 $f -Raw).Trim(); $n=Split-Path $d -Leaf; Copy-Item \"saida\%EP%.mp4\" (Join-Path $d ($n+\".mp4\")) -Force; Write-Host \"Video copiado para: $d\" }"
echo PRONTO!
pause
