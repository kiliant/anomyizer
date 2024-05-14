#!/bin/bash

ENV_NAME="env"

if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
elif command -v python &>/dev/null && python --version 2>&1 | grep -q "Python 3"; then
    PYTHON_CMD=python
    PIP_CMD=pip
else
    echo "Python ist nicht installiert. Beenden."
    exit 1
fi

if [ ! -d "$ENV_NAME" ]; then
    $PYTHON_CMD -m venv "$ENV_NAME"
    echo "Virtuelle Umgebung $ENV_NAME erstellt."
fi

source "$ENV_NAME/bin/activate"

$PIP_CMD install -r requirements.txt

$PYTHON_CMD app.py
