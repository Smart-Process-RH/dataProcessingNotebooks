#!/bin/bash

# Script de diagnostic - Vérification de l'environnement Python
# ==============================================================

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  DIAGNOSTIC PYTHON - Repository dataProcessingNotebooks       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 1. Vérifier Python
echo "1️⃣  VÉRIFICATION DE PYTHON"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   Python 3:"
python3 --version
echo ""
echo "   Localisation:"
which python3
echo ""

# 2. Vérifier les dépendances critiques
echo ""
echo "2️⃣  VÉRIFICATION DES DÉPENDANCES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Fonction pour tester une dépendance
test_package() {
    local package=$1
    local import_name=${2:-$1}

    if python3 -c "import $import_name" 2>/dev/null; then
        version=$(python3 -c "import $import_name; print(getattr($import_name, '__version__', 'unknown'))" 2>/dev/null)
        echo "   ✅ $package: $version"
    else
        echo "   ❌ $package: NOT INSTALLED"
    fi
}

test_package "requests"
test_package "pandas" "pd"
test_package "numpy" "np"
test_package "openpyxl"
test_package "json"
test_package "warnings"
test_package "os"
test_package "datetime"
test_package "pathlib" "pathlib"

echo ""

# 3. Vérifier l'environnement
echo "3️⃣  ENVIRONNEMENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Vérifier venv
if [ -d "venv" ]; then
    echo "   ✅ Dossier venv: présent"
    if [ -d "venv/lib/python3.12" ]; then
        echo "   ✅ venv Python 3.12: configuré"
    fi
else
    echo "   ℹ️  Dossier venv: non présent (utilise Python système)"
fi

echo ""

# 4. Vérifier le répertoire courant
echo "4️⃣  RÉPERTOIRE COURANT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

pwd
echo ""

# 5. Fichiers importants
echo "5️⃣  FICHIERS IMPORTANTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "ats_cibli.py" ]; then
    echo "   ✅ ats_cibli.py: $(wc -l < ats_cibli.py) lignes"
else
    echo "   ❌ ats_cibli.py: NOT FOUND"
fi

if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt: présent"
else
    echo "   ℹ️  requirements.txt: non présent"
fi

echo ""

# 6. Test d'exécution
echo "6️⃣  TEST D'EXÉCUTION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if python3 -c "
import sys
import requests
import pandas as pd
import numpy as np
import json
import warnings
import os
from datetime import datetime, timedelta
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
print('   ✅ Tous les imports sont OK')
" 2>&1; then
    echo ""
    echo "   ✅ Script testable sans erreur"
else
    echo ""
    echo "   ❌ Erreur lors de l'import des modules"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  DIAGNOSTIC TERMINÉ                                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

