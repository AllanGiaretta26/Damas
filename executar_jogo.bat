@echo off
REM Script para executar o Jogo de Damas no Windows

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║       INICIANDO JOGO DE DAMAS EM PYTHON            ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! 
    echo.
    echo Por favor, instale Python 3.7 ou superior de:
    echo https://www.python.org/downloads/
    echo.
    echo Certifique-se de marcar a opção "Add Python to PATH" durante a instalação.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
python --version
echo.

REM Verificar tkinter
echo Verificando tkinter...
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ tkinter não encontrado!
    echo.
    echo Para corrigir, reinstale Python e certifique-se de selecionar a opção:
    echo "tcl/tk and IDLE"
    pause
    exit /b 1
)

echo ✅ tkinter disponível!
echo.
echo Iniciando jogo...
echo.

python main.py

pause
