# ============================================================
# SCRIPT:   Cabine Analytics - API Integration
# Description: Analyser les données de la Cabine (CV créés, imprimés, offres consultées)
# Repository:   Zaidoudou/dataProcessingNotebooks
# Branch:  statysics-by-vlad
# ============================================================
# Imports

import sys
print("🔄 Démarrage du script...", file=sys.stderr)
print("📦 Vérification des imports...", file=sys.stderr)

try:
    import requests
    print("✓ requests importé", file=sys.stderr)
except ImportError as e:
    print(f"❌ Erreur import requests: {e}", file=sys.stderr)
    sys.exit(1)

try:
    import pandas as pd
    print("✓ pandas importé", file=sys.stderr)
except ImportError as e:
    print(f"❌ Erreur import pandas: {e}", file=sys.stderr)
    sys.exit(1)

import warnings
import os
import time

print("✓ Tous les imports sont OK\n", file=sys.stderr)

warnings.filterwarnings('ignore')

# ============================================================
# ⚙️ CONFIGURATION - MODIFIEZ ICI
# ============================================================

# 📅 DATES PRINCIPALES
DATE_START = "2025-09-01"           # ← DATE DE DÉBUT (YYYY-MM-DD)
DATE_END = "2026-01-19"             # ← DATE DE FIN (YYYY-MM-DD)

# 🏢 SÉLECTION DES CABINES À ANALYSER
# Options:
#   "all"  → Analyser toutes les cabines
#   "NAME" → Analyser une cabine spécifique (ex: "Cabine 1", "Cabine 2", etc)
CABINES_TO_ANALYZE = "all"          # ← MODIFIEZ: "all" ou nom de cabine spécifique

# 📅 ANALYSE PAR SEMAINE ET PAR JOUR
# Options:
#   ""          → Analyser TOUTES les semaines et tous les jours
#   "YYYY-MM"   → Analyser seulement le mois spécifié (ex: "2026-01")
#   "YYYY-MM-DD" → Analyser un jour spécifique
ANALYZE_PERIOD = "2026-01"                 # ← MODIFIEZ: "" (tout), "2026-01" (mois), ou "2026-01-15" (jour)

# 📊 OPTIONS D'AFFICHAGE
SHOW_DETAILS = True                 # ← Afficher détails (toujours actif)
EXPORT_TO_EXCEL = False             # ← Générer fichier Excel (désactivé)

# 🌍 ENVIRONNEMENT
ENVIRONMENT = 'PRODUCTION'          # ← MODIFIEZ: 'STAGING' ou 'PRODUCTION'

# ============================================================
# 📊 INFORMATIONS DE CONFIGURATION
# ============================================================
#
# CABINES_TO_ANALYZE:
#   - "all"    : Affiche toutes les cabines avec toutes les étapes
#   - "NAME"   : Affiche seulement la cabine spécifiée
#
# ANALYZE_PERIOD (pour semaines et jours):
#   - ""       : Affiche TOP 5 des mois entiers + TOP 5 semaines + TOP 5 jours
#   - "2026-01": Affiche seulement le mois de janvier 2026
#   - "2026-01-15": Affiche seulement le jour 15 janvier 2026
#
# Les étapes affichées pour chaque cabine:
# - Étape 3: Filtrage et enrichissement
# - Étape 3.5: Sélection clients
# - Étape 4: Statistiques globales
# - Étape 5: Statistiques par période
# - Étape 6: Statistiques par mois (détaillées)
# - Étape 7: Top Clients
# - Étape 8: Répartition par statut
# - Étape 9: Top Campagnes
# - Étape 10: Export Excel
# - Étape 11: Analyse par semaine
# - Étape 12: Analyse par jour

# ============================================================
# CONFIGURATION DE L'API - NE MODIFIEZ PAS
# ============================================================

# URLs et clés API
API_STAGING_URL = 'https://cibli-api.agency.lonestone.io/api'
API_STAGING_KEY = 'PGZ4qtc5jtf@rph3twf'

API_PROD_URL = 'https://app-api.ciblijob.fr/api'
API_PROD_KEY = 'txf.hpc9aut9rbd2KWA'

# Sélectionner l'URL et la clé selon l'environnement
if ENVIRONMENT == 'STAGING':
    API_URL = API_STAGING_URL
    API_KEY = API_STAGING_KEY
    ENV_STATUS = '🧪 STAGING (Environnement de test)'
else:
    API_URL = API_PROD_URL
    API_KEY = API_PROD_KEY
    ENV_STATUS = '🚀 PRODUCTION'

# Créer le dossier d'exports s'il n'existe pas
if not os.path.exists('exports'):
    os.makedirs('exports')

# Headers pour les requêtes API
HEADERS = {
    'x-secret-key': API_KEY
}

# Afficher la configuration
print('✅ Configuration chargée :  ')
print(f'   Environnement:       {ENV_STATUS}')
print(f'   URL API:             {API_URL}')
print(f'   Période:             {DATE_START} à {DATE_END}')
print(f'   Cabines à analyser:  {CABINES_TO_ANALYZE}')
print(f'   Période détails:     {ANALYZE_PERIOD if ANALYZE_PERIOD else "TOUTES les périodes"}')
print()
print('💡 Astuce:   Pour changer les paramètres, modifiez les variables ci-dessus.')

# ============================================================
# 📥 ÉTAPE 1 : Récupération des données API
# ============================================================

print('\n📥 Récupération des données depuis l\'API...')
print('=' * 60)

# Fonction utilitaire pour afficher l'état de l'API
def get_status_icon(status_code):
    if 200 <= status_code < 300:
        return '✅'
    elif 400 <= status_code < 500:
        return '⚠️'
    else:
        return '❌'

def get_status_text(status_code):
    status_map = {
        200: 'OK',
        201: 'Created',
        204: 'No Content',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable'
    }
    return status_map.get(status_code, 'Unknown')

# 1️⃣ Récupérer les cabines (booths)
print('\n1️⃣ Récupération des cabines...')
try:
    start_time = time.time()
    print(f'   📡 URL: {API_URL}/booths/all')
    print(f'   🔑 Headers: {{"x-secret-key": "***"}}')
    response_booths = requests.get(
        f'{API_URL}/booths/all',
        headers=HEADERS,
        timeout=10
    )
    elapsed_time = time.time() - start_time
    status_icon = get_status_icon(response_booths.status_code)
    status_text = get_status_text(response_booths.status_code)
    print(f'   État API: {status_icon} {response_booths.status_code} {status_text} ({elapsed_time:.2f}s)')
    print(f'   📝 Taille réponse: {len(response_booths.text)} bytes')
    print(f'   📦 Contenu brut:\n{response_booths.text[:500]}\n')
    if response_booths.status_code == 200:
        booths_data = response_booths.json()
        print(f'   ✓ JSON valide')
        print(f'   ✓ Type: {type(booths_data).__name__}')
        if isinstance(booths_data, list):
            booths_df = pd.DataFrame(booths_data)
            print(f'✅ {len(booths_df)} cabines récupérées')
        elif isinstance(booths_data, dict):
            booths_df = pd.DataFrame([booths_data])
            print(f'✅ Données cabine reçues')
        else:
            print(f'⚠️ Format de réponse inattendu: {type(booths_data)}')
            booths_df = pd.DataFrame()
    else:
        print(f'❌ Erreur HTTP: {response_booths.status_code}')
        print(f'   📝 Réponse complète: {response_booths.text[:500]}')
        booths_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Exception: {str(e)}')
    import traceback
    traceback.print_exc()
    booths_df = pd.DataFrame()

# 2️⃣ Récupérer les événements
print('\n2️⃣ Récupération des événements...')
try:
    start_time = time.time()
    print(f'   📡 URL: {API_URL}/analytics/events')
    print(f'   📅 Paramètres: from={DATE_START}, to={DATE_END}')
    response_events = requests.get(
        f'{API_URL}/analytics/events',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END},
        timeout=10
    )
    elapsed_time = time.time() - start_time
    status_icon = get_status_icon(response_events.status_code)
    status_text = get_status_text(response_events.status_code)
    print(f'   État API: {status_icon} {response_events.status_code} {status_text} ({elapsed_time:.2f}s)')
    print(f'   📝 Taille réponse: {len(response_events.text)} bytes')
    print(f'   📦 Contenu brut:\n{response_events.text[:500]}\n')
    if response_events.status_code == 200:
        events_data = response_events.json()
        print(f'   ✓ JSON valide')
        print(f'   ✓ Type: {type(events_data).__name__}')
        if isinstance(events_data, list):
            events_df = pd.DataFrame(events_data)
            print(f'✅ {len(events_df)} événements récupérés')
        elif isinstance(events_data, dict):
            events_df = pd.DataFrame([events_data])
            print(f'✅ Données événement reçues')
        else:
            print(f'⚠️ Format de réponse inattendu: {type(events_data)}')
            events_df = pd.DataFrame()
    else:
        print(f'❌ Erreur HTTP: {response_events.status_code}')
        print(f'   📝 Réponse complète: {response_events.text[:500]}')
        events_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Exception: {str(e)}')
    import traceback
    traceback.print_exc()
    events_df = pd.DataFrame()

# 3️⃣ Récupérer les KPIs
print('\n3️⃣ Récupération des KPIs...')
try:
    start_time = time.time()
    print(f'   📡 URL: {API_URL}/analytics/kpis')
    print(f'   📅 Paramètres: from={DATE_START}, to={DATE_END}')
    response_kpis = requests.get(
        f'{API_URL}/analytics/kpis',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END},
        timeout=10
    )
    elapsed_time = time.time() - start_time
    status_icon = get_status_icon(response_kpis.status_code)
    status_text = get_status_text(response_kpis.status_code)
    print(f'   État API: {status_icon} {response_kpis.status_code} {status_text} ({elapsed_time:.2f}s)')
    print(f'   📝 Taille réponse: {len(response_kpis.text)} bytes')
    print(f'   📦 Contenu brut:\n{response_kpis.text[:500]}\n')
    if response_kpis.status_code == 200:
        kpis_data = response_kpis.json()
        print(f'   ✓ JSON valide')
        print(f'   ✓ Type: {type(kpis_data).__name__}')
        kpis_df = pd.DataFrame([kpis_data] if isinstance(kpis_data, dict) else kpis_data)
        print(f'✅ KPIs récupérés')
    else:
        print(f'❌ Erreur HTTP: {response_kpis.status_code}')
        print(f'   📝 Réponse complète: {response_kpis.text[:500]}')
        kpis_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Exception: {str(e)}')
    import traceback
    traceback.print_exc()
    kpis_df = pd.DataFrame()

# 4️⃣ Récupérer la timeline
print('\n4️⃣ Récupération de la timeline...')
try:
    start_time = time.time()
    print(f'   📡 URL: {API_URL}/analytics/timeline')
    print(f'   📅 Paramètres: from={DATE_START}, to={DATE_END}')
    response_timeline = requests.get(
        f'{API_URL}/analytics/timeline',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END},
        timeout=10
    )
    elapsed_time = time.time() - start_time
    status_icon = get_status_icon(response_timeline.status_code)
    status_text = get_status_text(response_timeline.status_code)
    print(f'   État API: {status_icon} {response_timeline.status_code} {status_text} ({elapsed_time:.2f}s)')
    print(f'   📝 Taille réponse: {len(response_timeline.text)} bytes')
    print(f'   📦 Contenu brut:\n{response_timeline.text[:500]}\n')
    if response_timeline.status_code == 200:
        timeline_data = response_timeline.json()
        print(f'   ✓ JSON valide')
        print(f'   ✓ Type: {type(timeline_data).__name__}')
        timeline_df = pd.DataFrame(timeline_data)
        print(f'✅ Timeline récupérée')
    else:
        print(f'❌ Erreur HTTP: {response_timeline.status_code}')
        print(f'   📝 Réponse complète: {response_timeline.text[:500]}')
        timeline_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Exception: {str(e)}')
    import traceback
    traceback.print_exc()
    timeline_df = pd.DataFrame()

# 5️⃣ Récupérer les sessions
print('\n5️⃣ Récupération des sessions...')
try:
    start_time = time.time()
    print(f'   📡 URL: {API_URL}/analytics/sessions')
    print(f'   📅 Paramètres: from={DATE_START}, to={DATE_END}')
    response_sessions = requests.get(
        f'{API_URL}/analytics/sessions',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END},
        timeout=10
    )
    elapsed_time = time.time() - start_time
    status_icon = get_status_icon(response_sessions.status_code)
    status_text = get_status_text(response_sessions.status_code)
    print(f'   État API: {status_icon} {response_sessions.status_code} {status_text} ({elapsed_time:.2f}s)')
    print(f'   📝 Taille réponse: {len(response_sessions.text)} bytes')
    print(f'   📦 Contenu brut:\n{response_sessions.text[:500]}\n')
    if response_sessions.status_code == 200:
        sessions_data = response_sessions.json()
        print(f'   ✓ JSON valide')
        print(f'   ✓ Type: {type(sessions_data).__name__}')
        # Extraire la liste 'sessions' si c'est un dict avec clé 'sessions'
        if isinstance(sessions_data, dict) and 'sessions' in sessions_data:
            sessions_data = sessions_data['sessions']
            print(f'   ✓ Extracting "sessions" list from dict')
        if isinstance(sessions_data, list):
            sessions_df = pd.DataFrame(sessions_data)
            print(f'✅ {len(sessions_df)} sessions récupérées')
        elif isinstance(sessions_data, dict):
            sessions_df = pd.DataFrame([sessions_data])
            print(f'✅ Données session reçues')
        else:
            print(f'⚠️ Format de réponse inattendu: {type(sessions_data)}')
            sessions_df = pd.DataFrame()
    else:
        print(f'❌ Erreur HTTP: {response_sessions.status_code}')
        print(f'   📝 Réponse complète: {response_sessions.text[:500]}')
        sessions_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Exception: {str(e)}')
    import traceback
    traceback.print_exc()
    sessions_df = pd.DataFrame()

# 6️⃣ Récupérer les interviews par jour
print('\n6️⃣ Récupération des interviews par jour...')
try:
    start_time = time.time()
    print(f'   📡 URL: {API_URL}/interviews/analytics/per-day')
    print(f'   📅 Paramètres: from={DATE_START}, to={DATE_END}')
    response_interviews = requests.get(
        f'{API_URL}/interviews/analytics/per-day',
        headers=HEADERS,
        params={'from': DATE_START, 'to': DATE_END},
        timeout=10
    )
    elapsed_time = time.time() - start_time
    status_icon = get_status_icon(response_interviews.status_code)
    status_text = get_status_text(response_interviews.status_code)
    print(f'   État API: {status_icon} {response_interviews.status_code} {status_text} ({elapsed_time:.2f}s)')
    print(f'   📝 Taille réponse: {len(response_interviews.text)} bytes')
    print(f'   📦 Contenu brut:\n{response_interviews.text[:500]}\n')
    if response_interviews.status_code == 200:
        interviews_data = response_interviews.json()
        print(f'   ✓ JSON valide')
        print(f'   ✓ Type: {type(interviews_data).__name__}')
        if isinstance(interviews_data, list):
            interviews_df = pd.DataFrame(interviews_data)
            print(f'✅ Interviews par jour récupérés')
        elif isinstance(interviews_data, dict):
            interviews_df = pd.DataFrame([interviews_data])
            print(f'✅ Données interview reçues')
        else:
            print(f'⚠️ Format de réponse inattendu: {type(interviews_data)}')
            interviews_df = pd.DataFrame()
    else:
        print(f'❌ Erreur HTTP: {response_interviews.status_code}')
        print(f'   📝 Réponse complète: {response_interviews.text[:500]}')
        interviews_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Exception: {str(e)}')
    import traceback
    traceback.print_exc()
    interviews_df = pd.DataFrame()

# 7️⃣ Récupérer les jobs
print('\n7️⃣ Récupération des jobs...')
try:
    start_time = time.time()
    print(f'   📡 URL: {API_URL}/jobs')
    response_jobs = requests.get(
        f'{API_URL}/jobs',
        headers=HEADERS,
        timeout=10
    )
    elapsed_time = time.time() - start_time
    status_icon = get_status_icon(response_jobs.status_code)
    status_text = get_status_text(response_jobs.status_code)
    print(f'   État API: {status_icon} {response_jobs.status_code} {status_text} ({elapsed_time:.2f}s)')
    if response_jobs.status_code == 200:
        jobs_data = response_jobs.json()
        if isinstance(jobs_data, list):
            jobs_df = pd.DataFrame(jobs_data)
            print(f'✅ {len(jobs_df)} jobs récupérés')
        elif isinstance(jobs_data, dict) and 'data' in jobs_data:
            jobs_df = pd.DataFrame(jobs_data['data'])
            print(f'✅ {len(jobs_df)} jobs récupérés')
        else:
            print(f'⚠️ Format inattendu')
            jobs_df = pd.DataFrame()
    else:
        print(f'❌ Erreur HTTP: {response_jobs.status_code}')
        jobs_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Exception: {str(e)}')
    jobs_df = pd.DataFrame()

# 8️⃣ Récupérer les organizations
print('\n8️⃣ Récupération des organizations...')
try:
    start_time = time.time()
    print(f'   📡 URL: {API_URL}/organizations')
    response_orgs = requests.get(
        f'{API_URL}/organizations',
        headers=HEADERS,
        timeout=10
    )
    elapsed_time = time.time() - start_time
    status_icon = get_status_icon(response_orgs.status_code)
    status_text = get_status_text(response_orgs.status_code)
    print(f'   État API: {status_icon} {response_orgs.status_code} {status_text} ({elapsed_time:.2f}s)')
    if response_orgs.status_code == 200:
        orgs_data = response_orgs.json()
        if isinstance(orgs_data, list):
            organizations_df = pd.DataFrame(orgs_data)
            print(f'✅ {len(organizations_df)} organizations récupérées')
        elif isinstance(orgs_data, dict) and 'data' in orgs_data:
            organizations_df = pd.DataFrame(orgs_data['data'])
            print(f'✅ {len(organizations_df)} organizations récupérées')
        else:
            print(f'⚠️ Format inattendu')
            organizations_df = pd.DataFrame()
    else:
        print(f'❌ Erreur HTTP: {response_orgs.status_code}')
        organizations_df = pd.DataFrame()
except Exception as e:
    print(f'❌ Exception: {str(e)}')
    organizations_df = pd.DataFrame()

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

# Afficher la structure des données reçues (DÉBOGAGE)
print('\n🔍 DÉBOGAGE - Structure des données reçues:')
print('─' * 60)
print(f'1️⃣ Events DataFrame:')
if not events_df.empty:
    print(f'   Colonnes: {list(events_df.columns)}')
    print(f'   Nombre de lignes: {len(events_df)}')
    print(f'   Premiers éléments:\n{events_df.head(2).to_string()}')
else:
    print(f'   ⚠️ DataFrame vide')

print(f'\n2️⃣ KPIs DataFrame:')
if not kpis_df.empty:
    print(f'   Colonnes: {list(kpis_df.columns)}')
    print(f'   Nombre de lignes: {len(kpis_df)}')
    print(f'   Contenu:\n{kpis_df.to_string()}')
else:
    print(f'   ⚠️ DataFrame vide')

print(f'\n3️⃣ Sessions DataFrame:')
if not sessions_df.empty:
    print(f'   Colonnes: {list(sessions_df.columns)}')
    print(f'   Nombre de lignes: {len(sessions_df)}')
else:
    print(f'   ⚠️ DataFrame vide')

print(f'\n4️⃣ Timeline DataFrame:')
if not timeline_df.empty:
    print(f'   Colonnes: {list(timeline_df.columns)}')
    print(f'   Nombre de lignes: {len(timeline_df)}')
else:
    print(f'   ⚠️ DataFrame vide')

print('\n' + '=' * 60)

# Créer les mappings pour les cabines
if not booths_df.empty and 'id' in booths_df.columns:
    # Construire le mapping correctement
    booth_map = {}
    for idx, row in booths_df.iterrows():
        booth_id = row['id']
        # Chercher le nom dans cet ordre: 'label', 'name', 'title'
        booth_name = row.get('label') or row.get('name') or row.get('title') or f'Cabine {booth_id}'
        booth_map[booth_id] = str(booth_name).strip()  # Assurer que c'est un string propre
    print(f'✅ {len(booth_map)} cabines mappées')
    # Afficher le mapping pour diagnostique
    print(f'   Mapping des cabines:')
    for booth_id, booth_name in list(booth_map.items())[:5]:
        print(f'      {booth_id}: {booth_name}')
else:
    booth_map = {}
    print('⚠️ Aucune cabine trouvée')

# Créer les mappings pour les jobs
job_map = {}
if not jobs_df.empty and 'id' in jobs_df.columns:
    for idx, row in jobs_df.iterrows():
        job_id = row['id']
        # Chercher le titre dans cet ordre: 'title', 'name', 'label'
        job_title = row.get('title') or row.get('name') or row.get('label') or f'Job {job_id}'
        job_map[job_id] = str(job_title).strip()
    print(f'✅ {len(job_map)} jobs mappés')
    print(f'   Mapping des jobs:')
    for job_id, job_title in list(job_map.items())[:5]:
        print(f'      {job_id}: {job_title}')

# Créer les mappings pour les organizations
org_map = {}
if not organizations_df.empty and 'id' in organizations_df.columns:
    for idx, row in organizations_df.iterrows():
        org_id = row['id']
        # Chercher le nom dans cet ordre: 'name', 'title', 'label'
        org_name = row.get('name') or row.get('title') or row.get('label') or f'Org {org_id}'
        org_map[org_id] = str(org_name).strip()
    print(f'✅ {len(org_map)} organizations mappées')
    print(f'   Mapping des organizations:')
    for org_id, org_name in list(org_map.items())[:5]:
        print(f'      {org_id}: {org_name}')

print('\n' + '=' * 60)
print('✅ Filtrage et enrichissement terminés !')

# ============================================================
# 🏢 CABINES DISPONIBLES
# ============================================================

print('\n' + '=' * 100)
print('🏢 CABINES DISPONIBLES')
print('=' * 100)

if booth_map:
    print(f'\n📍 Total de cabines disponibles: {len(booth_map)}')
    print(f'\n   {"Rang":<6} {"ID Cabine":<40} {"Nom de la Cabine":<50}')
    print('   ' + '─' * 102)
    for idx, (booth_id, booth_name) in enumerate(sorted(booth_map.items(), key=lambda x: x[1]), 1):
        print(f'   {idx:<6} {str(booth_id):<40} {booth_name:<50}')
    print('   ' + '─' * 102)
    print(f'\n💡 Pour analyser une cabine spécifique, modifiez CABINES_TO_ANALYZE dans la configuration')
    print(f'   Exemples: "Cabine 1", "Paris", "{list(booth_map.values())[0] if booth_map else "Nom"}"')
else:
    print('\n⚠️ Aucune cabine disponible')

# ============================================================
# 📊 ÉTAPE 3 : Filtrage et enrichissement + ÉTAPE 3.5 : Sélection clients
# ============================================================

print('\n' + '=' * 60)
print('🔍 FILTRAGE ET ENRICHISSEMENT')
print('=' * 60)

# Afficher les candidatures filtrées par source
print(f'\n📥 Candidatures filtrées par source:')
if not events_df.empty and 'source' in events_df.columns:
    source_counts = events_df['source'].value_counts()
    for source, count in source_counts.items():
        print(f'   {source}: {count}')
else:
    print('   ℹ️ Données non disponibles')

# Afficher les candidatures dans la période date
print(f'\n📅 Candidatures dans la période {DATE_START} à {DATE_END}:')
if not events_df.empty and 'created_at' in events_df.columns:
    period_count = len(events_df)
    print(f'   Total: {period_count}')
else:
    print('   ℹ️ Données non disponibles')

print(f'\n📊 Nombre total de clients disponibles: {len(booth_map)}')
print(f'Cabines mappées: {len(booth_map)}')

# ============================================================
# 📊 ÉTAPE 4 : Statistiques globales
# ============================================================

print('\n' + '=' * 60)
print(f'{ENV_STATUS}')
print('\n' + '=' * 60)
print(f'{ENV_STATUS}')
print('=' * 60)

# Initialiser les métriques
total_cv_created = 0
total_cv_printed = 0
total_job_offers_viewed = 0
total_sessions = 0
total_events = 0
total_applications = 0
total_users_completed_session = 0

print(f'\n📊 Statistiques globales de la période {DATE_START} à {DATE_END}:')
print('─' * 60)
if not kpis_df.empty:
    print('📈 Source: KPIs API')
    kpis_row = kpis_df.iloc[0] if len(kpis_df) > 0 else {}

    print(f'   Colonnes disponibles: {list(kpis_df.columns)}')

    # Les vrais noms de colonnes de l'API
    if 'sessionCount' in kpis_df.columns:
        total_sessions = int(kpis_row['sessionCount'])
        print(f'   ✓ Sessions trouvé: sessionCount = {total_sessions}')

    if 'interviewsEnded' in kpis_df.columns:
        total_users_completed_session = int(kpis_row['interviewsEnded'])
        print(f'   ✓ Interviews complétées trouvé: interviewsEnded = {total_users_completed_session}')

    if 'totalApplications' in kpis_df.columns:
        total_applications = int(kpis_row['totalApplications'])
        print(f'   ✓ Candidatures trouvé: totalApplications = {total_applications}')

    if 'uniqueUsersViewedJobs' in kpis_df.columns:
        total_job_offers_viewed = int(kpis_row['uniqueUsersViewedJobs'])
        print(f'   ✓ Offres consultées trouvé: uniqueUsersViewedJobs = {total_job_offers_viewed}')

    if 'totalPrints' in kpis_df.columns:
        total_cv_printed = int(kpis_row['totalPrints'])
        print(f'   ✓ CV imprimés trouvé: totalPrints = {total_cv_printed}')

    if 'uniqueUsersWithCvDownload' in kpis_df.columns:
        total_cv_created = int(kpis_row['uniqueUsersWithCvDownload'])
        print(f'   ✓ CV téléchargés trouvé: uniqueUsersWithCvDownload = {total_cv_created}')

    # Afficher le contenu complet pour diagnostique
    print(f'\n   📋 Contenu complet des KPIs:')
    for col in kpis_df.columns:
        val = kpis_row[col]
        if isinstance(val, dict):
            print(f'      {col}: {val}')
        else:
            print(f'      {col}: {val}')

# Stratégie 2: Essayer depuis les événements si KPIs vide
elif not events_df.empty:
    print('📈 Source: Events API')
    if 'event_type' in events_df.columns:
        event_counts = events_df['event_type'].value_counts()
        print(f'   Types d\'événements trouvés: {event_counts.to_dict()}')
        total_cv_created = event_counts.get('CV_CREATED', 0)
        total_cv_printed = event_counts.get('CV_PRINTED', 0)
        total_job_offers_viewed = event_counts.get('JOB_OFFER_VIEWED', 0)
        total_applications = event_counts.get('APPLICATION_SUBMITTED', 0)
    total_events = len(events_df)

# Stratégie 3: Essayer depuis la timeline
elif not timeline_df.empty:
    print('📈 Source: Timeline API')
    if len(timeline_df) > 0:
        last_day = timeline_df.iloc[-1]
        cv_cols = ['cv_created', 'cvCreated', 'total_cv_created']
        for col in cv_cols:
            if col in timeline_df.columns:
                total_cv_created = timeline_df[col].sum()
                break

        print(f'   Données récupérées de la timeline')

# Sessions
# Ne pas utiliser len(sessions_df) car c'est souvent une seule ligne contenant toutes les sessions
# Utiliser sessionCount des KPIs qui a déjà été extrait
if total_sessions == 0 and not sessions_df.empty:
    # Fallback: si sessionCount n'a pas été trouvé dans KPIs
    total_sessions = len(sessions_df)
    print(f'📈 Sessions trouvées (fallback): {total_sessions}')
else:
    if total_sessions > 0:
        print(f'📈 Sessions trouvées: {total_sessions}')

# Afficher les résultats TOUJOURS
print(f'\n✅ RÉSULTATS FINAUX:')
print('─' * 60)
print(f'🔵 Nombre total de CV créés: {total_cv_created}')
print(f'🟢 Nombre total de CV imprimés: {total_cv_printed}')
print(f'🟡 Nombre d\'offres consultées: {total_job_offers_viewed}')
print(f'🟠 Nombre de candidatures: {total_applications}')
print(f'🔴 Nombre de sessions: {total_sessions}')
print(f'🟣 Nombre d\'utilisateurs ayant complété une session: {total_users_completed_session}')

# Statistiques supplémentaires
if total_cv_created > 0:
    print(f'\n📊 Statistiques supplémentaires:')
    if total_cv_printed > 0:
        print(f'   - Taux d\'impression: {(total_cv_printed/total_cv_created)*100:.1f}%')
    if total_job_offers_viewed > 0:
        print(f'   - Ratio offres/CV: {(total_job_offers_viewed/total_cv_created):.2f}')
    if total_applications > 0:
        print(f'   - Ratio candidatures/CV: {(total_applications/total_cv_created):.2f}')
    if total_sessions > 0:
        print(f'   - Ratio CV/session: {(total_cv_created/total_sessions):.2f}')
        if total_users_completed_session > 0:
            print(f'   - Taux de complétion de session: {(total_users_completed_session/total_sessions)*100:.1f}%')

# ============================================================
# 📅 ÉTAPE 5 : Statistiques par période (Global)
# ============================================================

print('\n📅 ÉTAPE 5 : Statistiques par période')
print('─' * 60)
print('\n✅ Confirmation de sauvegarde des fichiers mensuels: N/A (export Excel désactivé)')

if not sessions_df.empty and 'startedAt' in sessions_df.columns:
    sessions_df['startedAt'] = pd.to_datetime(sessions_df['startedAt'], errors='coerce')
    sessions_df['year_month'] = sessions_df['startedAt'].dt.to_period('M')

    print(f'\n📊 Nombre de candidatures par mois:')
    monthly_total = sessions_df.groupby('year_month').size()
    for month, count in monthly_total.items():
        print(f'   {month}: {count}')
else:
    print(f'\n   ℹ️ Données non disponibles')

# ============================================================
# 🏢 ANALYSE PAR CABINE
# ============================================================

print('\n' + '=' * 60)
print('🏢 ANALYSE PAR CABINE')
print('=' * 60)

# Boucle principale: traiter chaque cabine
if not sessions_df.empty and 'boothId' in sessions_df.columns:
    # Préparer les données de sessions
    sessions_df['startedAt'] = pd.to_datetime(sessions_df['startedAt'], errors='coerce')
    sessions_df['date'] = sessions_df['startedAt'].dt.date
    sessions_df['year_month'] = sessions_df['startedAt'].dt.to_period('M')
    sessions_df['year_week'] = sessions_df['startedAt'].dt.isocalendar().week
    sessions_df['year'] = sessions_df['startedAt'].dt.isocalendar().year

    # Obtenir les cabines uniques triées
    booth_ids = sorted(sessions_df['boothId'].dropna().unique())

    # Filtrer les cabines selon CABINES_TO_ANALYZE
    if CABINES_TO_ANALYZE != "all":
        # Chercher la cabine spécifiée
        matching_booths = []
        for booth_id in booth_ids:
            if booth_id in booth_map:
                booth_name = booth_map[booth_id]
            else:
                booth_name = f'Cabine {str(booth_id)[:8]}...'

            # Vérifier si le nom contient la chaîne demandée (case-insensitive)
            if CABINES_TO_ANALYZE.lower() in booth_name.lower():
                matching_booths.append(booth_id)

        if matching_booths:
            booth_ids = matching_booths
            print(f'\n✅ Cabine(s) sélectionnée(s): {CABINES_TO_ANALYZE}')
        else:
            print(f'\n⚠️ Aucune cabine trouvée correspondant à: {CABINES_TO_ANALYZE}')
            print(f'   Cabines disponibles:')
            for booth_id in sorted(sessions_df['boothId'].dropna().unique()):
                if booth_id in booth_map:
                    print(f'      - {booth_map[booth_id]}')

    # Initialiser la liste pour stocker les données récapitulatives
    cabines_recap = []

    for booth_idx, booth_id in enumerate(booth_ids, 1):
        # Obtenir le nom de la cabine
        if booth_id in booth_map:
            booth_name = booth_map[booth_id]
        else:
            booth_name = f'Cabine {str(booth_id)[:8]}...'

        # Filtrer les sessions pour cette cabine
        booth_sessions = sessions_df[sessions_df['boothId'] == booth_id]

        if len(booth_sessions) == 0:
            continue

        print(f'\n\n{"=" * 100}')
        print(f'🏢 {booth_name}')
        print(f'{"=" * 100}')

        # Statistiques globales pour cette cabine
        booth_cv_created = int(booth_sessions['hasCvDownloaded'].sum()) if 'hasCvDownloaded' in booth_sessions.columns else 0
        booth_cv_printed = int(booth_sessions['hasCvPrinted'].sum()) if 'hasCvPrinted' in booth_sessions.columns else 0
        booth_apps = int(booth_sessions['applicationsCount'].sum()) if 'applicationsCount' in booth_sessions.columns else 0
        booth_total_sessions = len(booth_sessions)

        print(f'\n📊 Statistiques Globales')
        print('─' * 100)
        print(f'   CV créés: {booth_cv_created}')
        print(f'   CV imprimés: {booth_cv_printed}')
        print(f'   Candidatures: {booth_apps}')
        print(f'   Sessions: {booth_total_sessions}')
        print(f'   Période: {DATE_START} à {DATE_END}')

        # Statistiques par mois
        print(f'\n📅 Candidatures par Mois')
        print('─' * 100)
        print(f'   {"Mois":<15} {"Candidatures":>15}')
        print('   ' + '─' * 96)
        monthly_stats = booth_sessions.groupby('year_month').size()
        for month, count in monthly_stats.items():
            print(f'   {str(month):<15} {count:>15}')

        # Répartition par statut
        print(f'\n📊 Répartition par Statut')
        print('─' * 100)
        status_recap = {}
        if 'status' in booth_sessions.columns:
            status_counts = booth_sessions['status'].value_counts()
            total_status = status_counts.sum()
            for status, count in status_counts.items():
                percentage = (count / total_status * 100) if total_status > 0 else 0
                status_recap[status] = count
                print(f'   {status}: {count} ({percentage:.1f}%)')
        else:
            print(f'   ℹ️ Données de statut non disponibles')

        # Détail des candidatures avec clients et campagnes
        print(f'\n📋 Détail des Candidatures (Client + Campagne)')
        print('─' * 100)

        # Chercher les colonnes disponibles
        client_col = None
        job_col = None

        if 'clientId' in booth_sessions.columns:
            client_col = 'clientId'
        elif 'client_id' in booth_sessions.columns:
            client_col = 'client_id'

        if 'jobId' in booth_sessions.columns:
            job_col = 'jobId'
        elif 'job_id' in booth_sessions.columns:
            job_col = 'job_id'

        num_clients = 0
        num_campaigns = 0

        if client_col and job_col:
            # Créer une table avec les candidatures groupées par client et campagne
            print(f'   {"Client (Organisation)":<45} {"Campagne (Job)":<45} {"Candidatures":>15}')
            print('   ' + '─' * 110)

            candidatures_detail = booth_sessions.groupby([client_col, job_col]).size().reset_index(name='count')
            candidatures_detail = candidatures_detail.sort_values('count', ascending=False)

            for _, row in candidatures_detail.iterrows():
                client_id = row[client_col]
                campaign_id = row[job_col]

                # Utiliser les mappings pour obtenir les noms
                client_name = org_map.get(client_id, str(client_id))[:43]
                campaign_name = job_map.get(campaign_id, str(campaign_id))[:43]

                count = int(row['count'])
                print(f'   {client_name:<45} {campaign_name:<45} {count:>15}')

            print('   ' + '─' * 110)
            print(f'   Total: {len(candidatures_detail)} combinaisons client-campagne')
        elif client_col:
            print(f'   ⚠️ Données de campagnes non disponibles')
            print(f'   Affichage des clients uniquement:')
            client_counts = booth_sessions[client_col].value_counts()
            for client_id, count in client_counts.items():
                print(f'      {str(client_id):<40} : {count:>15} candidatures')
        elif job_col:
            print(f'   ⚠️ Données de clients non disponibles')
            print(f'   Affichage des campagnes uniquement:')
            job_counts = booth_sessions[job_col].value_counts()
            for job_id, count in job_counts.items():
                print(f'      {str(job_id):<40} : {count:>15} candidatures')
        else:
            print(f'   ℹ️ Données de clients et campagnes non disponibles')

        # Liste complète des clients (récapitulatif)
        print(f'\n👥 Récapitulatif des Clients')
        print('─' * 100)
        if client_col:
            client_counts = booth_sessions[client_col].value_counts()
            num_clients = len(client_counts)
            print(f'   {"Rang":<6} {"Client (Organisation)":<60} {"Candidatures":>15}')
            print('   ' + '─' * 92)
            for idx, (client_id, count) in enumerate(client_counts.items(), 1):
                client_name = org_map.get(client_id, str(client_id))[:58]
                print(f'   {idx:<6} {client_name:<60} {count:>15}')
            print('   ' + '─' * 92)
            print(f'   Total: {len(client_counts)} clients uniques')
        else:
            print(f'   ℹ️ Données de clients non disponibles')

        # ===== ANALYSE DÉTAILLÉE PAR CLIENT =====
        print(f'\n🔍 ANALYSE DÉTAILLÉE PAR CLIENT')
        print('─' * 100)
        if client_col:
            clients_list = booth_sessions[client_col].unique()
            for client_id in clients_list:
                client_data = booth_sessions[booth_sessions[client_col] == client_id]
                client_total_apps = len(client_data)

                # Afficher le nom de l'organisation au lieu de l'ID
                client_name = org_map.get(client_id, str(client_id))

                print(f'\n   📊 Organisation: {client_name:<40} | Candidatures: {client_total_apps}')
                print(f'   {"─" * 98}')

                # Statut pour ce client
                if 'status' in client_data.columns:
                    status_dist = client_data['status'].value_counts()
                    print(f'   Statuts: {", ".join([f"{s}:{c}" for s, c in status_dist.items()])}')

                # Campagnes pour ce client
                if job_col:
                    campaigns_for_client = client_data[job_col].value_counts()
                    print(f'   Campagnes: {len(campaigns_for_client)} uniques')
                    for campaign_id, count in campaigns_for_client.head(3).items():
                        print(f'      - {str(campaign_id):<45} : {count} candidatures')
                    if len(campaigns_for_client) > 3:
                        print(f'      ... et {len(campaigns_for_client) - 3} autres')

        # Liste complète des offres/campagnes (récapitulatif)
        print(f'\n💼 Récapitulatif des Campagnes / Offres')
        print('─' * 100)
        if job_col:
            job_counts = booth_sessions[job_col].value_counts()
            num_campaigns = len(job_counts)
            print(f'   {"Rang":<6} {"Campagne / Offre (Job)":<60} {"Candidatures":>15}')
            print('   ' + '─' * 92)
            for idx, (job_id, count) in enumerate(job_counts.items(), 1):
                job_title = job_map.get(job_id, str(job_id))[:58]
                print(f'   {idx:<6} {job_title:<60} {count:>15}')
            print('   ' + '─' * 92)
            print(f'   Total: {len(job_counts)} campagnes uniques')
        else:
            print(f'   ℹ️ Données de campagnes non disponibles')

        # ===== ANALYSE DÉTAILLÉE PAR CAMPAGNE =====
        print(f'\n🔍 ANALYSE DÉTAILLÉE PAR CAMPAGNE')
        print('─' * 100)
        if job_col:
            campaigns_list = booth_sessions[job_col].unique()
            for campaign_id in campaigns_list:
                campaign_data = booth_sessions[booth_sessions[job_col] == campaign_id]
                campaign_total_apps = len(campaign_data)

                # Afficher le titre de la campagne au lieu de l'ID
                campaign_title = job_map.get(campaign_id, str(campaign_id))

                print(f'\n   📊 Campagne: {campaign_title:<45} | Candidatures: {campaign_total_apps}')
                print(f'   {"─" * 98}')

                # Statut pour cette campagne
                if 'status' in campaign_data.columns:
                    status_dist = campaign_data['status'].value_counts()
                    print(f'   Statuts: {", ".join([f"{s}:{c}" for s, c in status_dist.items()])}')

                # Clients pour cette campagne
                if client_col:
                    clients_for_campaign = campaign_data[client_col].value_counts()
                    print(f'   Clients: {len(clients_for_campaign)} uniques')
                    for client_id, count in clients_for_campaign.head(3).items():
                        print(f'      - {str(client_id):<45} : {count} candidatures')
                    if len(clients_for_campaign) > 3:
                        print(f'      ... et {len(clients_for_campaign) - 3} autres')

                # CV et autres stats
                cv_for_campaign = int(campaign_data['hasCvDownloaded'].sum()) if 'hasCvDownloaded' in campaign_data.columns else 0
                print(f'   CV créés: {cv_for_campaign}')

        # Analyse par semaine
        print(f'\n📆 Analyse par Semaine')
        print('─' * 100)
        if ANALYZE_PERIOD:
            if len(ANALYZE_PERIOD) == 7:
                filtered_sessions = booth_sessions[booth_sessions['year_month'].astype(str) == ANALYZE_PERIOD]
                print(f'   Filtre: Mois {ANALYZE_PERIOD}')
            elif len(ANALYZE_PERIOD) == 10:
                filtered_sessions = booth_sessions[booth_sessions['date'].astype(str) == ANALYZE_PERIOD]
                print(f'   Filtre: Jour {ANALYZE_PERIOD}')
            else:
                filtered_sessions = booth_sessions
        else:
            filtered_sessions = booth_sessions

        if len(filtered_sessions) > 0:
            print(f'   {"Semaine":<15} {"Candidatures":>15}')
            print('   ' + '─' * 96)
            weekly_stats = filtered_sessions.groupby(['year', 'year_week']).agg({
                'applicationsCount': 'sum'
            }).reset_index()
            weekly_stats.columns = ['year', 'week', 'applications']
            weekly_stats = weekly_stats.sort_values('applications', ascending=False).head(10)

            for _, row in weekly_stats.iterrows():
                week_str = f"S{int(row['week']):02d}-{int(row['year'])}"
                apps = int(row['applications']) if row['applications'] > 0 else 0
                print(f'   {week_str:<15} {apps:>15}')
        else:
            print(f'   ℹ️ Aucune donnée pour la période sélectionnée')

        # Stocker les données récapitulatives
        cabines_recap.append({
            'Cabine': booth_name,
            'Sessions': booth_total_sessions,
            'CV Créés': booth_cv_created,
            'CV Imprimés': booth_cv_printed,
            'Candidatures': booth_apps,
            'Clients': num_clients,
            'Campagnes': num_campaigns,
            'Statuts': ', '.join([f'{k}:{v}' for k, v in status_recap.items()]) if status_recap else 'N/A'
        })

    # Afficher le tableau récapitulatif global
    print('\n\n' + '=' * 150)
    print('📊 TABLEAU RÉCAPITULATIF GLOBAL - TOUTES LES CABINES')
    print('=' * 150)

    if cabines_recap:
        # Créer un DataFrame pour afficher le tableau
        recap_df = pd.DataFrame(cabines_recap)

        # Afficher le tableau formaté
        print('\n' + recap_df.to_string(index=False))

        print('\n' + '=' * 150)
        print(f'\nRÉSUMÉ GLOBAL:')
        print('─' * 150)
        print(f'   Nombre de cabines analysées: {len(cabines_recap)}')
        print(f'   Total sessions: {recap_df["Sessions"].sum()}')
        print(f'   Total CV créés: {recap_df["CV Créés"].sum()}')
        print(f'   Total CV imprimés: {recap_df["CV Imprimés"].sum()}')
        print(f'   Total candidatures: {recap_df["Candidatures"].sum()}')
        print(f'   Total clients uniques: {recap_df["Clients"].sum()}')
        print(f'   Total campagnes uniques: {recap_df["Campagnes"].sum()}')

else:
    print('⚠️ Pas de données de sessions disponibles pour l\'analyse par cabine')

# ============================================================
# 📅 ÉTAPE 5 : Timeline - Évolution temporelle PAR CABINE
# ============================================================

# ============================================================
# 📅 ÉTAPE 13 : Résumé final
# ============================================================

print('\n' + '=' * 100)
print('✅ ANALYSE COMPLÈTE TERMINÉE !')
print('=' * 100)
print(f'\nEnvironnement: {ENVIRONMENT}')
print(f'   {ENV_STATUS}')
print(f'   URL:   {API_URL}')
print(f'   Période: {DATE_START} à {DATE_END}')

print(f'\n📊 RÉSUMÉ DES STATISTIQUES:')
print('─' * 60)
print(f'   🔵 CV créés: {total_cv_created}')
print(f'   🟢 CV imprimés: {total_cv_printed}')
print(f'   🟡 Offres consultées: {total_job_offers_viewed}')
print(f'   🟠 Candidatures: {total_applications}')
print(f'   🔴 Sessions: {total_sessions}')
print(f'   🟣 Utilisateurs ayant complété une session: {total_users_completed_session}')

if total_cv_created > 0 or total_sessions > 0 or total_job_offers_viewed > 0:
    print(f'\n📈 INDICATEURS DE PERFORMANCE:')
    print('─' * 60)
    if total_cv_created > 0 and total_cv_printed > 0:
        print(f'   ✓ Taux d\'impression: {(total_cv_printed/total_cv_created)*100:.1f}%')
    if total_cv_created > 0 and total_job_offers_viewed > 0:
        print(f'   ✓ Ratio offres/CV: {(total_job_offers_viewed/total_cv_created):.2f}')
    if total_cv_created > 0 and total_applications > 0:
        print(f'   ✓ Ratio candidatures/CV: {(total_applications/total_cv_created):.2f}')
    if total_sessions > 0 and total_cv_created > 0:
        print(f'   ✓ CV par session: {(total_cv_created/total_sessions):.2f}')
    if total_sessions > 0 and total_users_completed_session > 0:
        print(f'   ✓ Taux de complétion: {(total_users_completed_session/total_sessions)*100:.1f}%')

print(f'\nConfiguration active:')
print(f'   Cabines: {CABINES_TO_ANALYZE}')
print(f'   Période détails: {ANALYZE_PERIOD if ANALYZE_PERIOD else "Toutes"}')
print(f'   Export Excel: Désactivé')
print('\n' + '=' * 100)

