# Journal des modifications

Ce document présente les évolutions significatives du projet.

## v1.0.0 — Version initiale

### Préparation et contrôle des données

- Ajout d’un script Python de nettoyage et d’enrichissement.
- Validation du schéma et des conversions numériques.
- Imputation de 37 notes manquantes par la médiane de leur catégorie.
- Normalisation des noms de colonnes en `snake_case`.
- Création des groupes d’âge par quartiles.
- Conversion conventionnelle des fréquences d’achat en jours.
- Suppression de la colonne de code promotionnel après contrôle de sa redondance.
- Génération d’un rapport qualité avec empreintes SHA-256 et métadonnées d’exécution.

### SQL Server

- Ajout des contrôles de structure, de volumes et de valeurs numériques.
- Documentation de dix analyses métier en T-SQL.
- Ajout d’un chargement transactionnel dans une table technique de validation.
- Comparaison des 19 colonnes entre la table active et la table de validation.
- Conservation de la table active `dbo.customer_shop` comme source du rapport.

### Power BI

- Connexion Power Query paramétrée et typage explicite.
- Structuration des mesures DAX par famille.
- Comptage distinct des clients non vides.
- Sécurisation des ratios et respect des filtres.
- Traitement explicite des cas non couverts par la segmentation.
- Carte HTML présentant le total des clients et la répartition par genre.
- Clarification des graphiques de volume avec le terme « observations ».
- Préparation d’un rapport de diffusion limité aux deux pages métier.

### Livrables et documentation

- Rapport Power BI au format PBIX.
- Export PDF de deux pages.
- Captures PNG du rapport et du modèle.
- Fichiers CSV source et nettoyé.
- Documentation de la méthodologie, des contrôles et de la prise en main.
- Clarification du périmètre de la licence MIT et des réserves sur les données.

### Résultats de validation

| Contrôle | Résultat |
|---|---:|
| Observations source et nettoyées | 3 900 |
| Clients distincts | 3 900 |
| Notes imputées | 37 |
| Montant total des achats | 233 071,00 USD |
| Montant moyen d’achat | 59,76 USD |
| Note moyenne | 3,75 |
| Écarts entre les tables SQL comparées | 0 dans chaque sens |

Les comparaisons SQL sont réalisées selon les conventions de précision numérique et de comparaison textuelle documentées.

### Exploitation et limites

- Une version du projet est déjà publiée dans Power BI Service.
- L’actualisation est configurée via une passerelle locale standard à 11 h 30 et 17 h 00, heure d’Afrique du Sud — UTC+02:00.
- La publication GitHub ne remplace pas automatiquement la version du Service.
- Les traitements Python et le chargement SQL ne sont pas déclenchés par l’actualisation Power BI.
- Le jeu de données ne comporte ni date d’achat ni identifiant explicite de commande.
- La provenance exacte et la licence d’origine des données restent non confirmées.
