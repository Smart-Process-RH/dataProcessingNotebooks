# 📊 CABINE CIBLI - Script Unique v3.0

## 🎯 Vue d'ensemble

**cabine_cibli.py** est le script unique qui fait TOUT :

1. ✅ Récupère les données depuis l'API
2. ✅ Filtre pour "cabine cibli job"
3. ✅ Génère les statistiques
4. ✅ Exporte en Excel

---

## 🚀 Utilisation

```bash
python3 ats_cibli.py
```

**Résultat :**
- Fichiers CSV mis à jour
- Statistiques générées
- Rapport Excel créé

---

## 📋 Paramètres Modifiables

Dans le script (lignes 30-35) :

```python
SOURCE_FILTER = "cabine cibli job"  # Source à analyser
DATE_START = "2025-09-01"           # Date de début
DATE_END = "2026-01-14"             # Date de fin
TOP_N_CLIENTS = 15                  # Nombre de top clients
TOP_N_CAMPAIGNS = 15                # Nombre de top campagnes
```

---

## 📁 Fichiers Générés

### Données brutes
- `stats/applications/raw_applications.csv` - Toutes les candidatures
- `stats/campaigns/raw_campaigns.csv` - Toutes les campagnes

### Données filtrées
- `stats/applications/cabine_cibli_job_applications.csv` - Candidatures cabine cibli job

### Statistiques
- `stats/cabin_stats_total_20260114.csv` - Stats globales
- `stats/cabin_stats_december_20260114.csv` - Stats décembre 2025
- `stats/cabin_stats_january_20260114.csv` - Stats janvier 2026

### Rapports
- `exports/cabine_cibli_analytics_YYYYMMDD_HHMMSS.xlsx` - Rapport Excel complet

### Backups
- `backups/applications_backup_YYYYMMDD_HHMMSS.csv` - Backup automatique

---

## 📊 Contenu du Rapport Excel

### Feuille 1: Résumé
- Source (cabine cibli job)
- Période (dates)
- CVs (nombre total)
- Candidatures (nombre total)
- Clients (nombre total)

### Feuille 2: Top Clients
- Classement des clients
- Nombre de candidatures
- Pourcentage

### Feuille 3: Top Campagnes
- Classement des campagnes
- Nombre de candidatures
- Pourcentage

### Feuille 4: Statuts
- Distribution par statut
- Nombre et pourcentage

---

## ✅ Processus Complet

```
1. RÉCUPÉRATION API
   ↓
2. SAUVEGARDE RAW
   ↓
3. FILTRAGE (source + dates)
   ↓
4. EXTRACTION IDs
   ↓
5. STATISTIQUES GLOBALES
   ↓
6. STATISTIQUES PAR PÉRIODE
   ↓
7. TOP CLIENTS
   ↓
8. TOP CAMPAGNES
   ↓
9. RÉPARTITION STATUTS
   ↓
10. EXPORT EXCEL
```

---

## 🎓 Exemple de Résultat

```
📊 ANALYSE CANDIDATURES CABINE CIBLI

Source:           cabine cibli job
Période:          2025-09-01 à 2026-01-14

CVs:              987
Candidatures:     1131
Clients:          129

✅ Fichiers générés:
   - raw_applications.csv
   - cabine_cibli_job_applications.csv
   - raw_campaigns.csv
   - cabin_stats_total_20260114.csv
   - cabine_cibli_analytics_20260114_150150.xlsx
```

---

## ⚙️ Configuration API

Le script utilise automatiquement :
- **API_URL:** https://api.smart-process-rh.com/v1
- **API_KEY:** Définie dans le script

---

## 📅 Date

- **Créé:** 14 janvier 2026
- **Dernière mise à jour:** 14 janvier 2026
- **Version:** 3.0

---

## ✅ Status

**SCRIPT UNIQUE - FUSIONNÉ ET OPTIMISÉ** ✅

Tous les processus sont centralisés dans un seul fichier.

