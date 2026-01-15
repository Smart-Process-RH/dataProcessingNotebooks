# 📊 Script Analytics Cabine - Documentation Complète

## 🎯 Vue d'ensemble

Le script `stats_cabines.py` récupère et analyse les données de la Cabine CIBLI depuis les APIs Staging et Production. Il génère un rapport détaillé en fichier Excel avec 5 feuilles d'analyse.

**Créé par:** Vlad Kunitsyn  
**Repository:** `Zaidoudou/dataProcessingNotebooks`  
**Branch:** `statysics-by-vlad`  
**Version:** 1.0  
**Date:** 2026-01-15

---

## 📋 Table des matières

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Utilisation](#utilisation)
4. [Fonctionnalités](#fonctionnalités)
5. [Endpoints API](#endpoints-api)
6. [Résultats Générés](#résultats-générés)
7. [Exemples d'Utilisation](#exemples-dutilisation)
8. [Dépannage](#dépannage)

---

## 🚀 Installation

### Prérequis

- Python 3.7+
- Les dépendances listées dans `requirements.txt`

### Étapes

```bash
# 1. Cloner ou accéder au repository
cd /home/vladkunitsyn/PycharmProjects/dataProcessingNotebooks

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Vérifier l'installation
python3 -m py_compile stats/stats_cabines.py
```

### Dépendances Requises

```
pandas       # Manipulation de données
requests     # Requêtes HTTP/API
openpyxl     # Génération fichiers Excel
```

---

## ⚙️ Configuration

Le script utilise des variables configurables au début du fichier (ligne 21-32). **Modifiez ces variables selon vos besoins :**

### Variables Principales

```python
# 📍 Ligne 23-24 : Environnement
ENVIRONMENT = 'STAGING'  # Choisir: 'STAGING' ou 'PRODUCTION'

# 📍 Ligne 27-28 : Dates
DATE_START = '2025-09-01'  # Format: YYYY-MM-DD
DATE_END = '2026-01-14'    # Format: YYYY-MM-DD

# 📍 Ligne 31-32 : Affichage
SHOW_DETAILS = True              # True = détails, False = résumé
COMPARE_ENVIRONMENTS = False     # True = comparer STAGING vs PROD

# 📍 Ligne 35 : Export
EXPORT_TO_EXCEL = True           # True = générer Excel
```

### ⚠️ Configuration API (NE PAS MODIFIER)

Les URLs et clés API sont préconfigurées (ligne 42-47) :

| Environnement | URL | Clé API | Statut |
|---|---|---|---|
| **STAGING** | `https://cibli-api.agency.lonestone.io/api` | `PGZ4qtc5jtf@rph3twf` | ✅ Actif |
| **PRODUCTION** | `https://app-api.ciblijob.fr/api` | `txf.hpc9aut9rbd2KWA` | 🔜 À venir |

---

## 🎬 Utilisation

### Commande Basique

```bash
# Exécuter le script avec la configuration par défaut (STAGING)
python3 stats/stats_cabines.py
```

### Modifier la Configuration

#### Option 1 : Éditer le fichier directement

```bash
# Ouvrir dans un éditeur
nano stats/stats_cabines.py
# Modifier les variables à la ligne 23-35
# Sauvegarder et quitter
```

#### Option 2 : Variables d'environnement (Optionnel)

```python
# Ajouter avant l'import dans le script
import os
ENVIRONMENT = os.getenv('CABINE_ENV', 'STAGING')
DATE_START = os.getenv('CABINE_DATE_START', '2025-09-01')
DATE_END = os.getenv('CABINE_DATE_END', '2026-01-14')
```

### Exemples de Configuration

#### 📊 Analyse STAGING (par défaut)

```python
ENVIRONMENT = 'STAGING'
DATE_START = '2025-09-01'
DATE_END = '2026-01-14'
EXPORT_TO_EXCEL = True
```

#### 🌍 Analyse PRODUCTION (quand disponible)

```python
ENVIRONMENT = 'PRODUCTION'
DATE_START = '2025-09-01'
DATE_END = '2026-01-14'
EXPORT_TO_EXCEL = True
```

#### 📈 Comparer STAGING vs PRODUCTION

```python
ENVIRONMENT = 'STAGING'
COMPARE_ENVIRONMENTS = True
EXPORT_TO_EXCEL = True
```

---

## 🔍 Fonctionnalités

Le script exécute **8 étapes principales** :

### ✅ ÉTAPE 1 : Récupération des données API (ligne 71-246)

**Récupère 6 sources de données :**

1. **Booths (Cabines)** → `/booths/all`
2. **Events (Événements)** → `/analytics/events`
3. **KPIs** → `/analytics/kpis`
4. **Timeline** → `/analytics/timeline`
5. **Sessions** → `/analytics/sessions`
6. **Interviews** → `/interviews/analytics/per-day`

**Statut :** ✅ Affiche le nombre d'éléments récupérés

### ✅ ÉTAPE 2 : Filtrage et enrichissement (ligne 249-276)

- Convertit les dates au format datetime
- Crée un mapping : ID cabine → Nom cabine
- Valide les données

**Statut :** ✅ Affiche le nombre de cabines mappées

### ✅ ÉTAPE 3 : Statistiques principales (ligne 279-316)

**Calcule 3 métriques clés :**

- 📌 **CV créés** (event_type = `CV_CREATED`)
- 📌 **CV imprimés** (event_type = `CV_PRINTED`)
- 📌 **Offres consultées** (event_type = `JOB_OFFER_VIEWED`)

**Statistiques supplémentaires :**
- Taux d'impression (%)
- Ratio offres/CV
- Événements par session

### ✅ ÉTAPE 4 : Analyse par cabine (ligne 319-337)

- Classement des 10 meilleures cabines par nombre d'événements
- Affiche : `Cabine → Nombre d'événements`

### ✅ ÉTAPE 5 : Timeline quotidienne (ligne 340-359)

- Affiche l'évolution des 10 derniers jours
- Métriques : CV créés, CV imprimés

### ✅ ÉTAPE 6 : Comparaison STAGING vs PRODUCTION (ligne 362-377)

- **Actuellement :** ℹ️ Message informatif (PROD pas encore disponible)
- **Futur :** Comparaison automatique quand PROD sera déployé

### ✅ ÉTAPE 7 : Export Excel (ligne 380-410)

**Génère un fichier Excel avec 5 feuilles :**

| # | Feuille | Contenu |
|---|---------|---------|
| 1 | 📋 Résumé | Métriques principales |
| 2 | 📊 Événements | Tous les événements |
| 3 | 📅 Timeline | Évolution quotidienne |
| 4 | 🏢 Par Cabine | Statistiques par cabine |
| 5 | 📈 KPIs | Indicateurs clés |

**Nom du fichier :**
```
exports/cabine_analytics_{ENV}_{DATE_START}_{DATE_END}_{TIMESTAMP}.xlsx
```

Exemple : `cabine_analytics_STAGING_2025-09-01_2026-01-14_20260115_121652.xlsx`

### ✅ ÉTAPE 8 : Message de fin (ligne 413-423)

- Résumé des résultats
- Affichage de l'environnement utilisé
- Confirmation de la réussite

---

## 🌐 Endpoints API

Tous les endpoints utilisent le header d'authentification :

```python
headers = {'x-secret-key': API_KEY}
```

### 1. GET `/booths/all`

**Description :** Récupère toutes les cabines  
**Paramètres :** Aucun  
**Réponse :** Liste des cabines avec `id` et `name`

```json
[
  {"id": 1, "name": "Cabine Paris", ...},
  {"id": 2, "name": "Cabine Lyon", ...}
]
```

### 2. GET `/analytics/events`

**Description :** Récupère tous les événements  
**Paramètres :**
- `from` : Date de début (YYYY-MM-DD)
- `to` : Date de fin (YYYY-MM-DD)

**Types d'événements :**
- `CV_CREATED` - CV créé
- `CV_PRINTED` - CV imprimé
- `JOB_OFFER_VIEWED` - Offre consultée

### 3. GET `/analytics/kpis`

**Description :** Récupère les indicateurs clés  
**Paramètres :**
- `from` : Date de début
- `to` : Date de fin

### 4. GET `/analytics/timeline`

**Description :** Récupère l'évolution quotidienne  
**Paramètres :**
- `from` : Date de début
- `to` : Date de fin

**Champs :** `date`, `cv_created`, `cv_printed`, etc.

### 5. GET `/analytics/sessions`

**Description :** Récupère les sessions utilisateur  
**Paramètres :**
- `from` : Date de début
- `to` : Date de fin

### 6. GET `/interviews/analytics/per-day`

**Description :** Récupère les interviews par jour  
**Paramètres :**
- `from` : Date de début
- `to` : Date de fin

---

## 📊 Résultats Générés

### Fichier Excel

**Localisation :** `exports/cabine_analytics_STAGING_*.xlsx`

#### Feuille 1 : 📋 Résumé

| Métrique | Valeur |
|----------|--------|
| Environnement | STAGING |
| Période | 2025-09-01 à 2026-01-14 |
| CV créés | 0 |
| CV imprimés | 0 |
| Offres consultées | 0 |
| Sessions | 100 |
| Événements | 100 |

#### Feuille 2 : 📊 Événements

Tableau complet de tous les événements avec colonnes :
- `id`, `booth_id`, `event_type`, `user_id`, `created_at`, etc.

#### Feuille 3 : 📅 Timeline

Évolution quotidienne :
- `date`, `cv_created`, `cv_printed`, `events`, etc.

#### Feuille 4 : 🏢 Par Cabine

Classement des cabines :
- `Cabine`, `Total` (nombre d'événements)

#### Feuille 5 : 📈 KPIs

Indicateurs clés de performance avec toutes les métriques

---

## 💻 Exemples d'Utilisation

### Exemple 1 : Rapport Standard (STAGING)

```bash
cd /home/vladkunitsyn/PycharmProjects/dataProcessingNotebooks
python3 stats/stats_cabines.py
```

**Résultat :**
- Affichage console avec progress
- Fichier Excel généré : `exports/cabine_analytics_STAGING_2025-09-01_2026-01-14_*.xlsx`

### Exemple 2 : Analyser une Période Spécifique

```python
# Modifier dans le script (ligne 27-28)
DATE_START = '2025-11-01'
DATE_END = '2025-11-30'
```

Puis exécuter :
```bash
python3 stats/stats_cabines.py
```

### Exemple 3 : Production (Quand disponible)

```python
# Modifier dans le script (ligne 23)
ENVIRONMENT = 'PRODUCTION'
```

Puis exécuter :
```bash
python3 stats/stats_cabines.py
```

### Exemple 4 : Mode Comparaison

```python
# Modifier dans le script (ligne 32)
COMPARE_ENVIRONMENTS = True
```

Puis exécuter :
```bash
python3 stats/stats_cabines.py
```

---

## 🔧 Dépannage

### ❌ Erreur : "No module named 'pandas'"

**Solution :**
```bash
pip install --break-system-packages pandas openpyxl requests
```

### ❌ Erreur : "Connexion refusée" ou "Timeout"

**Causes :**
- API indisponible
- URL incorrecte
- Problème réseau

**Solution :**
```bash
# Vérifier la connexion
curl -H "x-secret-key: PGZ4qtc5jtf@rph3twf" \
  https://cibli-api.agency.lonestone.io/api/booths/all
```

### ❌ Erreur : "Code 401 ou 403"

**Cause :** Clé API incorrecte ou expirée

**Solution :** Vérifier `API_KEY` à la ligne 42-46

### ❌ Fichier Excel non généré

**Cause :** Dossier `exports/` inexistant

**Solution :** Le script crée automatiquement le dossier. Si le problème persiste :
```bash
mkdir -p /home/vladkunitsyn/PycharmProjects/dataProcessingNotebooks/exports
```

### ⚠️ Accents mal affichés dans le terminal

**Cause :** Encodage UTF-8 non supporté

**Solution :** Le script fonctionne correctement. L'affichage console est juste cosmétique. Les fichiers Excel auront les accents corrects.

---

## 📈 Performance et Optimisations

- **Taille des données :** Le script gère jusqu'à 1000+ événements
- **Temps d'exécution :** ~5-10 secondes (selon la connexion)
- **Mémoire :** ~50-100 MB en pic d'utilisation

---

## 🔐 Sécurité

⚠️ **ATTENTION :** Les clés API sont stockées en dur. Pour un environnement de production :

```python
import os
API_STAGING_KEY = os.getenv('CIBLI_STAGING_KEY', 'PGZ4qtc5jtf@rph3twf')
API_PROD_KEY = os.getenv('CIBLI_PROD_KEY', 'txf.hpc9aut9rbd2KWA')
```

---

## 📞 Support

**Repository :** [Zaidoudou/dataProcessingNotebooks](https://github.com/Zaidoudou/dataProcessingNotebooks)  
**Branch :** `statysics-by-vlad`  
**Créateur :** Vlad Kunitsyn

---

**Dernière mise à jour :** 2026-01-15

