# Recette du rapport Power BI

## 1. Périmètre

La recette porte sur le rapport local préparé à partir de la table SQL active `dbo.customer_shop`.

Elle complète la validation croisée entre Python et SQL Server.

Les contrôles du rapport local ne constituent pas, à eux seuls, une validation de la nouvelle version dans Power BI Service.

## 2. Connexion et actualisation locale

- [x] Connexion SQL paramétrée avec `pServeurSQL` et `pBaseSQL`.
- [x] Conservation de la table active `dbo.customer_shop` comme source.
- [x] Actualisation complète réussie dans la copie de validation.
- [x] Conservation des indicateurs de référence après actualisation.

## 3. Mesures numériques

| Contrôle sans filtre | Résultat validé |
|---|---:|
| Observations | 3 900 |
| Clients distincts | 3 900 |
| Clients masculins | 2 652 |
| Clients féminins | 1 248 |
| Montant total des achats | 233 071,00 USD |
| Montant moyen d’achat | 59,76 USD |
| Note moyenne | 3,75 |
| Observations avec remise | 1 677 |
| Proportion d’achats avec remise | 43,0 % |
| Montant des achats associés à une remise | 99 401,00 USD |
| Clients ayant plus de cinq achats antérieurs | 3 476 |

## 4. Segmentation

| Segment | Clients validés |
|---|---:|
| New | 83 |
| Returning | 701 |
| Loyal | 3 116 |
| Total | 3 900 |

- [x] Les règles non couvertes sont traitées par le libellé `Non classé`.
- [x] Aucun segment `Non classé` n’apparaît sur le périmètre global contrôlé.
- [x] Le graphique de segmentation utilise la mesure des clients distincts.

## 5. Carte HTML et filtres

| Sélection de genre | Total | Male | Female |
|---|---:|---:|---:|
| Aucune restriction | 3 900 | 2 652 | 1 248 |
| Female uniquement | 1 248 | 0 | 1 248 |
| Male uniquement | 2 652 | 2 652 | 0 |

- [x] Les badges sont empilés verticalement.
- [x] Le badge Male utilise un fond noir.
- [x] Le badge Female utilise un fond rose avec un texte bleu.
- [x] Les comptages respectent les filtres de genre.
- [x] Les nombres de la carte sont présentés avec des espaces comme séparateurs de milliers.

Ces résultats décrivent le jeu de données étudié et ne constituent pas une conclusion générale sur les comportements des clients.

## 6. Présentation

- [x] Les graphiques de volume utilisent le terme « observations ».
- [x] Les mesures sont organisées en dossiers d’affichage.
- [x] La copie destinée à la diffusion ne contient que les deux pages métier.
- [x] Les boutons de navigation ne proposent plus la page `Contrôles DAX`.
- [x] Le fichier s’ouvre sur Dashboard 1 sans filtre accidentel.

## 7. Exports

- [x] Le PDF contient exactement deux pages.
- [x] La carte HTML est correctement rendue dans le PDF.
- [x] Les graphiques et les textes du PDF sont lisibles.
- [x] Les captures PNG reflètent la version destinée à la diffusion.
- [x] Les captures ne présentent pas de menus, de poignées de sélection ou d’informations personnelles inutiles.

## 8. Vérifications avant release

- [x] Les fichiers diffusés ont fait l’objet d’une revue de confidentialité.
- [x] Les conditions de diffusion des données et des éléments graphiques ont été examinées ; les éventuelles restrictions sont respectées.
- [x] Le README principal correspond aux fichiers effectivement disponibles.
- [x] La version locale et la version publiée dans Power BI Service sont clairement distinguées.

Les cases ne doivent être cochées qu’après réalisation effective du contrôle correspondant.

## 9. Vérification des fichiers déposés

- [x] Le PBIX téléchargé depuis GitHub s’ouvre dans Power BI Desktop.
- [x] Le PBIX téléchargé contient les deux pages métier attendues.
- [x] Le PDF disponible sur GitHub est lisible et contient deux pages.
- [x] Les liens de téléchargement du dossier `power-bi` fonctionnent.

Ces vérifications portent sur les fichiers effectivement déposés, et non uniquement sur les copies locales.
