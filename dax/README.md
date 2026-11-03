# Mesures, segmentation et présentation DAX

## 1. Organisation

| Fichier | Famille | Contenu |
|---|---|---|
| `01_mesures_base.dax` | Mesures de base | Montants, observations et clients distincts |
| `02_indicateurs.dax` | Indicateurs et mesures filtrées | Moyennes, remises, genre et clients récurrents |
| `03_segmentation.dax` | Colonne calculée | Segmentation à partir des achats antérieurs |
| `04_carte_html.dax` | Présentation | Carte HTML du nombre de clients |

Les noms anglais des mesures existantes sont conservés pour préserver les références du rapport.

## 2. Installation

Les fichiers `.dax` constituent une documentation des définitions.

Ils ne doivent pas être exécutés en bloc dans la vue Requête DAX.

Chaque mesure doit être créée ou mise à jour séparément dans Power BI Desktop.

La définition `customer_segment` doit être intégrée comme une colonne calculée, et non comme une mesure.

Ordre d’intégration :

1. mesures de base ;
2. indicateurs ;
3. segmentation ;
4. carte HTML.

## 3. Observations et clients

- `Total Observations` dénombre les lignes.
- `Number of customers` dénombre les identifiants clients distincts et non vides.

Ces deux mesures valent 3 900 dans la version actuelle, mais représentent des concepts différents.

Aucun identifiant explicite de commande n’étant disponible, le projet ne définit pas de mesure certifiée de commandes distinctes.

## 4. Moyennes et formats

Les moyennes restent numériques et ne sont pas arrondies dans leurs formules.

Le nombre de décimales affichées est défini dans les formats des mesures ou des visuels.

`Avg purchase amount` correspond au montant total divisé par le nombre d’observations.

`Avg review rating` inclut les 37 notes imputées lors du nettoyage Python.

Les montants sont exprimés en USD, conformément au libellé de la colonne source.

## 5. Remises

`% Purchases with Discount` calcule la proportion d’observations pour lesquelles une remise est appliquée.

La mesure retourne une valeur comprise entre 0 et 1, à formater en pourcentage.

Elle ne mesure pas le pourcentage de réduction du prix.

`Purchase amount with discount applied` représente le montant des achats associés à une remise, et non le montant des réductions accordées.

## 6. Filtres et absence de données

Les mesures filtrées utilisent `KEEPFILTERS` pour respecter l’intersection avec les filtres du rapport.

Exemple : lorsque Female est sélectionné, Male customers retourne zéro.

Les comptages sont présentés à zéro en l’absence de clients ou d’observations.

Les ratios utilisant `DIVIDE` restent vides lorsque leur dénominateur est nul.

## 7. Segmentation

| Segment | Règle |
|---|---|
| `New` | 1 achat antérieur |
| `Returning` | De 2 à 10 achats antérieurs |
| `Loyal` | Plus de 10 achats antérieurs |
| `Non classé` | Valeur absente ou non couverte |

Ces règles sont des conventions analytiques propres au projet.

Le libellé New ne signifie pas nécessairement « premier achat ».

La segmentation est une colonne calculée lors du traitement du modèle.

La définition de client récurrent, plus de cinq achats antérieurs, est distincte de celle du segment Loyal.

## 8. Carte HTML

La mesure `HTML KPI Customers` est destinée au visuel HTML Content.

Elle réutilise les mesures numériques et présente :

- le total des clients ;
- les clients masculins sur fond noir ;
- les clients féminins sur fond rose, avec un texte bleu ;
- les badges empilés verticalement ;
- des nombres avec espaces insécables ;
- la police Segoe UI Semibold, si disponible dans l’environnement de rendu.

`FORMAT` est réservé à cette mesure de présentation. Les mesures analytiques restent numériques.

## 9. Formats recommandés

| Type d’indicateur | Format |
|---|---|
| Comptages | Nombre entier, sans décimales |
| Montants | Devise USD, deux décimales |
| Note moyenne | Nombre décimal, deux décimales |
| Proportion d’achats avec remise | Pourcentage, une ou deux décimales |

## 10. Contrôles numériques effectués

Les contrôles des mesures numériques dans la copie du PBIX ont confirmé, sans filtre :

| Mesure | Résultat |
|---|---:|
| Total Observations | 3 900 |
| Number of customers | 3 900 |
| Male customers | 2 652 |
| Female customers | 1 248 |
| Total Purchase | 233 071,00 USD |
| Avg purchase amount | 59,76 USD |
| Avg review rating | 3,75 |
| Observations with Discount | 1 677 |
| % Purchases with Discount | 43,0 % |
| Purchase amount with discount applied | 99 401,00 USD |
| Number of repeat buyers | 3 476 |

Le test numérique avec Female sélectionné a également confirmé :

- 1 248 observations ;
- 1 248 clients distincts ;
- zéro client masculin ;
- 1 248 clients féminins.

Les vérifications de la segmentation et du rendu HTML complètent ces contrôles avant la préparation du livrable final.

## 11. Classements Top 5

Les classements utilisent les mesures numériques non arrondies :

- `Avg review rating` pour les meilleures notes ;
- `% Purchases with Discount` pour la proportion d’achats avec remise.

Le filtre Top N de Power BI peut inclure des ex æquo à la limite du classement.

Il peut donc différer d’une requête SQL limitée strictement à cinq lignes avec départage alphabétique.

## 12. Compatibilité avec les anciennes mesures

Les mesures proposées ne nécessitent pas Total Orders, Total Revenue ou Avg Revenue.

Si ces anciennes mesures existent dans le PBIX, leurs dépendances doivent être examinées avant suppression.

Les visuels de volume privilégient Total Observations et des titres ne supposant pas l’existence de commandes distinctes.
