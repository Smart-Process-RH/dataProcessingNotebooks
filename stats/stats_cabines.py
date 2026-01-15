# ============================================================
# SCRIPT:   Cabine Analytics - API Integration
# Description: Analyser les données de la Cabine (CV créés, imprimés, offres consultées)
# Repository:   Zaidoudou/dataProcessingNotebooks
# Branch:  statysics-by-vlad
# ============================================================
# Imports

import requests
import pandas as pd
import warnings
import os
from datetime import datetime

warnings.filterwarnings('ignore')

# ============================================================
# ⚙️ CONFIGURATION - MODIFIEZ ICI
# ============================================================

# Environnement
ENVIRONMENT = 'STAGING'  # ← MODIFIEZ:    'STAGING' ou 'PRODUCTION'

# Dates
DATE_START = '2025-09-01'  # ← MODIFIEZ LA DATE DE DÉBUT
DATE_END = '2026-01-14'    # ← MODIFIEZ LA DATE DE FIN

# Affichage
SHOW_DETAILS = True              # ← Afficher détails ou résumé
COMPARE_ENVIRONMENTS = False     # ← Comparer STAGING vs PRODUCTION

# Export
EXPORT_TO_EXCEL = True           # ← Générer fichier Excel

# ============================================================
# CONFIGURATION DE L'API - NE MODIFIEZ PAS
# ============================================================

# URLs et clés API
API_STAGING_URL = 'https://cibli-api.agency.lonestone.io/api'
API_STAGING_KEY = 'PGZ4qtc5jtf@rph3twf'

API_PROD_URL = 'https://app-api.ciblijob.fr/api'  # COMING SOON - pas encore déployée
API_PROD_KEY = 'txf.hpc9aut9rbd2KWA'

# Sélectionner l'URL et la clé selon l'environnement
if ENVIRONMENT == 'STAGING':
    API_URL = API_STAGING_URL
    API_KEY = API_STAGING_KEY
    ENV_STATUS = '🧪 STAGING (Environnement de test)'
else:
    API_URL = API_PROD_URL
    API_KEY = API_PROD_KEY
    ENV_STATUS = '🚀 PRODUCTION (Environnement réel - COMING SOON)'

# Créer le dossier d'exports s'il n'existe pas
if not os.path.exists('exports'):
    os.makedirs('exports')

# Headers pour les requêtes API
HEADERS = {
    'x-secret-key': API_KEY
}

# Afficher la configuration
print('✅ Configuration chargée :  ')
print(f'   Environnement:    {ENV_STATUS}')
print(f'   URL API:  {API_URL}')
print(f'   Période:  {DATE_START} à {DATE_END}')
print(f'   Afficher détails: {SHOW_DETAILS}')
print(f'   Comparer ENV: {COMPARE_ENVIRONMENTS}')
print()
print('💡 Astuce:   Pour changer les paramètres, modifiez les variables ci-dessus.')

# ============================================================
# 📥 ÉTAPE 1 : Récupération des données API
# ============================================================

print('\n📥 Récupération des données depuis l\'API...')
print('=' * 60)

# 1️⃣ Récupérer les cabines (booths)
print('\n1️⃣ Récupération des cabines...')
try:
    response_booths = requests.get(
        f'{API_URL}/booths/all',
        headers=HEADERS
    )
    if response_booths.status_code == 200:
        booths_data = response_booths.json()
        booths_df = pd.DataFrame(booths_data)
        print(f'✅ {len(booths_df)} cabines récupérées')
    else:
        print(f'❌ Erreur:   {response_booths.status_code}')
        booths_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Erreur:   {str(e)}')
    booths_df = pd.DataFrame()

# 2️⃣ Récupérer les événements
print('\n2️⃣ Récupération des événements...')
try:
    response_events = requests.get(
        f'{API_URL}/analytics/events',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END}
    )
    if response_events.status_code == 200:
        events_data = response_events.json()
        events_df = pd.DataFrame(events_data)
        print(f'✅ {len(events_df)} événements récupérés')
    else:
        print(f'❌ Erreur:  {response_events.status_code}')
        events_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Erreur:   {str(e)}')
    events_df = pd.DataFrame()

# 3️⃣ Récupérer les KPIs
print('\n3️⃣ Récupération des KPIs...')
try:
    response_kpis = requests.get(
        f'{API_URL}/analytics/kpis',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END}
    )
    if response_kpis.status_code == 200:
        kpis_data = response_kpis.json()
        kpis_df = pd.DataFrame([kpis_data] if isinstance(kpis_data, dict) else kpis_data)
        print(f'✅ KPIs récupérés')
    else:
        print(f'❌ Erreur: {response_kpis.status_code}')
        kpis_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Erreur:  {str(e)}')
    kpis_df = pd.DataFrame()

# 4️⃣ Récupérer la timeline
print('\n4️⃣ Récupération de la timeline...')
try:
    response_timeline = requests.get(
        f'{API_URL}/analytics/timeline',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END}
    )
    if response_timeline.status_code == 200:
        timeline_data = response_timeline.json()
        timeline_df = pd.DataFrame(timeline_data)
        print(f'✅ Timeline récupérée')
    else:
        print(f'❌ Erreur:   {response_timeline.status_code}')
        timeline_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Erreur:   {str(e)}')
    timeline_df = pd.DataFrame()

# 5️⃣ Récupérer les sessions
print('\n5️⃣ Récupération des sessions...')
try:
    response_sessions = requests.get(
        f'{API_URL}/analytics/sessions',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END}
    )
    if response_sessions.status_code == 200:
        sessions_data = response_sessions.json()
        sessions_df = pd.DataFrame(sessions_data)
        print(f'✅ {len(sessions_df)} sessions récupérées')
    else:
        print(f'❌ Erreur: {response_sessions.status_code}')
        sessions_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Erreur:    {str(e)}')
    sessions_df = pd.DataFrame()

# 6️⃣ Récupérer les interviews par jour
print('\n6️⃣ Récupération des interviews par jour...')
try:
    response_interviews = requests.get(
        f'{API_URL}/interviews/analytics/per-day',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END}
    )
    if response_interviews.status_code == 200:
        interviews_data = response_interviews.json()
        interviews_df = pd.DataFrame(interviews_data)
        print(f'✅ Interviews par jour récupérés')
    else:
        print(f'❌ Erreur:  {response_interviews.status_code}')
        interviews_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Erreur:  {str(e)}')
    interviews_df = pd.DataFrame()

print('\n' + '=' * 60)
print('✅ Toutes les données ont été récupérées avec succès !')

# ============================================================
# 🔍 ÉTAPE 2 : Filtrage et enrichissement
# ============================================================

print('\n🔍 Filtrage et enrichissement des données...')
print('=' * 60)

# Convertir les dates
if not events_df.empty and 'created_at' in events_df.columns:
    events_df['created_at'] = pd.to_datetime(events_df['created_at'], errors='coerce')

if not timeline_df.empty and 'date' in timeline_df.columns:
    timeline_df['date'] = pd.to_datetime(timeline_df['date'], errors='coerce')

if not interviews_df.empty and 'date' in interviews_df.columns:
    interviews_df['date'] = pd.to_datetime(interviews_df['date'], errors='coerce')

print('✅ Dates converties')

# Créer les mappings pour les cabines
if not booths_df.empty and 'id' in booths_df.columns:
    booth_map = dict(zip(booths_df['id'], booths_df.get('name', booths_df.get('title', 'Unknown'))))
    print(f'✅ {len(booth_map)} cabines mappées')
else:
    booth_map = {}
    print('⚠️ Aucune cabine trouvée')

print('\n' + '=' * 60)
print('✅ Filtrage et enrichissement terminés !')

# ============================================================
# 📊 ÉTAPE 3 : Statistiques principales
# ============================================================

print('\n' + '=' * 60)
print(f'{ENV_STATUS}')
print('=' * 60)

# Initialiser les métriques
total_cv_created = 0
total_cv_printed = 0
total_job_offers_viewed = 0
total_sessions = 0
total_events = 0

# Calculer les métriques depuis les événements
if not events_df.empty:
    if 'event_type' in events_df.columns:
        event_counts = events_df['event_type'].value_counts()
        total_cv_created = event_counts.get('CV_CREATED', 0)
        total_cv_printed = event_counts.get('CV_PRINTED', 0)
        total_job_offers_viewed = event_counts.get('JOB_OFFER_VIEWED', 0)
    total_events = len(events_df)

# Calculer les sessions uniques
if not sessions_df.empty:
    total_sessions = len(sessions_df)

# Afficher les résultats
print(f'\n✓ Nombre total de CV créés: {total_cv_created}')
print(f'✓ Nombre total de CV imprimés: {total_cv_printed}')
print(f'✓ Nombre d\'offres consultées: {total_job_offers_viewed}')
print(f'✓ Nombre de sessions:   {total_sessions}')
print(f'✓ Nombre total d\'événements: {total_events}')

# Statistiques supplémentaires
if total_cv_created > 0:
    print(f'\n📊 Statistiques supplémentaires:')
    print(f'   - Taux d\'impression: {(total_cv_printed/total_cv_created)*100:.1f}%')
    print(f'   - Ratio offres/CV: {(total_job_offers_viewed/total_cv_created):.2f}')
    if total_sessions > 0:
        print(f'   - Événements par session: {total_events/total_sessions:.1f}')

# ============================================================
# 📈 ÉTAPE 4 : Analyse détaillée par cabine
# ============================================================

print('\n' + '=' * 60)
print('📈 ANALYSE DÉTAILLÉE PAR CABINE')
print('=' * 60)

if not events_df.empty and 'booth_id' in events_df.columns:
    booth_stats = events_df.groupby('booth_id').agg({
        'event_type': 'count'
    }).reset_index()
    booth_stats.columns = ['booth_id', 'total_events']
    booth_stats = booth_stats.sort_values('total_events', ascending=False)

    print(f'\n📊 Top cabines (par nombre d\'événements):')
    for idx, (_, row) in enumerate(booth_stats.head(10).iterrows(), 1):
        booth_id = row['booth_id']
        booth_name = booth_map.get(booth_id, f'Cabine {booth_id}')
        total = row['total_events']
        print(f'   {idx}. {booth_name}:   {total} événements')
else:
    print('⚠️ Aucune donnée par cabine disponible')

# ============================================================
# 📅 ÉTAPE 5 : Timeline - Évolution quotidienne
# ============================================================

print('\n' + '=' * 60)
print('📅 TIMELINE - Évolution quotidienne')
print('=' * 60)

if not timeline_df.empty:
    print(f'\n📊 Évolution des métriques (top 10 jours):')
    if 'date' in timeline_df.columns:
        timeline_sorted = timeline_df.sort_values('date', ascending=False).head(10)
    else:
        timeline_sorted = timeline_df.head(10)

    for _, row in timeline_sorted.iterrows():
        date = row.get('date', 'N/A')
        cv_created = row.get('cv_created', 0)
        cv_printed = row.get('cv_printed', 0)
        print(f'   {date}: CV créés:   {cv_created}, imprimés: {cv_printed}')
else:
    print('⚠️ Aucune donnée de timeline disponible')

# ============================================================
# 🔄 ÉTAPE 6 : Comparer STAGING vs PRODUCTION
# ============================================================

if COMPARE_ENVIRONMENTS and ENVIRONMENT == 'STAGING':
    print('\n' + '=' * 60)
    print('🔄 COMPARAISON STAGING vs PRODUCTION')
    print('=' * 60)
    print('\n⚠️ PRODUCTION est actuellement en statut COMING SOON')
    print('   URL:    https://app-api.ciblijob.fr/api')
    print('   Statut: 🔜 Pas encore déployée')
    print('   Cette comparaison sera disponible dès le déploiement.')
else:
    if COMPARE_ENVIRONMENTS:
        print('\nℹ️ La comparaison nécessite STAGING comme environnement de base.')

# ============================================================
# 💾 ÉTAPE 7 : Export Excel
# ============================================================

if EXPORT_TO_EXCEL:
    print('\n💾 Génération du fichier Excel...')
    print('=' * 60)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    env_label = 'STAGING' if ENVIRONMENT == 'STAGING' else 'PROD'
    excel_filename = f'exports/cabine_analytics_{env_label}_{DATE_START}_{DATE_END}_{timestamp}.xlsx'

    try:
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            # Feuille 1: Résumé
            print('\n1️⃣ Création de la feuille "Résumé"...')
            summary_data = {
                'Métrique': [
                    'Environnement',
                    'Période',
                    'CV créés',
                    'CV imprimés',
                    'Offres consultées',
                    'Sessions',
                    'Événements'
                ],
                'Valeur': [
                    ENVIRONMENT,
                    f'{DATE_START} à {DATE_END}',
                    total_cv_created,
                    total_cv_printed,
                    total_job_offers_viewed,
                    total_sessions,
                    total_events
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='📋 Résumé', index=False)

            # Feuille 2: Événements
            if not events_df.empty:
                print('2️⃣ Création de la feuille "Événements"...')
                events_df.to_excel(writer, sheet_name='📊 Événements', index=False)

            # Feuille 3: Timeline
            if not timeline_df.empty:
                print('3️⃣ Création de la feuille "Timeline"...')
                timeline_df.to_excel(writer, sheet_name='📅 Timeline', index=False)

            # Feuille 4: Par cabine
            if not events_df.empty and 'booth_id' in events_df.columns:
                print('4️⃣ Création de la feuille "Par Cabine"...')
                booth_summary = events_df.groupby('booth_id').size().reset_index(name='Total')
                booth_summary['Cabine'] = booth_summary['booth_id'].map(booth_map)
                booth_summary[['Cabine', 'Total']].to_excel(writer, sheet_name='🏢 Par Cabine', index=False)

            # Feuille 5: KPIs
            if not kpis_df.empty:
                print('5️⃣ Création de la feuille "KPIs"...')
                kpis_df.to_excel(writer, sheet_name='📈 KPIs', index=False)

        print(f'\n✅ Fichier Excel généré !')
        print(f'📍 Emplacement: {excel_filename}')
        print(f'📊 Feuilles créées:')
        print(f'   1.   📋 Résumé')
        print(f'   2. 📊 Événements')
        print(f'   3. 📅 Timeline')
        print(f'   4. 🏢 Par Cabine')
        print(f'   5. 📈 KPIs')
    except Exception as e:
        print(f'❌ Erreur lors de la création du fichier Excel: {str(e)}')

# ============================================================
# ✅ ÉTAPE 8 : Message de fin
# ============================================================

print('\n' + '=' * 60)
print('✅ ANALYSE TERMINÉE !')
print('=' * 60)
print(f'\nEnvironnement: {ENVIRONMENT}')
print(f'   {ENV_STATUS}')
print(f'   URL:   {API_URL}')
print(f'\nRésultats:  ')
print(f'   CV créés: {total_cv_created}')
print(f'   CV imprimés:  {total_cv_printed}')
print(f'   Offres consultées: {total_job_offers_viewed}')
print(f'\nComparaison:    {"✓ Oui (STAGING vs PRODUCTION)" if COMPARE_ENVIRONMENTS else "✗ Non"}')
print('\n' + '=' * 60)

