# Connexion et typage des données dans Power Query

## 1. Objectif

Power Query connecte le rapport Power BI à la table active `dbo.customer_shop` dans SQL Server.

Le nettoyage et les enrichissements métier sont réalisés en amont dans Python.

## 2. Fichiers

| Fichier | Fonction |
|---|---|
| `pServeurSQL.pq` | Définition du paramètre du serveur SQL |
| `pBaseSQL.pq` | Définition du paramètre de la base de données |
| `customer_shop.pq` | Connexion, sélection des colonnes et typage |

Les fichiers `.pq` sont des copies texte du code M. Leur présence sur GitHub ne les applique pas automatiquement au fichier PBIX.

## 3. Paramètres

| Paramètre | Type | Valeur de référence |
|---|---|---|
| `pServeurSQL` | Texte | `Localhost` |
| `pBaseSQL` | Texte | `customer shopping` |

Les paramètres doivent être créés dans l’éditeur Power Query, via « Gérer les paramètres ».

Les valeurs doivent correspondre à l’environnement SQL réellement utilisé.

## 4. Source retenue

- Schéma : `dbo`.
- Table active : `customer_shop`.
- Table technique de contrôle, non utilisée par le rapport : `customer_shop_validation`.

Le nom de la requête Power BI reste `customer_shop` afin de préserver les références existantes.

## 5. Transformations

La requête :

1. ouvre la connexion SQL ;
2. sélectionne la table active ;
3. conserve les 19 colonnes attendues ;
4. applique les types destinés au modèle.

Une colonne attendue absente provoque une erreur.

Les éventuelles colonnes supplémentaires de la table SQL ne sont pas importées automatiquement.

Aucune ligne n’est filtrée ou supprimée par cette requête.

## 6. Types principaux

| Champs | Type Power Query |
|---|---|
| Identifiant, âge, achats antérieurs, fréquence en jours | Nombre entier — `Int64.Type` |
| Montant d’achat | Nombre décimal fixe — `Currency.Type` |
| Note produit | Nombre décimal — `type number` |
| Attributs descriptifs | Texte |

Le type `Currency.Type` ne réalise aucune conversion de devise.

Ces transformations ne modifient pas les types physiques de la table SQL.

## 7. Colonne calculée DAX

La colonne `customer_segment` est calculée dans le modèle avec DAX.

Elle n’est pas une colonne attendue dans la source SQL et ne doit pas être ajoutée à la liste des colonnes importées pour cette raison.

## 8. Vérification avant publication

Les modifications doivent d’abord être testées sur une copie du fichier PBIX :

- actualisation complète réussie ;
- conservation des 3 900 observations ;
- concordance des indicateurs de référence ;
- conservation des visuels, mesures et filtres.

La validation d’une copie locale ne prouve pas, à elle seule, que l’actualisation dans Power BI Service est opérationnelle.

## 9. Passerelle et actualisation

Le rapport publié utilise une passerelle de données locale en mode standard.

Horaires configurés :

- 11 h 30 ;
- 17 h 00 ;
- fuseau Afrique du Sud — SAST, UTC+02:00.

Avant toute republication, vérifier la correspondance entre les paramètres de connexion et la source configurée dans la passerelle.

`Localhost` désigne la machine sur laquelle la connexion s’exécute. Dans le contexte de la passerelle, il s’agit donc de la machine hébergeant cette passerelle.

La planification Power BI ne déclenche pas le nettoyage Python ni le chargement SQL.
