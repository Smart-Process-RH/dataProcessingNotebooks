#!/usr/bin/env python3
"""
Script de test des appels API
Testé avec la configuration actuelle
"""

import requests
import json
from datetime import datetime

# Configuration
ENVIRONMENT = 'PRODUCTION'
DATE_START = '2025-09-01'
DATE_END = '2026-01-19'

# URLs et clés API
API_STAGING_URL = 'https://cibli-api.agency.lonestone.io/api'
API_STAGING_KEY = 'PGZ4qtc5jtf@rph3twf'

API_PROD_URL = 'https://app-api.ciblijob.fr/api'
API_PROD_KEY = 'txf.hpc9aut9rbd2KWA'

# Sélectionner selon l'environnement
if ENVIRONMENT == 'STAGING':
    API_URL = API_STAGING_URL
    API_KEY = API_STAGING_KEY
    ENV_STATUS = '🧪 STAGING'
else:
    API_URL = API_PROD_URL
    API_KEY = API_PROD_KEY
    ENV_STATUS = '🚀 PRODUCTION'

HEADERS = {
    'x-secret-key': API_KEY
}

print(f"\n{'='*60}")
print(f"TEST DES APPELS API")
print(f"{'='*60}")
print(f"Environnement: {ENV_STATUS}")
print(f"URL API: {API_URL}")
print(f"Période: {DATE_START} à {DATE_END}")
print(f"{'='*60}\n")

# Endpoints à tester
endpoints = [
    {
        'name': '1️⃣ Cabines',
        'url': f'{API_URL}/booths/all',
        'params': None
    },
    {
        'name': '2️⃣ Événements',
        'url': f'{API_URL}/analytics/events',
        'params': {'from': DATE_START, 'to': DATE_END}
    },
    {
        'name': '3️⃣ KPIs',
        'url': f'{API_URL}/analytics/kpis',
        'params': {'from': DATE_START, 'to': DATE_END}
    },
    {
        'name': '4️⃣ Timeline',
        'url': f'{API_URL}/analytics/timeline',
        'params': {'from': DATE_START, 'to': DATE_END}
    },
    {
        'name': '5️⃣ Sessions',
        'url': f'{API_URL}/analytics/sessions',
        'params': {'from': DATE_START, 'to': DATE_END}
    },
    {
        'name': '6️⃣ Interviews par jour',
        'url': f'{API_URL}/interviews/analytics/per-day',
        'params': {'from': DATE_START, 'to': DATE_END}
    }
]

# Tester chaque endpoint
for endpoint in endpoints:
    print(f"\n{endpoint['name']}")
    print(f"{'─'*60}")
    print(f"📡 URL: {endpoint['url']}")

    if endpoint['params']:
        print(f"📅 Paramètres: {endpoint['params']}")

    try:
        response = requests.get(
            endpoint['url'],
            headers=HEADERS,
            params=endpoint['params'],
            timeout=10
        )

        print(f"✓ Code: {response.status_code}")
        print(f"✓ Taille réponse: {len(response.text)} bytes")

        # Afficher les premières 500 caractères
        if response.text:
            preview = response.text[:500]
            print(f"✓ Aperçu réponse:\n{preview}")
            if len(response.text) > 500:
                print(f"   ... ({len(response.text) - 500} bytes additionnels)")
        else:
            print("✓ Réponse vide")

        # Essayer de parser le JSON
        try:
            data = response.json()
            print(f"✓ JSON valide (type: {type(data).__name__})")
            if isinstance(data, dict):
                print(f"✓ Clés: {list(data.keys())}")
            elif isinstance(data, list):
                print(f"✓ Nombre d'éléments: {len(data)}")
        except:
            print("⚠️ Réponse non-JSON")

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

print(f"\n{'='*60}")
print("✅ Test terminé")
print(f"{'='*60}\n")

