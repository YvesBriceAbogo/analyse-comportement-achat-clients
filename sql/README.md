# Contrôles et analyses dans Microsoft SQL Server

## 1. Objectif

Ce dossier regroupe les scripts T-SQL de contrôle et d’analyse de la table `dbo.customer_shop`.

Les scripts sont destinés à Microsoft SQL Server. Ils ne reposent pas sur la syntaxe PostgreSQL.

## 2. Scripts disponibles

| Ordre | Fichier | Fonction |
|---|---|---|
| 1 | `01_controles_qualite.sql` | Examiner le schéma, les volumes, les identifiants, les valeurs numériques et les agrégats de référence |
| 2 | `02_analyses_metier.sql` | Répondre aux dix questions analytiques du projet |

Ces scripts sont en lecture seule. La création et l’alimentation de la table relèvent d’une étape distincte.

## 3. Environnement cible

- Base de données : `customer shopping`.
- Schéma : `dbo`.
- Table : `customer_shop`.
- Authentification de l’environnement local : Windows.

Le nom de la base contient un espace ; il est donc encadré par des crochets dans l’instruction `USE`.

Les scripts ne contiennent aucun mot de passe.

## 4. Ordre d’exécution

1. Exécuter `01_controles_qualite.sql`.
2. Examiner les résultats et les éventuels messages d’erreur.
3. Comparer les volumes et les agrégats avec le rapport qualité Python.
4. Exécuter `02_analyses_metier.sql` uniquement après validation des contrôles.

Les scripts peuvent être exécutés dans SQL Server Management Studio ou dans un éditeur SQL connecté au serveur.

GitHub héberge les fichiers mais n’exécute pas ces requêtes sur le serveur local.

## 5. Conventions de calcul

### Montants d’achat

Les montants sont convertis explicitement en `DECIMAL(19,4)` avant les agrégations.

Cette conversion évite notamment la troncature que peut produire `AVG()` sur une colonne de type entier.

Les résultats monétaires destinés à la lecture sont présentés avec deux décimales. Ces conversions de calcul ne modifient pas les types physiques de la table.

### Notes produits

Les notes sont converties en `DECIMAL(10,4)` pour le calcul des moyennes.

Les moyennes incluent les notes imputées pendant la préparation Python. Les 37 imputations sont documentées dans le rapport qualité ; elles ne sont pas identifiables individuellement à partir de la seule table finale.

### Clients et observations

- `COUNT_BIG(*)` dénombre les observations.
- `COUNT_BIG(DISTINCT customer_id)` dénombre les identifiants clients distincts.

Dans la version contrôlée du fichier Python, les deux nombres sont égaux à 3 900. Leur égalité dans SQL Server doit être vérifiée.

Les observations ne sont pas présentées comme des commandes certifiées.

### Achats avec remise

Le pourcentage d’achats avec remise correspond à :

Nombre d’observations avec remise / Nombre total d’observations × 100.

Il ne mesure pas le taux de réduction appliqué au prix.

Les pourcentages produits par les requêtes SQL sont exprimés sur une échelle de 0 à 100.

### Segmentation

Les conventions du rapport initial sont conservées :

- `New` : 1 achat antérieur ;
- `Returning` : de 2 à 10 achats antérieurs ;
- `Loyal` : plus de 10 achats antérieurs.

Les autres cas sont classés `Non classé`, plutôt que d’être automatiquement considérés comme fidèles.

Le groupe des clients récurrents, défini par plus de 5 achats antérieurs, est distinct du segment `Loyal`.

## 6. Classements et égalités

Les classements utilisent les valeurs non arrondies.

Un second critère alphabétique sur le produit rend les résultats déterministes en cas d’égalité.

Les requêtes renvoient au maximum cinq produits pour les Top 5 et trois produits par catégorie pour le Top 3. Elles ne cherchent pas à inclure tous les ex æquo.

## 7. Limites

Les comparaisons sont descriptives et ne démontrent pas de relation causale.

En particulier :

- une proportion élevée d’achats avec remise ne prouve pas l’efficacité commerciale d’une promotion ;
- une différence entre abonnés et non-abonnés ne démontre pas un effet de l’abonnement ;
- les montants d’achat ne permettent pas, sans coûts associés, de mesurer la rentabilité.

Voir également la [note méthodologique](../documentation/methodologie-et-limites.md).
