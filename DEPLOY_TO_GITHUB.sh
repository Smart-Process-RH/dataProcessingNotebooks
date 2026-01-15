#!/bin/bash
# ============================================================
# SCRIPT: Déployer vers Smart-Process-RH
# Description: Initialiser et pousser le repository vers GitHub
# ============================================================

set -e  # Quitter en cas d'erreur

echo "============================================================"
echo "🚀 DÉPLOIEMENT VERS SMART-PROCESS-RH"
echo "============================================================"
echo ""

# Configuration
REPO_PATH="/home/vladkunitsyn/WebstormProjects/dataProcessingNotebooks"
GITHUB_ORG="Smart-Process-RH"
GITHUB_REPO="Statsistics-Cabins-ATS"
BRANCH="statysics-by-vlad"

echo "📍 Destination : $REPO_PATH"
echo "📦 Organization : $GITHUB_ORG"
echo "🌿 Branch : $BRANCH"
echo ""

# Vérifier que le dossier existe
if [ ! -d "$REPO_PATH" ]; then
    echo "❌ ERREUR: Le dossier $REPO_PATH n'existe pas"
    exit 1
fi

echo "✅ Dossier trouvé"
echo ""

# Naviguer dans le dossier
cd "$REPO_PATH"
echo "📂 Accédé à : $(pwd)"
echo ""

# Étape 1: Initialiser Git
echo "="*60
echo "ÉTAPE 1 : Initialiser le Repository Git"
echo "="*60

if [ -d ".git" ]; then
    echo "⚠️ Repository Git existe déjà"
    echo "Confirmation de la branche actuelle :"
    git branch
else
    echo "Initialisation du repository..."
    git init
    echo "✅ Repository initialisé"
fi

echo ""

# Étape 2: Configurer la remote
echo "="*60
echo "ÉTAPE 2 : Configurer la remote GitHub"
echo "="*60

REMOTE_URL="https://github.com/$GITHUB_ORG/$GITHUB_REPO.git"

if git remote | grep -q origin; then
    echo "Remote 'origin' existe déjà :"
    git remote -v
else
    echo "Ajout de la remote origin..."
    git remote add origin "$REMOTE_URL"
    echo "✅ Remote configurée : $REMOTE_URL"
fi

echo ""

# Étape 3: Ajouter tous les fichiers
echo "="*60
echo "ÉTAPE 3 : Ajouter les fichiers"
echo "="*60

echo "Ajout de tous les fichiers..."
git add .
echo "✅ Fichiers ajoutés"
echo ""
echo "État du repository :"
git status

echo ""

# Étape 4: Créer le commit
echo "="*60
echo "ÉTAPE 4 : Créer le commit initial"
echo "="*60

COMMIT_MSG="chore: initial commit - stats_cabines.py avec branche statysics-by-vlad

- Script d'analyse Cabine complet (8 étapes)
- 6 endpoints API intégrés
- Export Excel avec 5 feuilles
- Documentation professionnelle
- Prêt pour production"

echo "Message de commit :"
echo "$COMMIT_MSG"
echo ""

if git commit -m "$COMMIT_MSG"; then
    echo "✅ Commit créé"
else
    echo "⚠️ Aucun changement à commiter"
fi

echo ""

# Étape 5: Créer/Vérifier la branche
echo "="*60
echo "ÉTAPE 5 : Configurer la branche"
echo "="*60

echo "Branches locales :"
git branch -a

if git rev-parse --verify $BRANCH 2>/dev/null; then
    echo "✅ Branche $BRANCH existe déjà"
else
    echo "Création de la branche $BRANCH..."
    git branch -m $BRANCH || git checkout -b $BRANCH
    echo "✅ Branche $BRANCH créée"
fi

echo ""

# Étape 6: Pousser vers GitHub
echo "="*60
echo "ÉTAPE 6 : Pousser vers GitHub"
echo "="*60

echo "⚠️  ATTENTION : Vous devez avoir :"
echo "  1. Un account GitHub avec accès à l'organisation $GITHUB_ORG"
echo "  2. Les droits de push sur le repository $GITHUB_REPO"
echo "  3. Une clé SSH configurée OU utiliser HTTPS avec token"
echo ""
echo "Commande de push :"
echo "  git push -u origin $BRANCH"
echo ""
read -p "Voulez-vous pousser maintenant ? (oui/non) : " RESPONSE

if [ "$RESPONSE" = "oui" ] || [ "$RESPONSE" = "yes" ] || [ "$RESPONSE" = "y" ]; then
    echo "Pushing to $REMOTE_URL..."
    git push -u origin $BRANCH
    echo "✅ Succès ! Repository poussé vers GitHub"
else
    echo "ℹ️  Push annulé. Pour pousser plus tard :"
    echo "   git push -u origin $BRANCH"
fi

echo ""
echo "="*60
echo "✅ OPÉRATION TERMINÉE"
echo "="*60
echo ""
echo "Étapes complétées :"
echo "  [✓] Initialisation Git"
echo "  [✓] Configuration de la remote"
echo "  [✓] Ajout des fichiers"
echo "  [✓] Création du commit"
echo "  [✓] Branche $BRANCH configurée"
echo "  [$([ "$RESPONSE" = "oui" ] && echo "✓" || echo "○")] Push vers GitHub"
echo ""
echo "Infos utiles :"
echo "  Repository local : $REPO_PATH"
echo "  Repository GitHub : https://github.com/$GITHUB_ORG/$GITHUB_REPO"
echo "  Branche : $BRANCH"
echo ""

