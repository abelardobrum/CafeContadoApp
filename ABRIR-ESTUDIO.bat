@echo off
setlocal
title Cafe Contado - Estudio
cd /d "%~dp0app"
set "PORTA=3001"
set "URL=http://localhost:%PORTA%"

where node >nul 2>nul
if errorlevel 1 (
  echo Node.js nao encontrado. Instale em https://nodejs.org e tente de novo.
  pause
  exit /b 1
)

rem Porta livre (2), estudio ja aberto (0) ou outro programa nela (1)?
powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; $c = Get-NetTCPConnection -LocalPort %PORTA% -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1; if (-not $c) { exit 2 }; try { $r = Invoke-WebRequest -UseBasicParsing %URL%/api/ping -TimeoutSec 5; if ($r.Content -match 'cafe-contado') { exit 0 } } catch {}; $p = Get-Process -Id $c.OwningProcess -ErrorAction SilentlyContinue; Write-Host ('A porta %PORTA% esta ocupada por outro programa: ' + $p.ProcessName + ' (PID ' + $c.OwningProcess + ')'); exit 1"
set "SITUACAO=%errorlevel%"
if "%SITUACAO%"=="0" (
  echo O estudio ja esta aberto em outra janela. Abrindo o navegador...
  start "" "%URL%"
  timeout /t 4 >nul
  exit /b 0
)
if "%SITUACAO%"=="1" (
  echo Feche esse programa e abra o estudio de novo.
  pause
  exit /b 1
)

set "FALTA="
if not exist "node_modules" set "FALTA=1"
if not exist "..\kit-cafe-contado\node_modules" set "FALTA=1"
if not exist "..\kit-cafe-contado\motor\tools\ffmpeg.exe" where ffmpeg >nul 2>nul || set "FALTA=1"
if defined FALTA (
  echo O estudio ainda nao foi instalado neste computador.
  echo Rode primeiro o INSTALAR.bat - fica na mesma pasta deste arquivo.
  pause
  exit /b 1
)

echo Preparando a tela...
call npm run build > "%TEMP%\cafe-estudio-build.txt" 2>&1
if errorlevel 1 (
  type "%TEMP%\cafe-estudio-build.txt"
  echo.
  echo Falha ao montar a tela.
  pause
  exit /b 1
)

rem abre o navegador assim que o servidor responder
start "" /b powershell -NoProfile -WindowStyle Hidden -Command "$ProgressPreference='SilentlyContinue'; for($i=0;$i -lt 60;$i++){try{Invoke-WebRequest -UseBasicParsing %URL%/api/ping -TimeoutSec 2 | Out-Null; Start-Process '%URL%'; break}catch{Start-Sleep 1}}"

echo.
echo  Estudio rodando em %URL%
echo  Deixe esta janela aberta enquanto usa. Para encerrar, feche a janela.
echo.
node server\index.mjs
echo.
echo O servidor parou. Veja a mensagem acima.
pause
