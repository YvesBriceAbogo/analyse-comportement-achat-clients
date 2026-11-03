# Rapport Power BI et livrables

## 1. Présentation

Le rapport analyse les comportements d’achat à partir des données préparées dans Python et chargées dans Microsoft SQL Server.

Il comprend deux pages :

- `Dashboard 1` : vue d’ensemble et segmentation ;
- `Dashboard 2` : produits, remises, livraison et abonnement.

Les intitulés du rapport sont principalement en anglais. La documentation du projet est rédigée en français.

## 2. Livrables préparés

| Fichier | Usage |
|---|---|
| `analyse-comportement-achat-clients.pbix` | Rapport interactif et modèle Power BI |
| `analyse-comportement-achat-clients.pdf` | Consultation statique des deux pages |

La mise à disposition du PBIX est finalisée lors de la préparation de la release, en fonction de sa taille et des conditions de diffusion applicables.

Les captures PNG sont disponibles dans le dossier [images](../images/).

## 3. Version destinée à la diffusion

La version de diffusion est préparée à partir d’une copie de validation.

Elle ne contient pas la page temporaire `Contrôles DAX`.

Les tests intermédiaires ne sont pas présentés comme une troisième page métier du rapport.

Les graphiques de volume utilisent le terme « observations », en l’absence d’identifiant explicite de commande.

## 4. Indicateurs de référence

Sur le périmètre global, sans filtre :

| Indicateur | Valeur |
|---|---:|
| Clients distincts | 3 900 |
| Observations | 3 900 |
| Montant total des achats | 233 071,00 USD |
| Montant moyen d’achat | 59,76 USD |
| Note moyenne | 3,75 |

## 5. Ouverture du PBIX

L’ouverture et la modification du fichier nécessitent une version compatible de Power BI Desktop.

GitHub ne fournit pas de lecteur interactif natif des fichiers PBIX.

Le fichier peut contenir les données importées lors de sa dernière actualisation enregistrée.

Pour actualiser les données, l’utilisateur doit disposer :

- d’un accès à SQL Server ;
- de la table `dbo.customer_shop` correctement alimentée ;
- des autorisations de connexion nécessaires ;
- de valeurs adaptées pour les paramètres `pServeurSQL` et `pBaseSQL`.

Dans un autre environnement, `Localhost` désigne l’ordinateur de cet utilisateur, et non le serveur de l’auteur.

## 6. Visuel personnalisé

La carte du nombre de clients utilise le visuel HTML Content.

Son rendu et son export doivent être vérifiés dans l’environnement utilisé.

Le PDF et les PNG ne conservent pas les interactions du rapport.

## 7. Publication dans Power BI Service

Une version du projet est déjà publiée dans Power BI Service.

L’actualisation du modèle sémantique est configurée via une passerelle de données locale en mode standard :

- 11 h 30 ;
- 17 h 00 ;
- fuseau Afrique du Sud — SAST, UTC+02:00.

La préparation des fichiers de diffusion ne remplace pas automatiquement la version publiée dans le Service.

Le téléchargement du PBIX ne donne pas accès à l’espace de travail, à la passerelle ou au rapport privé de l’auteur.

L’actualisation planifiée ne déclenche pas le nettoyage Python ni le chargement SQL.

## 8. Confidentialité et conditions de diffusion

Un PBIX en mode Import peut contenir les données détaillées, même lorsque les pages du rapport ne présentent que des agrégats.

Masquer une colonne ou une page ne constitue pas une mesure de protection des données contenues dans le fichier.

Les conditions de redistribution des données et des éléments graphiques doivent être examinées avant leur publication.

L’origine exacte et la licence du fichier source ne sont pas confirmées. Aucune autorisation de redistribution n’est déduite de sa seule disponibilité sur Internet.

## 9. Contrôles

Les vérifications sont documentées dans :

- la [validation Python et SQL Server](../documentation/validation-des-donnees.md) ;
- la [recette Power BI](../documentation/recette-power-bi.md).
