#!/bin/bash
# ============================================================
# SCRIPT:   Quick Start - Stats Cabines
# Description: Lanceur rapide pour le script analytics
# ============================================================

cd /home/vladkunitsyn/PycharmProjects/dataProcessingNotebooks

echo "============================================================"
echo "📊 CABINE ANALYTICS - Démarrage rapide"
echo "============================================================"
echo ""
echo "🎯 Options :"
echo "   1) Rapport Standard (STAGING, 2025-09-01 à 2026-01-14)"
echo "   2) Rapport Mensuel (Novembre 2025)"
echo "   3) Rapport Trimestriel (Q4 2025)"
echo "   4) Test sans Export (vérifier l'API)"
echo "   5) Comparaison STAGING vs PRODUCTION"
echo "   6) Mode personnalisé (éditer le script)"
echo ""
read -p "Choisissez une option (1-6) : " choice

case $choice in
    1)
        echo "▶️ Lancement du rapport Standard..."
        python3 stats/stats_cabines.py
        ;;
    2)
        echo "▶️ Lancement du rapport Mensuel (Nov 2025)..."
        # Modifier temporairement les dates
        sed -i "s/DATE_START = '2025-09-01'/DATE_START = '2025-11-01'/g" stats/stats_cabines.py
        sed -i "s/DATE_END = '2026-01-14'/DATE_END = '2025-11-30'/g" stats/stats_cabines.py
        python3 stats/stats_cabines.py
        # Restaurer les valeurs
        sed -i "s/DATE_START = '2025-11-01'/DATE_START = '2025-09-01'/g" stats/stats_cabines.py
        sed -i "s/DATE_END = '2025-11-30'/DATE_END = '2026-01-14'/g" stats/stats_cabines.py
        ;;
    3)
        echo "▶️ Lancement du rapport Trimestriel (Q4 2025)..."
        sed -i "s/DATE_START = '2025-09-01'/DATE_START = '2025-10-01'/g" stats/stats_cabines.py
        sed -i "s/DATE_END = '2026-01-14'/DATE_END = '2025-12-31'/g" stats/stats_cabines.py
        python3 stats/stats_cabines.py
        sed -i "s/DATE_START = '2025-10-01'/DATE_START = '2025-09-01'/g" stats/stats_cabines.py
        sed -i "s/DATE_END = '2025-12-31'/DATE_END = '2026-01-14'/g" stats/stats_cabines.py
        ;;
    4)
        echo "▶️ Lancement du test (sans export Excel)..."
        sed -i "s/EXPORT_TO_EXCEL = True/EXPORT_TO_EXCEL = False/g" stats/stats_cabines.py
        python3 stats/stats_cabines.py
        sed -i "s/EXPORT_TO_EXCEL = False/EXPORT_TO_EXCEL = True/g" stats/stats_cabines.py
        ;;
    5)
        echo "▶️ Lancement de la comparaison STAGING vs PRODUCTION..."
        sed -i "s/COMPARE_ENVIRONMENTS = False/COMPARE_ENVIRONMENTS = True/g" stats/stats_cabines.py
        python3 stats/stats_cabines.py
        sed -i "s/COMPARE_ENVIRONMENTS = True/COMPARE_ENVIRONMENTS = False/g" stats/stats_cabines.py
        ;;
    6)
        echo "Ouvrez le fichier stats/stats_cabines.py avec votre éditeur préféré"
        echo "Modifiez les variables à la ligne 21-35"
        echo ""
        echo "Puis exécutez : python3 stats/stats_cabines.py"
        ;;
    *)
        echo "❌ Option invalide. Quitter."
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "✅ Terminé !"
echo "============================================================"
echo ""
echo "📊 Fichiers générés : exports/cabine_analytics_*.xlsx"
echo "📖 Documentation    : stats/README_STATS_CABINES.md"
echo "⚙️ Configuration    : stats/config_examples.py"
echo ""

