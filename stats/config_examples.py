"""
Configuration Examples for stats_cabines.py
Fichier : config_examples.py
Description : Exemples de configurations pour faciliter l'utilisation
"""

# ============================================================
# 🎯 EXEMPLE 1 : Configuration Standard (STAGING)
# ============================================================
# Utilisation : Configuration par défaut
# Copier-coller dans stats_cabines.py à la ligne 21-35

CONFIG_STANDARD = {
    'ENVIRONMENT': 'STAGING',
    'DATE_START': '2025-09-01',
    'DATE_END': '2026-01-14',
    'SHOW_DETAILS': True,
    'COMPARE_ENVIRONMENTS': False,
    'EXPORT_TO_EXCEL': True
}

# ============================================================
# 🎯 EXEMPLE 2 : Rapport Mensuel (Novembre 2025)
# ============================================================
# Utilisation : Analyser une période spécifique

CONFIG_MONTHLY_NOV_2025 = {
    'ENVIRONMENT': 'STAGING',
    'DATE_START': '2025-11-01',
    'DATE_END': '2025-11-30',
    'SHOW_DETAILS': True,
    'COMPARE_ENVIRONMENTS': False,
    'EXPORT_TO_EXCEL': True
}

# ============================================================
# 🎯 EXEMPLE 3 : Rapport Trimestriel (Q4 2025)
# ============================================================
# Utilisation : Analyser un trimestre

CONFIG_QUARTERLY_Q4_2025 = {
    'ENVIRONMENT': 'STAGING',
    'DATE_START': '2025-10-01',
    'DATE_END': '2025-12-31',
    'SHOW_DETAILS': True,
    'COMPARE_ENVIRONMENTS': False,
    'EXPORT_TO_EXCEL': True
}

# ============================================================
# 🎯 EXEMPLE 4 : Production (Quand disponible)
# ============================================================
# Utilisation : Analyser les données de production

CONFIG_PRODUCTION = {
    'ENVIRONMENT': 'PRODUCTION',
    'DATE_START': '2025-09-01',
    'DATE_END': '2026-01-14',
    'SHOW_DETAILS': True,
    'COMPARE_ENVIRONMENTS': False,
    'EXPORT_TO_EXCEL': True
}

# ============================================================
# 🎯 EXEMPLE 5 : Comparaison STAGING vs PRODUCTION
# ============================================================
# Utilisation : Comparer les deux environnements
# Note : PRODUCTION n'est pas encore disponible

CONFIG_COMPARISON = {
    'ENVIRONMENT': 'STAGING',
    'DATE_START': '2025-09-01',
    'DATE_END': '2026-01-14',
    'SHOW_DETAILS': True,
    'COMPARE_ENVIRONMENTS': True,
    'EXPORT_TO_EXCEL': True
}

# ============================================================
# 🎯 EXEMPLE 6 : Mode Résumé Rapide
# ============================================================
# Utilisation : Rapport rapide sans détails

CONFIG_QUICK_SUMMARY = {
    'ENVIRONMENT': 'STAGING',
    'DATE_START': '2025-09-01',
    'DATE_END': '2026-01-14',
    'SHOW_DETAILS': False,  # ← Mode résumé
    'COMPARE_ENVIRONMENTS': False,
    'EXPORT_TO_EXCEL': True
}

# ============================================================
# 🎯 EXEMPLE 7 : Test sans Export
# ============================================================
# Utilisation : Tester l'API sans générer Excel

CONFIG_TEST_NO_EXPORT = {
    'ENVIRONMENT': 'STAGING',
    'DATE_START': '2025-09-01',
    'DATE_END': '2026-01-14',
    'SHOW_DETAILS': True,
    'COMPARE_ENVIRONMENTS': False,
    'EXPORT_TO_EXCEL': False  # ← Pas d'export
}

# ============================================================
# 🎯 EXEMPLE 8 : Derniers 7 Jours
# ============================================================
# Utilisation : Analyser seulement les 7 derniers jours
# (À adapter avec la date du jour)

from datetime import datetime, timedelta

today = datetime.now().date()
seven_days_ago = today - timedelta(days=7)

CONFIG_LAST_7_DAYS = {
    'ENVIRONMENT': 'STAGING',
    'DATE_START': str(seven_days_ago),
    'DATE_END': str(today),
    'SHOW_DETAILS': True,
    'COMPARE_ENVIRONMENTS': False,
    'EXPORT_TO_EXCEL': True
}

# ============================================================
# 📋 GUIDE D'UTILISATION
# ============================================================
"""
Pour utiliser une configuration, copiez les valeurs dans stats_cabines.py :

1. Ouvrez stats_cabines.py
2. Allez à la ligne 21-35 (section Configuration)
3. Remplacez les valeurs par celles d'un exemple
4. Sauvegardez le fichier
5. Exécutez : python3 stats_cabines.py

Exemple pour CONFIG_MONTHLY_NOV_2025:

    ENVIRONMENT = 'STAGING'              # ← Changer
    DATE_START = '2025-11-01'            # ← Changer
    DATE_END = '2025-11-30'              # ← Changer
    SHOW_DETAILS = True
    COMPARE_ENVIRONMENTS = False
    EXPORT_TO_EXCEL = True
"""

# ============================================================
# 🔄 CONVERSIONS UTILES
# ============================================================

# Pour obtenir les dates d'une période
def get_date_range(year, month):
    """Retourne DATE_START et DATE_END pour un mois"""
    from datetime import datetime, timedelta

    start = f"{year}-{month:02d}-01"
    if month == 12:
        end = f"{year + 1}-01-01"
    else:
        end = f"{year}-{month + 1:02d}-01"

    last_day = (datetime.strptime(end, "%Y-%m-%d") - timedelta(days=1)).date()

    return {
        'DATE_START': start,
        'DATE_END': str(last_day)
    }

# Exemple : dates pour Novembre 2025
# dates = get_date_range(2025, 11)
# print(f"DATE_START = '{dates['DATE_START']}'")
# print(f"DATE_END = '{dates['DATE_END']}'")
# Résultat :
# DATE_START = '2025-11-01'
# DATE_END = '2025-11-30'

# ============================================================
# 📊 RÉSULTATS ATTENDUS
# ============================================================
"""
Après l'exécution, vous obtiendrez :

1. Affichage console avec :
   ✅ Configuration chargée
   ✅ Toutes les données récupérées
   ✅ Analyse terminée
   ✅ Fichier Excel généré

2. Fichier Excel dans exports/ :
   Format : cabine_analytics_{ENV}_{START}_{END}_{TIMESTAMP}.xlsx
   
   Contenu : 5 feuilles
   - 📋 Résumé
   - 📊 Événements
   - 📅 Timeline
   - 🏢 Par Cabine
   - 📈 KPIs

3. Durée : ~5-10 secondes

Exemple de nom de fichier :
cabine_analytics_STAGING_2025-11-01_2025-11-30_20260115_143652.xlsx
"""

