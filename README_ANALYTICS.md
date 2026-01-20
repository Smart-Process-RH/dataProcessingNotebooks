# 🎯 ANALYTICS CIBLI - Guide d'exécution

## ✅ Scripts créés et prêts à l'emploi

### 1. **ANALYTICS_FINAL.py** ⭐ (À EXÉCUTER EN PREMIER)

Script complet et optimisé qui affiche tous les KPIs demandés.

**Comment l'exécuter:**
```
1. Ouvre le fichier ANALYTICS_FINAL.py dans WebStorm
2. Clique sur le bouton "Run" (icône verte ▶)
   OU appuie sur Shift+F10
3. La console en bas affichera la sortie
```

**Ce qu'il affiche:**
- ✅ Tous les 10 endpoints API testés
- ✅ Toutes les données brutes (premiers enregistrements)
- ✅ Les colonnes de chaque endpoint
- ✅ Les 5 KPIs calculés avec détails

**Temps d'exécution:** ~5-10 secondes

---

### 2. **debug_api.py** (Pour déboguer)

Version simplifiée de ANALYTICS_FINAL.py

---

### 3. **analytics_kpis.py** (Pour KPIs détaillés)

Version encore plus détaillée avec analyses approfondies

---

## 📊 Les 5 KPIs à calculer

### 1️⃣ Candidats nouveaux et revenus
```
Endpoints utilisés:
  - GET /candidates?from=DATE_START&to=DATE_END
  
Données affichées:
  - Total candidats
  - Candidats nouveaux (is_new ou status='new')
  - Revenu total (si disponible)
  - Top booths par nombre de candidats
```

### 2️⃣ Interviews réalisées
```
Endpoints utilisés:
  - GET /interviews?from=DATE_START&to=DATE_END
  
Données affichées:
  - Total interviews
  - Répartition par statut (completed, pending, etc.)
```

### 3️⃣ CV créés, téléchargés, imprimés
```
Endpoints utilisés:
  - GET /cvs?from=DATE_START&to=DATE_END
  - GET /cvs/downloads?from=DATE_START&to=DATE_END
  - GET /cvs/prints?from=DATE_START&to=DATE_END
  
Données affichées:
  - Nombre de CV créés
  - Nombre de CV téléchargés
  - Nombre de CV imprimés
  - Taux de téléchargement (%)
  - Taux d'impression (%)
```

### 4️⃣ Annonces vues (par client, titre, organisation)
```
Endpoints utilisés:
  - GET /job-offers/analytics?from=DATE_START&to=DATE_END
  
Données affichées:
  - Total vues
  - Top 5 annonces les plus vues
  - Top 5 organisations les plus consultées
  - (Par client si disponible dans les données)
```

### 5️⃣ Candidatures (par organisation, titre)
```
Endpoints utilisés:
  - GET /applications?from=DATE_START&to=DATE_END
  
Données affichées:
  - Total candidatures
  - Top 5 titres d'annonces les plus postulés
  - Top 5 organisations les plus postulées
  - Répartition par statut (submitted, approved, rejected, etc.)
```

---

## 🔧 Configuration API

**PRODUCTION (actuellement utilisée):**
```
URL: https://app-api.ciblijob.fr/api
Clé: txf.hpc9aut9rbd2KWA
```

**STAGING (optionnel):**
```
URL: https://cibli-api.agency.lonestone.io/api
Clé: PGZ4qtc5jtf@rph3twf
```

---

## 📋 Endpoints API disponibles

| N° | Endpoint | Description |
|----|----------|-------------|
| 1 | GET /booths/all | Récupère les cabines |
| 2 | GET /candidates | Candidats |
| 3 | GET /interviews | Interviews |
| 4 | GET /cvs | CVs créés |
| 5 | GET /cvs/downloads | CVs téléchargés |
| 6 | GET /cvs/prints | CVs imprimés |
| 7 | GET /job-offers | Offres d'emploi |
| 8 | GET /applications | Candidatures |
| 9 | GET /job-offers/analytics | Analytics des offres |
| 10 | GET /applications/analytics | Analytics des candidatures |

**Paramètres:**
- `from`: Date de début (format: YYYY-MM-DD)
- `to`: Date de fin (format: YYYY-MM-DD)

---

## 🚀 Comment exécuter

### Via WebStorm:
```
1. Ouvre le fichier ANALYTICS_FINAL.py
2. Clique sur "Run" (Shift+F10)
3. Regarde la sortie dans la console
```

### Via terminal:
```bash
cd /home/vladkunitsyn/WebstormProjects/dataProcessingNotebooks
python3 ANALYTICS_FINAL.py
```

---

## 📊 Résultat attendu

Le script affichera ceci:

```
🚀 ANALYTICS DASHBOARD - CIBLI PRODUCTION
================================================================================
[HH:MM:SS] API: https://app-api.ciblijob.fr/api
[HH:MM:SS] Période: 2025-09-01 → 2026-01-19

📥 PHASE 1: RÉCUPÉRATION DES DONNÉES
...

📊 PHASE 2: DONNÉES BRUTES RÉCUPÉRÉES
✅ Booths: 50 enregistrements
✅ Candidates: 1234 enregistrements
...

📈 PHASE 3: CALCUL DES KPIs
1️⃣  KPI 1 - CANDIDATS NOUVEAUX & REVENUS
   Total candidats: 1234
   Candidats nouveaux: 567
   Revenu total: €12,345.67
   Top booths par candidats:
      • Booth Paris: 234
      • Booth Lyon: 123
...

📊 RÉSUMÉ FINAL DES KPIs
🎯 KPI 1 - Candidats
   └─ Total: 1234
🎯 KPI 2 - Interviews
   └─ Total: 456
🎯 KPI 3 - CV
   ├─ Créés: 1234
   ├─ Téléchargés: 890
   └─ Imprimés: 456
🎯 KPI 4 - Annonces vues
   └─ Total vues: 5678
🎯 KPI 5 - Candidatures
   └─ Total: 234

✅ ANALYSE COMPLÈTE
```

---

## ⚠️ Dépannage

### Le script prend trop de temps
- C'est normal, l'API peut être lente
- Timeout configuré à 15 secondes par requête

### "❌ HTTP 404"
- L'endpoint n'existe pas
- Vérifier l'URL et la clé API

### "❌ Timeout"
- Vérifier la connexion internet
- L'API peut être en maintenance

### Les données sont vides
- L'endpoint retourne une liste vide
- C'est possible si aucune donnée pour cette période

---

## 💾 Exporter les résultats

Pour sauvegarder les résultats:
```bash
python3 ANALYTICS_FINAL.py > resultats.txt
```

---

## 📝 Notes importantes

1. **Configuration dates:**
   - Début: 2025-09-01
   - Fin: 2026-01-19
   - À modifier dans le script si besoin

2. **Environnement:**
   - Actuellement en PRODUCTION
   - Pour STAGING, modifier `API_URL` et `API_KEY`

3. **Données sensibles:**
   - Les clés API sont hardcodées (à sécuriser en production)
   - À mettre en variables d'environnement dans un vrai projet

4. **Performance:**
   - ~10 requêtes HTTP
   - Timeout global: ~150 secondes (15s par requête)

---

## ✅ Checklist avant d'exécuter

- [ ] Connexion internet OK
- [ ] WebStorm ouvert
- [ ] Fichier ANALYTICS_FINAL.py ouvert
- [ ] API Key copié correctement
- [ ] Dates configurées

---

## 🎯 Objectif

Afficher les KPIs suivants en PRODUCTION:
- ✅ Nombre de candidats nouveaux + revenus
- ✅ Nombre d'interviews réalisées
- ✅ CV: créés, téléchargés, imprimés
- ✅ Annonces vues (par client, titre, organisation)
- ✅ Candidatures (par organisation, titre)

**Status: ✅ PRÊT À L'EMPLOI**

---

**Bon courage! 🚀**

