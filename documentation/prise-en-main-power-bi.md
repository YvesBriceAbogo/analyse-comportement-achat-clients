# Prise en main du rapport Power BI

## 1. Choisir le mode de consultation

| Besoin | Support recommandé |
|---|---|
| Découvrir rapidement les résultats | Captures PNG et README principal |
| Consulter les deux pages sans Power BI Desktop | Export PDF |
| Utiliser les filtres et examiner les mesures | Fichier PBIX |
| Examiner les traitements et les contrôles | Scripts Python, SQL, Power Query et DAX |

Les livrables sont présentés dans le dossier [power-bi](../power-bi/README.md).

## 2. Consulter le PDF

Le PDF permet une lecture statique du rapport.

Il ne nécessite pas de connexion à SQL Server.

Les segments, boutons et interactions du rapport ne fonctionnent pas comme dans Power BI Desktop ou Power BI Service.

## 3. Ouvrir le PBIX

### Prérequis

Une version compatible et suffisamment récente de Power BI Desktop est nécessaire.

GitHub ne fournit pas de lecteur interactif natif des fichiers PBIX.

### Procédure

1. Ouvrir le fichier PBIX dans le dossier `power-bi` sur GitHub.
2. Utiliser le bouton de téléchargement du fichier brut.
3. Enregistrer le fichier sur l’ordinateur.
4. L’ouvrir avec Power BI Desktop.

Le fichier contient les données importées lors de sa dernière actualisation enregistrée.

La consultation de ces données ne nécessite pas de relancer immédiatement l’actualisation SQL.

### Rapport attendu

Le rapport destiné à la diffusion comprend deux pages :

- Dashboard 1 ;
- Dashboard 2.

La page temporaire de contrôle DAX n’est pas incluse dans cette version.

## 4. Utiliser les filtres

Les segments portent sur :

- le statut d’abonnement ;
- le genre ;
- la catégorie de produits.

Les indicateurs et la carte HTML réagissent aux sélections.

Pour retrouver les résultats globaux, effacer les sélections des segments et vérifier les éventuels filtres de page ou de rapport.

## 5. Actualiser les données dans un autre environnement

L’actualisation nécessite une source SQL accessible. Le PBIX ne crée pas automatiquement la base ou la table SQL.

Objets attendus :

- base de référence : `customer shopping` ;
- schéma : `dbo` ;
- table active : `customer_shop`.

La table technique `customer_shop_validation` n’est pas la source du rapport.

### Paramètres de connexion

| Paramètre | Fonction |
|---|---|
| `pServeurSQL` | Serveur ou instance SQL Server |
| `pBaseSQL` | Base de données contenant la table active |

La valeur `Localhost` désigne l’ordinateur sur lequel la connexion s’exécute. Elle ne donne pas accès au serveur de l’auteur depuis un autre ordinateur.

### Adapter la connexion

Dans Power BI Desktop :

1. ouvrir « Transformer les données » ;
2. ouvrir « Gérer les paramètres » ;
3. renseigner les valeurs correspondant à l’environnement SQL utilisé ;
4. appliquer les modifications ;
5. fournir les informations d’authentification demandées ;
6. lancer une actualisation complète.

L’environnement de référence du projet utilise l’authentification Windows.

Le compte utilisé doit disposer des autorisations SQL nécessaires.

Les paramètres de connexion et les identifiants personnels ne doivent pas être publiés pour faciliter cette configuration.

### Préparation de la source

Les traitements et les conventions sont documentés dans :

- [Préparation Python](../python/README.md) ;
- [Contrôles et analyses SQL](../sql/README.md) ;
- [Connexion Power Query](../power-query/README.md).

Le script Python de chargement de validation alimente une table technique distincte. Il ne remplace pas automatiquement la table active.

Les scripts ne constituent pas un ordonnanceur automatisé de l’ensemble de la chaîne.

## 6. Indicateurs de référence

Sur le périmètre global, sans filtre :

| Indicateur | Valeur |
|---|---:|
| Observations | 3 900 |
| Clients distincts | 3 900 |
| Montant total des achats | 233 071,00 USD |
| Montant moyen d’achat | 59,76 USD |
| Note moyenne | 3,75 |
| Proportion d’observations avec remise | 43,0 % |

Une différence après actualisation doit être examinée à partir des données sources, des filtres et des contrôles qualité.

Les formules ne doivent pas être ajustées artificiellement pour retrouver ces valeurs.

## 7. Visuel HTML Content

La carte du nombre de clients utilise un visuel personnalisé HTML Content.

Elle présente le total et la répartition par genre.

Le rendu dépend de la compatibilité du visuel avec l’environnement Power BI utilisé et des éventuelles restrictions de l’organisation sur les visuels personnalisés.

Les définitions sont disponibles dans le dossier [dax](../dax/README.md).

## 8. Power BI Service et passerelle

Une version du projet est déjà publiée dans Power BI Service.

L’actualisation est configurée avec une passerelle de données locale en mode standard :

- 11 h 30 ;
- 17 h 00 ;
- heure d’Afrique du Sud — SAST, UTC+02:00.

Le téléchargement du PBIX ne donne pas accès :

- à l’espace de travail Power BI de l’auteur ;
- à sa connexion SQL ;
- à sa passerelle ;
- à ses autorisations de partage.

Une nouvelle publication nécessite une vérification distincte des connexions, de la passerelle et des autorisations.

L’actualisation Power BI ne déclenche pas automatiquement le nettoyage Python ou le chargement SQL.

## 9. Versions figées et version publiée

Les PBIX, PDF et PNG disponibles sur GitHub représentent un état enregistré du projet.

Ils ne changent pas automatiquement lorsque le rapport du Service est actualisé.

La version améliorée déposée sur GitHub et la version déjà publiée dans le Service doivent être distinguées tant qu’une republication contrôlée n’a pas été effectuée.

## 10. Confidentialité et droits

Le PBIX peut contenir les données détaillées importées.

Masquer un champ ou une page ne retire pas les données du fichier et ne constitue pas une mesure de protection suffisante.

Les conditions de diffusion des données et des éléments graphiques restent applicables aux fichiers téléchargés.

Consulter les informations de provenance et les limites dans :

- [Données du projet](../data/README.md) ;
- [Méthodologie et limites](methodologie-et-limites.md).
