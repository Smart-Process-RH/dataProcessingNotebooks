# 📊 Cabine Cibli - Analyse des Candidatures

## 🎯 Description

Ce projet génère des statistiques détaillées sur les candidatures de la source **"Cabine Cibli Job"**, incluant :
- Nombre total de CVs
- Nombre total de candidatures
- Statistiques par client/campagne
- Exports en Excel et CSV

**Données à jour : 14/01/2026**

---

## 📁 Structure du Projet

```
dataProcessingNotebooks/
├── generate_cabin_stats.py          # 🔧 Script principal de génération des stats
├── requirements.txt                 # 📦 Dépendances Python
├── README.md                        # 📖 Ce fichier
│
├── stats/                           # 📊 Données et résultats
│   ├── cabin_stats_total_20260114.csv          # Stats TOTAL
│   ├── cabin_stats_december_20260114.csv       # Stats Décembre 2025
│   ├── cabin_stats_january_20260114.csv        # Stats Janvier 2026
│   ├── client_stats.csv                        # Données clients
│   ├── client_stats.xlsx                       # Données clients (Excel)
│   ├── cabine_cibli_job_analytics.ipynb        # Notebook d'analyse
│   │
│   ├── applications/
│   │   ├── cabine_cibli_job_applications.csv   # Candidatures Cabine Cibli
│   │   └── raw_applications.csv                # Données brutes complètes
│   │
│   └── campaigns/
│       └── raw_campaigns.csv                   # Données des campagnes
│
└── exports/                         # 📑 Rapports générés
    └── cabin_stats_report_20260114.xlsx        # Rapport Excel consolidé
```

---

## 🚀 Installation

### 1. Créer un environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

---

## 📊 Utilisation

### Générer les statistiques à jour

```bash
python3 generate_cabin_stats.py
```

Ce script :
1. ✅ Récupère les données depuis l'API
2. ✅ Filtre pour "cabine cibli job"
3. ✅ Calcule les statistiques
4. ✅ Génère les fichiers CSV et Excel

### Résultats générés

**Fichiers CSV :**
- `stats/cabin_stats_total_20260114.csv` - Toutes les candidatures
- `stats/cabin_stats_december_20260114.csv` - Candidatures décembre
- `stats/cabin_stats_january_20260114.csv` - Candidatures janvier

**Fichier Excel :**
- `exports/cabin_stats_report_20260114.xlsx` - Rapport complet avec 4 feuilles

---

## 📈 Statistiques Actuelles (14/01/2026)

### 🔹 TOTAL
| Métrique | Valeur |
|----------|--------|
| CVs | 983 |
| Candidatures | 1127 |
| Clients | 128 |

**Top 5 Clients :**
1. Campaign 193 : 71 candidatures
2. Campaign 200 : 66 candidatures
3. Campaign 191 : 47 candidatures
4. Campaign 189 : 42 candidatures
5. Campaign 175 : 41 candidatures

### 🔹 DÉCEMBRE 2025
| Métrique | Valeur |
|----------|--------|
| CVs | 143 |
| Candidatures | 143 |
| Clients | 60 |

**Top 5 Clients :**
1. Campaign 228 : 16 candidatures
2. Campaign 193 : 9 candidatures
3. Campaign 267 : 6 candidatures
4. Campaign 261 : 6 candidatures
5. Campaign 191 : 5 candidatures

### 🔹 JANVIER 2026 (1-14)
| Métrique | Valeur |
|----------|--------|
| CVs | 27 |
| Candidatures | 27 |
| Clients | 20 |

**Top 5 Clients :**
1. Campaign 200 : 3 candidatures
2. Campaign 258 : 2 candidatures
3. Campaign 213 : 2 candidatures
4. Campaign 261 : 2 candidatures
5. Campaign 331 : 2 candidatures

---

## 🔧 Configuration API

Le script utilise l'API Smart Process RH :
- **URL** : https://api.smart-process-rh.com/v1
- **Endpoint** : `/applications/all`
- **Headers** : `x-api-key` (clé API configurée dans le script)

---

## 📝 Fichiers Importants

| Fichier | Utilité |
|---------|---------|
| `generate_cabin_stats.py` | Script principal de génération |
| `requirements.txt` | Dépendances Python |
| `stats/cabin_stats_*.csv` | Résultats finaux en CSV |
| `exports/cabin_stats_report_*.xlsx` | Rapport Excel consolidé |

---

## 🧹 Projet Nettoyé

✅ **Supprimés :**
- Scripts de test anciens
- Fichiers de sauvegarde/restore
- Données dupliquées
- Notebooks expérimentaux

✅ **Conservés :**
- Script de génération optimisé
- Données consolidées à jour
- Notebooks d'analyse
- Documentation complète

---

## 📞 Support

Pour toute question ou mise à jour des données, exécutez simplement :
```bash
python3 generate_cabin_stats.py
```

---

**Dernière mise à jour : 14 janvier 2026**

