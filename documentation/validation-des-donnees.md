# Validation des données : Python et SQL Server

## 1. Objectif

La validation vise à vérifier la conservation des observations pendant le nettoyage, puis la concordance entre le fichier préparé en Python et les données disponibles dans SQL Server.

Les résultats ci-dessous concernent la version des données contrôlée pour ce projet. Ils doivent être revérifiés après toute modification du fichier source ou des règles de préparation.

## 2. Résultats du nettoyage Python

| Contrôle | Résultat |
|---|---:|
| Observations dans le fichier source | 3 900 |
| Observations dans le fichier nettoyé | 3 900 |
| Clients distincts dans le fichier nettoyé | 3 900 |
| Notes imputées par médiane de catégorie | 37 |

Aucune observation n’a été supprimée pendant le traitement.

Les imputations concernent environ 0,95 % des observations.

Le détail de l’exécution est disponible dans le [rapport qualité Python](../data/rapport_qualite.json).

## 3. Contrôles de la table SQL active

Table examinée : `dbo.customer_shop`.

| Contrôle | Résultat |
|---|---:|
| Observations | 3 900 |
| Clients distincts | 3 900 |
| Identifiants manquants | 0 |
| Répétitions d’identifiants | 0 |
| Montants absents ou invalides | 0 |
| Notes absentes ou invalides | 0 |

Types physiques observés dans la table active :

- `purchase_amount` : `BIGINT` ;
- `review_rating` : `FLOAT`.

Ces types n’ont pas été modifiés pendant la validation.

## 4. Chargement indépendant de validation

Le CSV nettoyé a été chargé dans une table technique distincte :

`dbo.customer_shop_validation`

Le chargement utilise notamment les types suivants :

- montants : `DECIMAL(19,4)` ;
- notes : `DECIMAL(10,4)` ;
- textes : `NVARCHAR` avec longueurs définies.

Le script Python vérifie l’empreinte du CSV, puis relit les données chargées pour les comparer aux valeurs préparées.

Ce chargement ne remplace pas la table active.

## 5. Rapprochement des indicateurs

| Indicateur | Table active | Table de validation |
|---|---:|---:|
| Observations | 3 900 | 3 900 |
| Clients distincts | 3 900 | 3 900 |
| Montant total des achats — USD | 233 071,00 | 233 071,00 |
| Montant moyen d’achat — USD | 59,76 | 59,76 |
| Note moyenne | 3,75 | 3,75 |

Les moyennes sont présentées avec deux décimales.

## 6. Comparaison des données détaillées

Le script SQL compare les 19 colonnes issues du CSV nettoyé.

| Sens de comparaison | Lignes en écart |
|---|---:|
| Table active vers table de validation | 0 |
| Table de validation vers table active | 0 |

La comparaison :

- aligne les montants et les notes à quatre décimales ;
- utilise les règles de comparaison textuelle de la base SQL ;
- repose sur `EXCEPT`, avec vérification complémentaire des volumes et de l’unicité des identifiants.

Elle ne constitue pas une comparaison binaire des fichiers.

## 7. Décision technique

La table active `dbo.customer_shop` est conservée comme source du rapport Power BI.

La table `dbo.customer_shop_validation` reste une table technique de contrôle.

Aucune modification du schéma de la table active ni aucun basculement de source Power BI n’a été effectué pendant cette validation.

## 8. Scripts associés

- [Nettoyage Python](../python/nettoyer_donnees.py)
- [Chargement SQL de validation](../python/charger_sql_validation.py)
- [Contrôles SQL](../sql/01_controles_qualite.sql)
- [Comparaison des deux tables](../sql/03_comparaison_chargement.sql)
