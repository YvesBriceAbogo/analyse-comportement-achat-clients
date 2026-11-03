# Données du projet

## 1. Fichiers attendus

| Fichier | Rôle |
|---|---|
| `customer_shopping_behavior.csv` | Fichier source, conservé sans modification |
| `customer_shopping_behavior_cleaned.csv` | Données préparées par le script Python |
| `rapport_qualite.json` | Métadonnées d’exécution et résultats des contrôles qualité |

Les fichiers CSV ne sont mis à disposition dans le dépôt que si leurs conditions de redistribution le permettent.

## 2. Provenance et conditions d’utilisation

Le fichier source a été obtenu sur Internet. Son adresse exacte et sa licence d’origine ne sont pas identifiées avec certitude.

Aucune autorisation de redistribution des données d’origine n’est revendiquée.

Une éventuelle licence appliquée aux scripts et à la documentation du projet ne doit pas être interprétée comme une licence accordée sur les données.

Avant toute diffusion, il convient également de vérifier l’absence de données personnelles ou confidentielles. Un identifiant client seul ne constitue pas une preuve d’anonymisation complète.

## 3. Structure attendue

Le script attend 18 colonnes dans le fichier source.

Après préparation, le fichier nettoyé comporte 19 colonnes :

- les noms de colonnes sont normalisés en `snake_case` ;
- `purchase_amount` conserve les montants exprimés en USD dans la source ;
- `age_group` est ajouté à partir des quartiles d’âge ;
- `purchase_frequency_days` est ajouté par conversion conventionnelle des fréquences déclarées ;
- `promo_code_used` est supprimé uniquement après vérification de son égalité avec `discount_applied`.

La colonne `customer_segment`, créée dans Power BI en DAX, ne fait pas partie de cet export Python.

## 4. Règles de préparation

### Notes produits

Les valeurs manquantes de `review_rating` sont remplacées par la médiane des notes de leur catégorie.

Si une catégorie ne possède aucune note exploitable, le script s’arrête : aucune médiane globale de remplacement n’est appliquée automatiquement.

### Groupes d’âge

Les groupes sont calculés avec `pandas.qcut`, selon les quartiles de la distribution.

Les libellés existants du rapport sont conservés :

- `Young Adult` ;
- `Adult` ;
- `Middle-aged` ;
- `Senior`.

Ces groupes ne correspondent pas à des tranches d’âge métier fixes. Leurs bornes et leurs effectifs sont enregistrés dans le rapport qualité.

### Fréquence d’achat

La conversion en jours repose sur une table de correspondance explicite.

Le libellé `Bi-Weekly` est interprété comme « toutes les deux semaines », soit 14 jours.

Les valeurs de 30 jours pour un mois et de 90 jours pour un trimestre sont des conventions, et non des durées mesurées entre des transactions.

## 5. Contrôles et traçabilité

Le traitement vérifie notamment :

- la présence des colonnes attendues ;
- la validité des conversions numériques ;
- les valeurs obligatoires ;
- les lignes strictement dupliquées après normalisation ;
- les modalités des indicateurs Oui/Non ;
- les fréquences d’achat non reconnues ;
- les notes restant manquantes après imputation ;
- la redondance entre remise et code promotionnel.

Aucune ligne n’est supprimée automatiquement.

Les identifiants clients répétés sont signalés et comptabilisés. Ils ne sont pas supprimés : plusieurs observations peuvent nécessiter une analyse métier avant toute décision.

Le rapport qualité conserve notamment :

- les versions de Python et de pandas ;
- les empreintes SHA-256 des fichiers source et nettoyé ;
- les volumes avant et après préparation ;
- le nombre de clients distincts ;
- le nombre de notes imputées ;
- les bornes et les effectifs des groupes d’âge ;
- les valeurs manquantes avant et après traitement.

## 6. Format des fichiers

- Séparateur CSV : virgule.
- Séparateur décimal : point.
- Export nettoyé : UTF-8, sans colonne d’index ajoutée.
- Le fichier source n’est jamais écrasé par le script.
- Un export existant n’est remplacé qu’avec l’option explicite `--ecraser`.

## 7. Limites d’interprétation

Une ligne représente une observation du fichier, pas nécessairement une commande distincte.

Le jeu de données présenté ne comporte pas de date d’achat ni d’identifiant explicite de commande.

Voir la [note méthodologique](../documentation/methodologie-et-limites.md).

## 8. Résultats du contrôle Python

L’exécution du script de préparation sur le fichier source utilisé pour cette version du projet a produit les résultats suivants :

| Contrôle | Résultat |
|---|---:|
| Observations dans le fichier source | 3 900 |
| Observations dans le fichier nettoyé | 3 900 |
| Clients distincts dans le fichier nettoyé | 3 900 |
| Notes imputées par la médiane de leur catégorie | 37 |

Les imputations concernent environ 0,95 % des observations.

Le nombre d’observations est conservé pendant le traitement. Le fichier nettoyé présente une observation par identifiant client dans cette version du jeu de données.

Cette correspondance ne permet pas d’assimiler les observations à des commandes distinctes : aucun identifiant explicite de commande n’est disponible.

Les détails de l’exécution, les empreintes des fichiers, les bornes des groupes d’âge et les contrôles de valeurs manquantes figurent dans le [rapport qualité](rapport_qualite.json).

La concordance avec la table SQL Server doit être contrôlée séparément.

## 9. Statut des fichiers et licence

Les fichiers source et nettoyé sont présents dans cette version du dépôt.

Leur présence ne constitue pas une déclaration selon laquelle ils seraient placés sous licence MIT.

La provenance exacte et la licence d’origine restent à confirmer. Aucune autorisation de réutilisation ou de redistribution n’est déduite de leur seule disponibilité sur Internet.

Les empreintes présentes dans le rapport qualité assurent la traçabilité technique des fichiers ; elles ne renseignent pas sur leurs droits d’utilisation.

Voir le document [Licences, provenance et conditions de diffusion](../NOTICE.md).
