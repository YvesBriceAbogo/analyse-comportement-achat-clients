# Méthodologie, conventions et limites

## 1. Origine et usage des données

Le projet utilise un fichier CSV obtenu sur Internet. L’adresse exacte de la source et sa licence d’origine ne sont pas identifiées avec certitude.

Le projet poursuit un objectif pédagogique et de démonstration de compétences en préparation de données, analyse SQL et Business Intelligence.

L’accessibilité publique du fichier ne constitue pas, à elle seule, une autorisation de redistribution. Une éventuelle licence appliquée aux scripts du projet ne s’étend pas automatiquement aux données ni aux éléments graphiques tiers.

## 2. Périmètre analytique et granularité

Le fichier associe des caractéristiques clients à une observation d’achat : produit, catégorie, montant, livraison, remise et note.

Le jeu de données ne comporte pas de date d’achat ni d’identifiant explicite de commande dans les colonnes présentées.

En conséquence :

- aucune période commerciale précise n’est attribuée aux résultats ;
- aucune analyse chronologique des achats n’est revendiquée ;
- un décompte de lignes représente un nombre d’observations, et non une preuve de commandes distinctes ;
- le nombre de clients doit être calculé à partir des identifiants distincts, après vérification de leur complétude et de leur unicité ;
- les montants agrégés sont présentés comme des montants d’achat observés, sans les assimiler à un chiffre d’affaires comptable audité.

Les intitulés « Orders » du rapport initial devront être interprétés à la lumière de ces limites.

## 3. Préparation des données dans Python

Les traitements comprennent :

- l’examen de la structure, des types et des valeurs manquantes ;
- l’imputation des notes manquantes par la médiane de leur catégorie de produits ;
- la normalisation des noms de colonnes en `snake_case` ;
- la création des groupes d’âge ;
- la conversion des fréquences d’achat déclarées en nombres de jours ;
- la vérification de la redondance entre les indicateurs de remise et de code promotionnel ;
- l’export d’un fichier CSV nettoyé.

Les volumes avant et après traitement, les valeurs imputées et les éventuelles anomalies seront documentés dans les contrôles qualité.

Une catégorie dont toutes les notes seraient manquantes ne permettrait pas, à elle seule, de calculer une médiane d’imputation.

## 4. Groupes d’âge

La variable `age_group` est construite avec `pandas.qcut`, à partir des quartiles de la distribution des âges.

Les libellés `Young Adult`, `Adult`, `Middle-aged` et `Senior` désignent donc des groupes relatifs au fichier étudié, et non des tranches d’âge métier fixes.

Les bornes effectivement calculées devront être conservées dans la documentation du traitement. Des âges identiques peuvent conduire à des effectifs légèrement différents entre groupes.

## 5. Fréquence d’achat

La variable `purchase_frequency_days` est une conversion conventionnelle des fréquences déclarées.

Les valeurs de 30 jours pour un mois et de 90 jours pour un trimestre sont des approximations.

Le libellé anglais `Bi-Weekly`, potentiellement ambigu, est interprété dans ce projet comme « toutes les deux semaines », soit 14 jours. Il ne s’agit pas d’un délai mesuré entre des transactions datées.

## 6. Segmentation des clients

La segmentation initiale repose sur `previous_purchases` :

- `New` : 1 achat antérieur ;
- `Returning` : de 2 à 10 achats antérieurs ;
- `Loyal` : plus de 10 achats antérieurs.

Il s’agit de conventions analytiques propres au projet. Le libellé `New` ne signifie donc pas nécessairement « premier achat ».

Les valeurs nulles, négatives ou égales à zéro devront faire l’objet d’un traitement explicite, et non être automatiquement classées dans le segment `Loyal`.

## 7. Interprétation des indicateurs

- Le pourcentage d’achats avec remise mesure la part des observations pour lesquelles `discount_applied = "Yes"`. Il ne mesure pas le pourcentage de réduction sur le prix.
- Les moyennes de notes calculées après imputation incluent les notes imputées.
- Les comparaisons entre abonnés et non-abonnés sont descriptives : elles ne démontrent pas un effet causal de l’abonnement.
- L’absence de coûts et de marges ne permet pas de conclure à la rentabilité des produits ou des promotions.

## 8. Actualisation et reproductibilité

Le rapport est publié dans Power BI Service avec une passerelle de données locale en mode standard.

L’actualisation est configurée à 11 h 30 et 17 h 00, heure d’Afrique du Sud : SAST, UTC+02:00.

Cette planification actualise le modèle sémantique à partir de SQL Server. Elle ne déclenche pas automatiquement le nettoyage Python ni le rechargement de la table SQL.

Les captures PNG, l’export PDF et le fichier PBIX déposés sur GitHub constituent des versions figées. Ils ne sont pas mis à jour automatiquement par Power BI Service.
