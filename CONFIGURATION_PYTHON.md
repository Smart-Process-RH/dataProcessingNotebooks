# 🔧 Configuration Python pour IDE

## 🚀 Configuration WebStorm/PyCharm

Pour que WebStorm exécute correctement le script `ats_cibli.py`, vous devez configurer l'interpréteur Python vers le **venv** :

### 1️⃣ Configuration WebStorm/PyCharm (Menu Préférences)

**Chemin:** `Settings` → `Project: dataProcessingNotebooks` → `Python Interpreter`

1. Cliquez sur **"Add..."** ou l'icône d'engrenage
2. Sélectionnez **"Add Local Interpreter"**
3. Choisissez **"Existing Environment"**
4. Naviguez vers: `/home/vladkunitsyn/WebstormProjects/dataProcessingNotebooks/venv/bin/python`
5. Cliquez **OK** et appliquez les changements

### 2️⃣ Vérifier la configuration

- Allez à `Settings` → `Project: dataProcessingNotebooks` → `Python Interpreter`
- Vous devriez voir:
  ```
  Python 3.12.3 (~/WebstormProjects/dataProcessingNotebooks/venv)
  ```

### 3️⃣ Configurer Run Configuration

**Pour lancer le script:**

1. Clic droit sur `ats_cibli.py`
2. Sélectionnez **"Run 'ats_cibli'"**
3. Ou utilisez: `Shift + F10` (Windows/Linux) ou `Ctrl + R` (macOS)

## 🖥️ Exécution en ligne de commande

### Option 1: Avec le script wrapper (RECOMMANDÉ)

```bash
cd /home/vladkunitsyn/WebstormProjects/dataProcessingNotebooks
bash run_ats_cibli.sh
```

### Option 2: Avec le venv activé

```bash
cd /home/vladkunitsyn/WebstormProjects/dataProcessingNotebooks
source venv/bin/activate
python3 ats_cibli.py
```

### Option 3: Sans activer le venv

```bash
cd /home/vladkunitsyn/WebstormProjects/dataProcessingNotebooks
./venv/bin/python3 ats_cibli.py
```

## 📋 Vérification des dépendances

Pour tester que tout est bien configuré:

```bash
cd /home/vladkunitsyn/WebstormProjects/dataProcessingNotebooks
bash diagnostic_python.sh
```

## 🆘 Dépannage

### ❌ Erreur: "ModuleNotFoundError: No module named 'pandas'"

**Solution:** Assurez-vous que le venv est utilisé:

```bash
# Créer/réinstaller le venv
python3 -m venv venv --upgrade-deps

# Installer les dépendances
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ Erreur: "python3: command not found"

**Solution:** Python3 doit être installé:

```bash
sudo apt update && sudo apt install python3 python3-venv python3-dev
```

### ❌ L'IDE ne reconnaît pas le venv

**Solution:** 
1. Supprimez le cache: `Settings` → `File` → `Invalidate Caches`
2. Redémarrez l'IDE
3. Reconfigurez l'interpréteur Python

## ✅ Configuration correcte

Quand tout est correctement configuré, vous devriez voir:

```
✅ Python 3.12.3 (~/WebstormProjects/dataProcessingNotebooks/venv)
✅ pandas: 2.1.0+
✅ numpy: 2.0.0+
✅ openpyxl: 3.1.0+
✅ requests: 2.31.0+
```

## 📝 Notes importantes

- Le `venv` est isolé et ne pollue pas le Python système
- Tous les scripts doivent être exécutés avec ce venv
- Le fichier `requirements.txt` liste toutes les dépendances nécessaires

---

**Dernière mise à jour:** 15 janvier 2026
**Version Python:** 3.12.3
**Statut:** ✅ Configuré et testé

