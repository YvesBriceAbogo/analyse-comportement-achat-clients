# Préparation des données avec Python

## 1. Objectif

Le script `nettoyer_donnees.py` prépare le fichier source CSV et produit :

- `data/customer_shopping_behavior_cleaned.csv` ;
- `data/rapport_qualite.json`.

Il ne réalise pas le chargement dans SQL Server et ne déclenche aucune actualisation Power BI.

## 2. Prérequis

- Python 3.14 pour l’environnement de référence du projet ;
- les dépendances définies dans `requirements.txt` ;
- le fichier source placé dans `data/customer_shopping_behavior.csv`.

Les chemins du projet sont calculés automatiquement à partir de l’emplacement du script.

## 3. Installation sous Windows

Depuis le dossier racine du projet :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r python/requirements.txt
```

L’environnement virtuel `.venv` doit rester local et ne doit pas être téléversé sur GitHub.

## 4. Exécution

```powershell
.\.venv\Scripts\python.exe python/nettoyer_donnees.py
```

Le script refuse par défaut de remplacer un fichier nettoyé ou un rapport qualité déjà présent.

Pour régénérer explicitement ces exports :

```powershell
.\.venv\Scripts\python.exe python/nettoyer_donnees.py --ecraser
```

Cette option remplace uniquement les exports locaux prévus par le script. Elle ne modifie pas le fichier source ni SQL Server.

## 5. Lecture du rapport qualité

Le fichier `rapport_qualite.json` est généré automatiquement.

Il permet de vérifier :

- le maintien du nombre d’observations ;
- le nombre de clients distincts ;
- les répétitions d’identifiants ;
- les valeurs manquantes ;
- le nombre de notes imputées ;
- les bornes des groupes d’âge ;
- les principaux agrégats de comparaison avec SQL et Power BI.

Il ne doit pas être rempli ou corrigé manuellement pour correspondre aux résultats attendus.

## 6. Gestion des anomalies

Le script s’arrête notamment si :

- des colonnes sont absentes ou inattendues ;
- une valeur numérique ne peut pas être convertie ;
- des données obligatoires sont manquantes ;
- des lignes strictement dupliquées nécessitent une revue ;
- une catégorie ne permet pas d’imputer sa note médiane ;
- une fréquence d’achat n’est pas reconnue ;
- les colonnes de remise et de code promotionnel divergent.

Il ne faut pas supprimer un contrôle uniquement pour faire disparaître une erreur. L’anomalie et la règle de traitement doivent d’abord être examinées.

## 7. Traçabilité et validation

Le rapport qualité enregistre la version de Python, celle de pandas et les empreintes des fichiers.

La concordance entre le fichier régénéré, la table SQL Server et le rapport Power BI doit être vérifiée avant la publication d’une release.

Les valeurs relevées dans les captures du rapport constituent des références de comparaison, et non des résultats de tests exécutés automatiquement.

## 8. Chargement de validation dans SQL Server

Le script `charger_sql_validation.py` charge le CSV nettoyé dans une table distincte :

`dbo.customer_shop_validation`

Il ne modifie pas la table active `dbo.customer_shop`.

### Dépendances supplémentaires

```powershell
.\.venv\Scripts\python.exe -m pip install -r python/requirements-sql.txt
```

Un pilote Microsoft ODBC Driver 18 ou 17 for SQL Server doit également être installé sur l’ordinateur. Le paquet Python `pyodbc` ne remplace pas ce pilote système.

### Connexion locale

L’authentification Windows utilise l’identité du compte qui exécute Python.

```powershell
$env:SQLSERVER_SERVER = "localhost"
$env:SQLSERVER_DATABASE = "customer shopping"
```

Aucun mot de passe n’est stocké dans le script.

Le compte Windows doit disposer des autorisations nécessaires pour créer et alimenter la table de validation.

### Exécution

```powershell
.\.venv\Scripts\python.exe python/charger_sql_validation.py
```

Le script :

- vérifie l’empreinte du CSV par rapport au rapport qualité ;
- prépare les types numériques et les longueurs de texte ;
- charge les données avec des types SQL explicites ;
- relit et compare les 19 colonnes ;
- encadre le chargement et sa vérification dans une transaction.

Il refuse de remplacer une table de validation déjà existante.

### Types de validation

- Montants : `DECIMAL(19,4)`.
- Notes : `DECIMAL(10,4)`.
- Identifiants : `BIGINT`.
- Textes : `NVARCHAR` avec longueurs définies.

Ces choix ne modifient pas les types de la table active.

### Certificat de connexion

La configuration proposée utilise une connexion chiffrée avec `TrustServerCertificate=yes`, pour l’environnement local de développement.

Pour une infrastructure de production, utiliser un certificat approuvé et conserver sa validation.

### Comparaison avec la table active

Après un chargement réussi, exécuter :

`sql/03_comparaison_chargement.sql`

Une concordance des données ne déclenche aucun remplacement automatique de la table active.
