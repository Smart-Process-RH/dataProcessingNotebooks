#!/bin/bash

cd /home/vladkunitsyn/WebstormProjects/dataProcessingNotebooks

echo "============================================================"
echo "🚀 DÉPLOIEMENT VERS SMART-PROCESS-RH"
echo "============================================================"
echo ""

# Vérifier la configuration
echo "1️⃣ Vérification de la configuration..."
echo "Remote configurée :"
git remote -v
echo ""

# Vérifier les commits
echo "2️⃣ Vérification des commits..."
echo "Commits locaux :"
git log --oneline -3
echo ""

# Vérifier la branche
echo "3️⃣ Vérification de la branche..."
echo "Branche actuelle :"
git branch -a
echo ""

# Pousser vers GitHub
echo "4️⃣ Poussement vers GitHub..."
git push -u origin statysics-by-vlad

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✅ SUCCÈS ! Repository poussé vers GitHub"
    echo "============================================================"
    echo ""
    echo "Repository : https://github.com/Smart-Process-RH/dataProcessingNotebooks"
    echo "Branche    : statysics-by-vlad"
    echo ""
else
    echo ""
    echo "============================================================"
    echo "⚠️ Le push a échoué"
    echo "============================================================"
    echo "Vérifiez :"
    echo "  1. Votre connexion internet"
    echo "  2. Vos credentials GitHub (SSH ou token)"
    echo "  3. L'existence du repository sur GitHub"
    echo ""
fi

