# Analyse des comportements d’achat des clients — Python, SQL Server & Power BI

### Segmentation clients, montants d’achat, satisfaction produits et recours aux remises

**Auteur :** Brice Abogo  
**Spécialisation :** Analyse financière | Comptabilité | Business Intelligence  
**Technologies :** Python / pandas | Microsoft SQL Server / T-SQL | Power Query / M | DAX | Power BI Desktop | Power BI Service | Passerelle de données locale

![Vue d’ensemble du rapport](images/tableau-de-bord-01.png)

---

## 1. Présentation du projet

Ce projet présente une chaîne de préparation, de contrôle et d’analyse de données consacrée aux comportements d’achat des clients.

À partir d’un fichier CSV de **3 900 observations**, les données sont examinées, nettoyées et enrichies dans **Python**. Elles sont ensuite exploitées dans **Microsoft SQL Server**, où des requêtes T-SQL répondent aux principales questions analytiques du projet.

Un rapport interactif de deux pages est construit dans **Power BI Desktop**, à partir d’une connexion SQL paramétrée, de mesures DAX et d’une carte personnalisée en HTML.

Une version du projet est déjà publiée dans **Power BI Service**, avec une actualisation configurée via une passerelle de données locale en mode standard.

Le projet met en évidence trois compétences complémentaires :

- préparer et contrôler un jeu de données ;
- traduire des questions métier en requêtes SQL et mesures DAX ;
- concevoir et documenter une restitution décisionnelle.

> Les données ne comportent ni date d’achat ni identifiant explicite de commande. Les résultats décrivent les observations disponibles et ne constituent pas un historique transactionnel complet.

---

## 2. Accès aux livrables

| Ressource | Accès |
|---|---|
| Rapport interactif Power BI | [Fichier PBIX](power-bi/analyse-comportement-achat-clients.pbix) |
| Rapport statique de deux pages | [Fichier PDF](power-bi/analyse-comportement-achat-clients.pdf) |
| Guide d’ouverture et d’actualisation | [Prise en main](documentation/prise-en-main-power-bi.md) |
| Contrôles du rapport | [Recette Power BI](documentation/recette-power-bi.md) |

GitHub ne fournit pas de lecteur interactif natif du PBIX. Le fichier doit être téléchargé et ouvert dans une version compatible de Power BI Desktop.

Les fichiers déposés constituent une version figée du projet. Ils ne sont pas actualisés automatiquement par Power BI Service.

---

## 3. Questions analysées

1. Comment les montants d’achat se répartissent-ils par genre ?
2. Quels clients ont bénéficié d’une remise tout en dépensant plus que la moyenne globale ?
3. Quels produits présentent les meilleures notes moyennes ?
4. Le montant moyen d’achat diffère-t-il entre les modes de livraison Standard et Express ?
5. Comment les abonnés et les non-abonnés se comparent-ils en montant moyen et en montant total d’achat ?
6. Quels produits présentent la plus forte proportion d’achats avec remise ?
7. Comment les clients se répartissent-ils selon leur nombre d’achats antérieurs ?
8. Quels sont les produits les plus représentés dans chaque catégorie ?
9. Quelle est la répartition des clients récurrents selon leur statut d’abonnement ?
10. Quelle est la contribution des groupes d’âge au montant total des achats ?

---

## 4. Outils et technologies

| Technologie | Usage |
|---|---|
| Python / pandas | Lecture du CSV, contrôle qualité, imputation, normalisation et enrichissement |
| SQLAlchemy / pyodbc | Chargement SQL de validation avec types explicites et relecture des données |
| Microsoft SQL Server | Stockage analytique, contrôles, rapprochements et analyses T-SQL |
| Power Query / M | Connexion SQL paramétrée, sélection des colonnes et typage |
| DAX | Agrégations, ratios, mesures filtrées et segmentation |
| HTML Content | Carte personnalisée du nombre de clients et de la répartition par genre |
| Power BI Desktop | Modèle sémantique et conception du rapport |
| Power BI Service | Publication et actualisation du modèle sémantique |
| Passerelle locale — mode standard | Accès à la source SQL locale depuis Power BI Service |
| GitHub | Documentation, versionnement des scripts et diffusion des livrables |

---

## 5. Données et périmètre

| Fichier | Rôle | Observations | Colonnes |
|---|---|---:|---:|
| `data/customer_shopping_behavior.csv` | Données sources | 3 900 | 18 |
| `data/customer_shopping_behavior_cleaned.csv` | Données préparées | 3 900 | 19 |

### Caractéristiques

- **Format source :** CSV.
- **Devise :** USD, d’après le libellé source `Purchase Amount (USD)`.
- **Période :** non déterminable à partir des colonnes disponibles.
- **Granularité constatée :** une observation par identifiant client dans la version contrôlée.
- **Provenance :** fichier obtenu sur Internet ; adresse exacte non identifiée avec certitude.
- **Licence des données :** non confirmée.
- **Finalité du projet :** pédagogique et démonstrative.

La colonne `customer_segment` est calculée dans Power BI et ne fait pas partie des 19 colonnes exportées par Python.

> La présence des CSV dans le dépôt ne signifie pas qu’ils sont placés sous licence MIT. Les droits sur les données et sur les éléments tiers sont distincts de la licence du code.

Détails dans [la documentation des données](data/README.md) et le [document relatif aux licences et à la provenance](NOTICE.md).

---

## 6. Préparation des données

Le script Python conserve le fichier source et produit un CSV nettoyé ainsi qu’un rapport qualité JSON.

| Traitement | Mise en œuvre |
|---|---|
| Validation du schéma | Vérification des colonnes attendues et détection des colonnes inattendues |
| Contrôle des valeurs | Conversions numériques explicites et vérification des données obligatoires |
| Imputation des notes | Remplacement des notes manquantes par la médiane de leur catégorie |
| Normalisation | Noms de colonnes en `snake_case` |
| Groupes d’âge | Quartiles calculés avec `pandas.qcut` |
| Fréquence d’achat | Correspondance conventionnelle entre libellés et nombres de jours |
| Redondance | Suppression de `promo_code_used` uniquement après vérification de son égalité avec `discount_applied` |
| Traçabilité | Versions logicielles, empreintes SHA-256, volumes et bornes des groupes d’âge |
| Protection des exports | Refus d’écrasement sans option explicite |

### Résultats du nettoyage

| Contrôle | Résultat |
|---|---:|
| Observations avant traitement | 3 900 |
| Observations après traitement | 3 900 |
| Clients distincts après traitement | 3 900 |
| Notes imputées | 37 |
| Part des observations concernées | Environ 0,95 % |

Aucune observation n’a été supprimée pendant le nettoyage.

Les groupes `Young Adult`, `Adult`, `Middle-aged` et `Senior` sont des groupes relatifs à la distribution des âges du fichier, et non des tranches d’âge métier fixes.

Le libellé `Bi-Weekly` est interprété comme « toutes les deux semaines », soit 14 jours. Les conversions mensuelles et trimestrielles sont conventionnelles.

Documentation et script : [python/](python/README.md).

---

## 7. Contrôles et validation croisée

La validation est réalisée à plusieurs niveaux :

1. contrôles du fichier pendant la préparation Python ;
2. contrôles de la structure et des données dans SQL Server ;
3. chargement indépendant dans `dbo.customer_shop_validation` ;
4. comparaison de cette table avec la table active `dbo.customer_shop` ;
5. contrôle des mesures et des filtres dans Power BI.

### Rapprochement SQL

| Indicateur | Table active | Table de validation |
|---|---:|---:|
| Observations | 3 900 | 3 900 |
| Clients distincts | 3 900 | 3 900 |
| Montant total des achats — USD | 233 071,00 | 233 071,00 |
| Montant moyen d’achat — USD | 59,76 | 59,76 |
| Note moyenne | 3,75 | 3,75 |

La comparaison des 19 colonnes a produit **zéro ligne en écart dans chaque sens**, après alignement des montants et des notes à quatre décimales, selon les règles de comparaison textuelle de SQL Server.

Les volumes et l’unicité des identifiants ont également été contrôlés.

La table active a été conservée sans modification. La table de validation n’est pas la source du rapport.

Détails : [validation des données](documentation/validation-des-donnees.md).

---

## 8. Architecture technique

```text
CSV source
    │
    ▼
Python / pandas
Contrôle, nettoyage et enrichissement
    │
    ├── CSV nettoyé
    └── Rapport qualité JSON
    │
    ▼
SQL Server — dbo.customer_shop
Contrôles et analyses T-SQL
    │
    ▼
Power Query
Connexion paramétrée et typage
    │
    ▼
Modèle Power BI / DAX / HTML Content
    │
    ▼
Rapport Power BI Desktop
    │
    ▼
Publication dans Power BI Service
```

Pour l’actualisation depuis le Service :

```text
Power BI Service
    │
    ▼
Passerelle de données locale — mode standard
    │
    ▼
SQL Server — dbo.customer_shop
```

Le script de chargement professionnalisé du dépôt alimente une table technique de validation. Il ne remplace pas automatiquement la table active utilisée par le rapport.

L’actualisation Power BI ne déclenche pas les traitements Python ni le chargement SQL.

---

## 9. Modèle de données et DAX

### Modèle

Le modèle repose sur une table analytique unique, `customer_shop`, sans relation intertable dans la version présentée.

Elle regroupe les attributs clients, les caractéristiques des produits et les informations associées aux observations d’achat.

![Modèle de données](images/modele-de-donnees.png)

### Organisation des calculs

| Famille | Exemples |
|---|---|
| Mesures de base | `Total Purchase`, `Total Observations`, `Number of customers` |
| Ratios et moyennes | `Avg purchase amount`, `Avg review rating`, `% Purchases with Discount` |
| Mesures filtrées | `Male customers`, `Female customers`, `Number of repeat buyers` |
| Colonne calculée | `customer_segment` |
| Présentation HTML | `HTML KPI Customers` |

### Points de conception

- distinction entre observations et clients distincts ;
- utilisation de `DISTINCTCOUNTNOBLANK` pour les clients ;
- utilisation de `DIVIDE` pour les ratios ;
- conservation des filtres avec `KEEPFILTERS` ;
- absence d’arrondi dans les mesures utilisées pour les classements ;
- utilisation de `FORMAT` uniquement pour la présentation HTML.

Les formules et leurs conventions sont disponibles dans [dax/](dax/README.md).

---

## 10. Pages du rapport

### Dashboard 1 — Vue d’ensemble et segmentation

Cette page présente :

- les quatre indicateurs globaux ;
- les montants d’achat et les observations par groupe d’âge ;
- la contribution des catégories de produits ;
- les montants associés aux abonnés et aux non-abonnés ;
- la segmentation selon les achats antérieurs.

La carte HTML présente le total des clients et deux badges verticaux :

- Male sur fond noir ;
- Female sur fond rose avec un texte bleu.

### Dashboard 2 — Produits, remises et abonnement

Cette page présente :

- les produits ayant les meilleures notes moyennes ;
- les produits ayant les plus fortes proportions d’achats avec remise ;
- la répartition des montants par mode de livraison ;
- la répartition selon l’application d’une remise ;
- une comparaison détaillée des abonnés et des non-abonnés.

![Analyse détaillée du rapport](images/tableau-de-bord-02.png)

**Filtres :** abonnement, genre et catégorie.

**Navigation :** boutons entre les deux pages métier.

Les intitulés du rapport sont principalement en anglais. La documentation du dépôt est rédigée en français.

---

## 11. Indicateurs et résultats

### Indicateurs globaux

Valeurs contrôlées sur le périmètre global, sans filtre :

| Indicateur | Valeur |
|---|---:|
| Observations | 3 900 |
| Clients distincts | 3 900 |
| Montant total des achats | 233 071,00 USD |
| Montant moyen d’achat | 59,76 USD |
| Note moyenne | 3,75 |
| Observations d’achat avec remise | 1 677 |
| Proportion d’observations avec remise | 43,0 % |
| Montant des achats associés à une remise | 99 401,00 USD |
| Clients ayant plus de cinq achats antérieurs | 3 476 |

Le montant des achats associés à une remise n’est pas le montant des réductions accordées.

### Répartition par genre

| Genre | Clients | Part |
|---|---:|---:|
| Male | 2 652 | 68,0 % |
| Female | 1 248 | 32,0 % |
| Total | 3 900 | 100,0 % |

Cette répartition décrit le fichier étudié et ne permet pas de conclure à la composition d’un marché ou d’une population plus large.

### Segmentation

| Segment | Convention | Clients | Part arrondie |
|---|---|---:|---:|
| New | 1 achat antérieur | 83 | 2,1 % |
| Returning | De 2 à 10 achats antérieurs | 701 | 18,0 % |
| Loyal | Plus de 10 achats antérieurs | 3 116 | 79,9 % |
| Total | | 3 900 | 100,0 % |

Les segments sont des conventions du projet. Le terme Loyal ne constitue pas une mesure indépendante et complète de la fidélité.

---

## 12. Constats et pistes d’analyse

1. **Le fichier est majoritairement composé de clients masculins.** Ils représentent 68 % des identifiants disponibles. Ce constat doit rester limité au périmètre du jeu de données.

2. **Le segment Loyal est prédominant.** Selon le seuil retenu, près de 80 % des clients présentent plus de dix achats antérieurs. Sans dates, il n’est pas possible d’en déduire une fréquence récente ou une rétention sur une période donnée.

3. **Les remises concernent 43 % des observations.** Leur présence est importante, mais les données ne permettent pas de mesurer leur effet causal sur les achats ou leur rentabilité.

4. **Les notes nécessitent une lecture documentée.** Les moyennes incluent 37 valeurs imputées par médiane de catégorie. Les classements doivent être interprétés avec les effectifs associés et cette méthode de préparation.

### Évolutions recommandées

- retrouver et documenter la source exacte ainsi que les conditions de réutilisation ;
- intégrer des dates et un identifiant de commande pour réaliser de véritables analyses transactionnelles ;
- ajouter les coûts et les montants de réduction pour analyser les marges et l’efficacité promotionnelle ;
- conserver un indicateur permettant d’identifier les notes imputées ;
- envisager un modèle en étoile si le périmètre et la granularité des données évoluent ;
- automatiser et tester séparément le chargement de la table active avant toute industrialisation.

---

## 13. Consultation et reproduction technique

### Consulter les résultats

Le PDF et les captures permettent de découvrir le rapport sans connexion SQL.

Le PBIX contient les données importées lors de sa dernière actualisation enregistrée. Son ouverture ne nécessite pas de relancer immédiatement les traitements.

### Exécuter les traitements

Les procédures sont documentées par composant :

1. [Préparation et contrôle Python](python/README.md)
2. [Contrôles et analyses SQL Server](sql/README.md)
3. [Connexion Power Query](power-query/README.md)
4. [Mesures et segmentation DAX](dax/README.md)
5. [Prise en main du rapport](documentation/prise-en-main-power-bi.md)

L’environnement de référence utilise Python 3.14 sous Windows et l’authentification Windows pour SQL Server.

La connexion Python nécessite également un pilote Microsoft ODBC pour SQL Server.

**Limite de reproductibilité :** les scripts fournis préparent les données et permettent un chargement de validation. Ils ne recréent pas automatiquement l’ensemble de l’environnement SQL actif, de la passerelle ou de Power BI Service.

---

## 14. Publication et actualisation

| Élément | Configuration |
|---|---|
| Plateforme | Power BI Service |
| Source | SQL Server — `dbo.customer_shop` |
| Passerelle | Passerelle de données locale — mode standard |
| Horaires configurés | 11 h 30 et 17 h 00 |
| Fuseau | Afrique du Sud — SAST, UTC+02:00 |

Une version du projet est déjà publiée dans le Service.

La version améliorée déposée sur GitHub ne remplace pas automatiquement cette publication. Une republication nécessite une vérification distincte des connexions, de la passerelle et des autorisations.

Les horaires concernent l’actualisation du modèle sémantique à partir de SQL Server, et non l’exécution du pipeline Python.

---

## 15. Organisation du dépôt

```text
.
├── README.md
├── LICENSE
├── NOTICE.md
├── .gitignore
├── data/              # CSV et rapport qualité
├── python/            # Nettoyage et chargement SQL de validation
├── sql/               # Contrôles, analyses et rapprochements
├── power-query/       # Paramètres et requête M
├── dax/               # Mesures, segmentation et carte HTML
├── power-bi/          # PBIX, PDF et documentation d’utilisation
├── images/            # Captures du rapport et du modèle
└── documentation/     # Méthodologie, validations et prise en main
```

### Documentation de référence

- [Données et contrôles Python](data/README.md)
- [Méthodologie et limites](documentation/methodologie-et-limites.md)
- [Validation croisée Python et SQL](documentation/validation-des-donnees.md)
- [Recette Power BI](documentation/recette-power-bi.md)
- [Prise en main du rapport](documentation/prise-en-main-power-bi.md)
- [Livrables Power BI](power-bi/README.md)

---

## 16. Licence et limites d’utilisation

Les scripts et la documentation originaux sont associés à la [licence MIT](LICENSE), sous réserve des droits détenus par leur auteur.

Cette licence ne couvre pas automatiquement les données sources, leurs dérivés ou les éléments tiers.

La source exacte et la licence d’origine des données restent non confirmées.

Le projet est une démonstration analytique. Les montants observés ne sont pas présentés comme un chiffre d’affaires comptable audité, et les comparaisons ne démontrent pas de causalité.

Consulter le document [Licences, provenance et conditions de diffusion](NOTICE.md) avant toute réutilisation ou redistribution.

## 17. Version publiée

La première version versionnée du projet est **v1.0.0**.

Elle regroupe le rapport Power BI, son export PDF, les données, les captures et les scripts documentés.

Consulter le [journal des modifications](CHANGELOG.md) pour connaître son contenu.


Télécharger la version v1.0.0 : https://github.com/YvesBriceAbogo/analyse-comportement-achat-clients/releases/tag/v1.0.0
