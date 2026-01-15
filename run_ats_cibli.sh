#!/bin/bash

# Script wrapper pour exécuter ats_cibli.py avec le venv
# ========================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Vérifier que le venv existe
if [ ! -d "venv" ]; then
    echo "❌ Erreur: Le dossier 'venv' n'existe pas!"
    echo "Créez-le avec: python3 -m venv venv"
    exit 1
fi

# Activer le venv
echo "🔧 Activation du venv..."
source venv/bin/activate

# Vérifier que les dépendances sont installées
echo "✅ venv activé"
echo ""

# Exécuter le script
echo "🚀 Lancement du script ats_cibli.py..."
echo ""
python3 ats_cibli.py "$@"

# Désactiver le venv à la fin
deactivate 2>/dev/null || true

