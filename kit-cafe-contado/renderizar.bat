@echo off
rem Renderiza um episodio do kit Coffee Hub.
rem Uso: renderizar.bat ST3-PT6 [processos]   (processos = 6 por padrao)
rem O video sai em saida\<EP>.mp4
setlocal
cd /d "%~dp0"
if "%~1"=="" (echo Uso: renderizar.bat ST3-PT6 & pause & exit /b 1)
set "W=%~2"
if "%W%"=="" set "W=6"
set "EP="
for /d %%S in (episodios\*) do if exist "%%S\%~1\index.html" set "EP=%%S\%~1"
if "%EP%"=="" (echo Episodio %~1 nao encontrado em episodios\ & pause & exit /b 1)
set "PATH=%~dp0motor\tools;%PATH%"
if "%MG_CHROME%"=="" if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set "MG_CHROME=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if "%MG_CHROME%"=="" if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set "MG_CHROME=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
if "%MG_CHROME%"=="" if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" set "MG_CHROME=%LocalAppData%\Google\Chrome\Application\chrome.exe"
if "%MG_CHROME%"=="" if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" set "MG_CHROME=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if not exist "saida" mkdir "saida"
echo Renderizando %EP% com %W% processos...
node motor\render.mjs "%EP%" --audio "%EP%\audio.flac" --out "saida\%~1.mp4" --workers %W%
echo.
echo Pronto: saida\%~1.mp4
