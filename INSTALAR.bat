@echo off
setlocal EnableExtensions
title Cafe Contado - Instalador
cd /d "%~dp0"
set "RAIZ=%~dp0"
set "KIT=%RAIZ%kit-cafe-contado"
set "APP=%RAIZ%app"
set "AUTO="
if /i "%~1"=="/auto" set "AUTO=1"
set "AVISOS=0"

echo ==============================================================
echo   CAFE CONTADO - instalador unico (kit + estudio)
echo ==============================================================
echo.
if not exist "%KIT%\CAFE-CONTADO.md" (
  echo ERRO: nao achei a pasta kit-cafe-contado ao lado deste instalador.
  goto :falhou
)
if not exist "%APP%\package.json" (
  echo ERRO: nao achei a pasta app ao lado deste instalador.
  goto :falhou
)

rem ------------------------------------------------------------ 1. Node.js
echo [1/7] Node.js
call :tem_node
if not errorlevel 1 goto :node_ok
echo   Node.js nao encontrado.
call :perguntar "  Instalar o Node.js LTS agora pelo winget?"
if errorlevel 1 goto :node_manual
call :winget OpenJS.NodeJS.LTS
call :atualizar_path
call :tem_node
if not errorlevel 1 goto :node_ok
:node_manual
echo   Instale o Node.js LTS em https://nodejs.org e rode este instalador de novo.
goto :falhou
:node_ok
for /f "delims=" %%V in ('node -v') do echo   ok %%V
echo.

rem ------------------------------------------------------------ 2. Python
echo [2/7] Python 3
call :tem_python
if not errorlevel 1 goto :python_ok
echo   Python nao encontrado.
call :perguntar "  Instalar o Python 3.12 agora pelo winget?"
if errorlevel 1 goto :python_manual
call :winget Python.Python.3.12
call :atualizar_path
call :tem_python
if not errorlevel 1 goto :python_ok
:python_manual
echo   Instale o Python 3 em https://www.python.org/downloads/ marcando "Add python.exe to PATH"
echo   e rode este instalador de novo.
goto :falhou
:python_ok
for /f "delims=" %%V in ('python --version') do echo   ok %%V
echo.

rem ------------------------------------------------------------ 3. Chrome / Edge
echo [3/7] Navegador para o render (Chrome ou Edge)
set "NAV="
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set "NAV=Chrome"
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set "NAV=Chrome"
if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" set "NAV=Chrome"
if not defined NAV if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" set "NAV=Edge"
if defined NAV (
  echo   ok %NAV%
) else (
  echo   ATENCAO: instale o Google Chrome - o render usa ele.
  set /a AVISOS+=1
)
echo.

rem ------------------------------------------------------------ 4. ffmpeg
echo [4/7] ffmpeg e ffprobe
if not exist "%KIT%\motor\tools" mkdir "%KIT%\motor\tools"
if exist "%KIT%\motor\tools\ffmpeg.exe" if exist "%KIT%\motor\tools\ffprobe.exe" goto :ffmpeg_ok
where ffmpeg >nul 2>nul && where ffprobe >nul 2>nul && goto :ffmpeg_path
echo   Nao encontrei o ffmpeg. Vou baixar a versao "essentials" do gyan.dev - cerca de 100 MB.
call :perguntar "  Baixar agora?"
if errorlevel 1 goto :ffmpeg_manual
set "FFZ=%TEMP%\cafe-ffmpeg.zip"
set "FFX=%TEMP%\cafe-ffmpeg"
curl.exe -L --fail --progress-bar -o "%FFZ%" https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
if errorlevel 1 goto :ffmpeg_manual
powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; Remove-Item -Recurse -Force '%FFX%' -ErrorAction SilentlyContinue; Expand-Archive -Force '%FFZ%' '%FFX%'; foreach ($n in 'ffmpeg.exe','ffprobe.exe') { Get-ChildItem '%FFX%' -Recurse -Filter $n | Select-Object -First 1 | Copy-Item -Destination '%KIT%\motor\tools' -Force }"
del /q "%FFZ%" >nul 2>nul
rmdir /s /q "%FFX%" >nul 2>nul
if exist "%KIT%\motor\tools\ffmpeg.exe" if exist "%KIT%\motor\tools\ffprobe.exe" goto :ffmpeg_ok
:ffmpeg_manual
echo   ATENCAO: baixe o ffmpeg em https://www.gyan.dev/ffmpeg/builds/ e coloque
echo   ffmpeg.exe e ffprobe.exe em kit-cafe-contado\motor\tools
set /a AVISOS+=1
goto :ffmpeg_fim
:ffmpeg_path
echo   ok - no PATH do sistema
goto :ffmpeg_fim
:ffmpeg_ok
echo   ok - kit-cafe-contado\motor\tools
:ffmpeg_fim
echo.

rem ------------------------------------------------------------ 5. Kit
echo [5/7] Kit Cafe Contado - motor e bibliotecas Python
pushd "%KIT%"
call npm install --no-fund --no-audit --loglevel=error
if errorlevel 1 (
  popd
  echo   ERRO no npm install do kit.
  goto :falhou
)
set "PATH=%KIT%\motor\tools;%PATH%"
set "PYTHONUTF8=1"
python ferramentas\cc.py checar
if errorlevel 1 (
  echo   ATENCAO: a checagem do kit acusou falta de algo - veja acima.
  set /a AVISOS+=1
)
popd
echo.

rem ------------------------------------------------------------ 6. Estudio
echo [6/7] Estudio - tela web
pushd "%APP%"
call npm install --no-fund --no-audit --loglevel=error
if errorlevel 1 (
  popd
  echo   ERRO no npm install do estudio.
  goto :falhou
)
call npm run build > "%TEMP%\cafe-estudio-build.txt" 2>&1
if errorlevel 1 (
  type "%TEMP%\cafe-estudio-build.txt"
  popd
  echo   ERRO ao montar a tela do estudio.
  goto :falhou
)
popd
echo   ok
echo.

rem ------------------------------------------------------------ 7. Claude Code
echo [7/7] Claude Code - login da conta Claude
call :tem_claude
if not errorlevel 1 goto :claude_ok
echo   Claude Code nao encontrado. Ele e usado para entrar com a sua conta Claude.
echo   Sem ele, ainda da para usar uma chave de API na aba Configuracao do estudio.
call :perguntar "  Instalar o Claude Code agora?"
if errorlevel 1 goto :claude_pulado
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://claude.ai/install.ps1 | iex"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
call :tem_claude
if not errorlevel 1 goto :claude_ok
echo   ATENCAO: a instalacao do Claude Code nao terminou. Veja https://claude.com/claude-code
set /a AVISOS+=1
goto :claude_fim
:claude_pulado
echo   pulado - use uma chave de API na aba Configuracao.
goto :claude_fim
:claude_ok
echo   ok - o login e feito na aba Configuracao do estudio.
:claude_fim
echo.

rem ------------------------------------------------------------ atalho
if defined AUTO goto :fim
call :perguntar "Criar atalho do estudio na Area de Trabalho?"
if errorlevel 1 goto :fim
powershell -NoProfile -Command "$s = (New-Object -ComObject WScript.Shell).CreateShortcut([IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'Cafe Contado - Estudio.lnk')); $s.TargetPath = '%RAIZ%ABRIR-ESTUDIO.bat'; $s.WorkingDirectory = '%RAIZ%'; $s.IconLocation = 'shell32.dll,137'; $s.Save()"
echo   atalho criado.
echo.

:fim
echo ==============================================================
if "%AVISOS%"=="0" (
  echo   Tudo instalado.
) else (
  echo   Instalado com %AVISOS% aviso^(s^) - veja as mensagens ATENCAO acima.
)
echo   Para usar: dois cliques em ABRIR-ESTUDIO.bat
echo ==============================================================
if defined AUTO exit /b 0
call :perguntar "Abrir o estudio agora?"
if errorlevel 1 exit /b 0
start "" "%RAIZ%ABRIR-ESTUDIO.bat"
exit /b 0

:falhou
echo.
echo Instalacao interrompida.
if not defined AUTO pause
exit /b 1

rem ============================================================ funcoes
:perguntar
rem Retorna 0 = sim, 1 = nao. Em /auto responde sim.
if defined AUTO exit /b 0
choice /c SN /n /m "%~1 [S/N] "
if errorlevel 2 exit /b 1
exit /b 0

:tem_node
node -v >nul 2>nul
exit /b %errorlevel%

:tem_python
rem evita o atalho falso da Microsoft Store
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul
exit /b %errorlevel%

:tem_claude
where claude >nul 2>nul && exit /b 0
if exist "%USERPROFILE%\.local\bin\claude.exe" (
  set "PATH=%USERPROFILE%\.local\bin;%PATH%"
  exit /b 0
)
exit /b 1

:winget
where winget >nul 2>nul
if errorlevel 1 (
  echo   winget nao esta disponivel neste Windows.
  exit /b 1
)
winget install -e --id %1 --accept-source-agreements --accept-package-agreements
exit /b %errorlevel%

:atualizar_path
for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')"`) do set "PATH=%%P;%PATH%"
exit /b 0
