#!/bin/bash

# Script para executar o Jogo de Damas
# Compatível com Windows PowerShell, Linux e macOS

echo "╔════════════════════════════════════════════════════╗"
echo "║       INICIANDO JOGO DE DAMAS EM PYTHON            ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python não encontrado. Por favor, instale Python 3.7 ou superior."
    exit 1
fi

# Encontrar o interpretador Python
if command -v python3 &> /dev/null; then
    PYTHON="python3"
else
    PYTHON="python"
fi

echo "✅ Python encontrado: $PYTHON"
echo ""

# Verificar versão
$PYTHON --version
echo ""

# Verificar tkinter
echo "Verificando tkinter..."
$PYTHON -c "import tkinter; print('✅ tkinter disponível')" 2>/dev/null || {
    echo "❌ tkinter não encontrado!"
    echo ""
    echo "Para instalar tkinter:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  Fedora: sudo dnf install python3-tkinter"
    echo "  macOS: brew install python-tk"
    echo "  Windows: Reinstale Python marcando a opção 'tcl/tk and IDLE'"
    exit 1
}

echo ""
echo "Iniciando jogo..."
echo ""

# Executar o jogo
$PYTHON main.py
