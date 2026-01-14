# 📊 Analyse des Candidatures - Cabine Cibli Job

Analyse détaillée des candidatures 'cabine cibli job' avec génération de rapports statistiques complets et exports Excel.

**Période d'analyse:** Septembre 2025 - Janvier 2026

---

## 📦 Installation

### Prérequis

- Python 3.7+
- pip ou conda

### Dépendances

```bash
pip install -r requirements.txt
```

Ou installez manuellement:

```bash
pip install requests pandas openpyxl numpy
```

### Environnement virtuel (recommandé)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 🚀 Utilisation

### Option 1 : Script Python (Standalone)

```bash
cd /home/vladkunitsyn/PycharmProjects/dataProcessingNotebooks
source venv/bin/activate
python3 cabine_cibli_analytics.py
```

**Avantages:**
- ✅ Exécution rapide et directe
- ✅ Pas de dépendance Jupyter
- ✅ Peut être programmé en cron job

**Résultat:**
- Rapport complet affichage en console
- Fichier Excel généré dans `exports/`

### Option 2 : Jupyter Notebook

```bash
cd /home/vladkunitsyn/PycharmProjects/dataProcessingNotebooks
source venv/bin/activate
jupyter notebook stats/cabine_cibli_job_analytics.ipynb
```

**Avantages:**
- ✅ Interface interactive
- ✅ Modification facile des paramètres
- ✅ Visualisation étape par étape

---

## ⚙️ Configuration

### Modifier les paramètres

Ouvrez le script ou le notebook et modifiez ces variables:

#### Script (`cabine_cibli_analytics.py`)

```python
SOURCE_FILTER = "cabine cibli job"  # Source à analyser
DATE_START = "2025-09-01"           # Date de début (YYYY-MM-DD)
DATE_END = "2026-01-14"             # Date de fin (YYYY-MM-DD)
TOP_N_CLIENTS = 10                  # Nombre de top clients
TOP_N_CAMPAIGNS = 10                # Nombre de top campagnes
```

#### Notebook (cellule de configuration)

Modifiez les mêmes variables dans la section "⚙️ Étape 2 : Configuration"

### Exemples de configuration

**Analyser une source différente:**
```python
SOURCE_FILTER = "hellowork"  # Au lieu de "cabine cibli job"
```

**Analyser une période différente:**
```python
DATE_START = "2025-01-01"
DATE_END = "2025-12-31"
```

**Afficher plus de clients/campagnes:**
```python
TOP_N_CLIENTS = 20
TOP_N_CAMPAIGNS = 20
```

---

## 📊 Résultats et Rapports

### Console Output (Exemple)

```
============================================================
📊 RÉSUMÉ DES STATISTIQUES DE LA CABINE CIBLI
============================================================

✓ Nombre total de CV faits: 957
✓ Nombre total de candidatures: 957
✓ Nombre de clients avec candidatures: 98

📋 TOP 10 CLIENTS (candidatures):
    1. E.LECLERC ATLANTIS: 554 candidatures
    2. Smart Profil: 65 candidatures
    3. RAS Intérim - Nantes: 35 candidatures
    ...

📊 RÉPARTITION PAR STATUT:
  - new: 643 (67.2%)
  - denied: 265 (27.7%)
  - on_hold: 46 (4.8%)
  ...
```

### Fichier Excel Généré

**Localisation:** `exports/cabine_cibli_analytics_cabine_cibli_job_YYYYMMDD_HHMMSS.xlsx`

**Feuilles incluses:**

1. **📋 Résumé** - Métriques clés
   - Nombre total de CV
   - Nombre total de candidatures
   - Nombre unique de candidats
   - Nombre de campagnes
   - Période analysée

2. **🏢 Top Clients** - Classement des clients
   - Rang
   - Nom du client
   - Nombre de candidatures

3. **🎯 Top Campagnes** - Top campagnes
   - Rang
   - ID de campagne
   - Nombre de candidatures
   - Pourcentage du total

4. **📊 Statuts** - Distribution des statuts
   - Statut
   - Nombre
   - Pourcentage

5. **🌐 Sources** - Distribution des sources
   - Source
   - Nombre
   - Pourcentage

6. **📊 Détails** - Liste complète des candidatures
   - ID
   - Statut
   - Source
   - Campagne
   - Candidat
   - Date de candidature

---

## 📋 Étapes du traitement

### 1️⃣ Imports des bibliothèques
Charge tous les modules Python nécessaires (requests, pandas, openpyxl, etc.)

### 2️⃣ Configuration
Définit les paramètres de filtrage et les chemins d'accès aux fichiers

### 3️⃣ Récupération des données
- Charge les candidatures depuis les fichiers locaux CSV
- Charge les campagnes
- Charge les données clients

Fallback: Récupère via API si les fichiers locaux ne sont pas disponibles

### 4️⃣ Filtrage et enrichissement
- Convertit les dates au format datetime
- Filtre par source (ex: "cabine cibli job")
- Filtre par plage de dates
- Enrichit avec données de campagne

### 5️⃣ Calcul des statistiques
- Nombre total de CV et candidatures
- Nombre de candidats et campagnes uniques
- Distribution par statut et source
- Top clients et top campagnes
- Analyse temporelle par mois

### 6️⃣ Export Excel
Crée un fichier Excel structuré avec 6 feuilles

---

## 🔧 Troubleshooting

### Erreur: "FileNotFoundError: [Errno 2] No such file or directory"

**Cause:** Les fichiers CSV locaux ne sont pas trouvés

**Solution:**
1. Vérifiez que vous êtes dans le bon répertoire:
   ```bash
   pwd  # Doit afficher: /home/vladkunitsyn/PycharmProjects/dataProcessingNotebooks
   ```
2. Vérifiez que les fichiers CSV existent:
   ```bash
   ls -la stats/applications/raw_applications.csv
   ls -la stats/campaigns/raw_campaigns.csv
   ls -la stats/client_stats.csv
   ```
3. Si les fichiers n'existent pas, assurez-vous que l'API est accessible pour le fallback

### Erreur: "ModuleNotFoundError: No module named 'openpyxl'"

**Cause:** Les dépendances ne sont pas installées

**Solution:**
```bash
pip install openpyxl pandas requests numpy
```

### Erreur: "API response 401 Unauthorized"

**Cause:** La clé API est invalide ou expirée

**Solution:**
1. Vérifiez que `API_KEY` est correct dans le script
2. Assurez-vous que vous avez accès à l'API
3. Contactez l'administrateur pour renouveler la clé

### Aucune donnée trouvée après filtrage

**Cause:** La source ou la plage de dates ne contient pas de données

**Solution:**
1. Vérifiez la valeur de `SOURCE_FILTER`
2. Vérifiez les dates `DATE_START` et `DATE_END`
3. Listez les sources disponibles:
   ```python
   df = pd.read_csv('stats/applications/raw_applications.csv')
   print(df['source'].unique())
   ```

---

## 📈 Exemples de rapport

### Exemple 1: Analyser toutes les sources de septembre 2025

Modifiez le script:
```python
SOURCE_FILTER = "hellowork"  # Analyser HelloWork au lieu de Cabine Cibli
DATE_START = "2025-09-01"
DATE_END = "2025-09-30"
```

### Exemple 2: Générer un rapport annuel

```python
DATE_START = "2025-01-01"
DATE_END = "2025-12-31"
TOP_N_CLIENTS = 20
TOP_N_CAMPAIGNS = 15
```

### Exemple 3: Comparer deux périodes

Exécutez deux fois le script avec des dates différentes:
```python
# Première exécution
DATE_START = "2025-01-01"
DATE_END = "2025-06-30"

# Deuxième exécution
DATE_START = "2025-07-01"
DATE_END = "2025-12-31"
```

---

## 📚 Structure des fichiers

```
dataProcessingNotebooks/
├── cabine_cibli_analytics.py          ← Script principal
├── stats/
│   ├── cabine_cibli_job_analytics.ipynb ← Notebook Jupyter
│   ├── applications/
│   │   └── raw_applications.csv        ← Données des candidatures
│   ├── campaigns/
│   │   └── raw_campaigns.csv           ← Données des campagnes
│   └── client_stats.csv                ← Données des clients
├── exports/                            ← Dossier des rapports Excel
│   └── cabine_cibli_analytics_*.xlsx
├── requirements.txt                    ← Dépendances
└── venv/                              ← Environnement virtuel
```

---

## 🔐 Sécurité

⚠️ **Important:** La clé API est stockée dans le script. 

**Recommandations:**
1. Ne jamais commiter la clé API sur GitHub
2. Stocker la clé dans une variable d'environnement:
   ```python
   import os
   API_KEY = os.getenv('SMART_PROCESS_API_KEY')
   ```
3. Utiliser un fichier `.env`:
   ```bash
   pip install python-dotenv
   ```
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   API_KEY = os.getenv('SMART_PROCESS_API_KEY')
   ```

---

## 📞 Support

Pour toute question ou problème:

1. Consultez le tableau de dépannage (section Troubleshooting)
2. Vérifiez les logs dans la console
3. Contactez l'administrateur système

---

## 📝 Changelog

### Version 1.0 (2026-01-14)

- ✅ Implémentation initiale du script d'analyse
- ✅ Création du notebook Jupyter
- ✅ Export Excel multi-feuilles
- ✅ Support API et fichiers locaux
- ✅ Analyse temporelle par mois
- ✅ Documentation complète

---

## 📄 License

Ce projet est confidentiel et réservé à usage interne.

---

**Auteur:** Équipe Analytics  
**Date:** 2026-01-14  
**Version:** 1.0

