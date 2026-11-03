/*
Projet : Analyse des comportements d'achat des clients
Objet  : Analyses métier
Cible  : Microsoft SQL Server
Source : dbo.customer_shop

Prérequis :
- avoir exécuté et examiné 01_controles_qualite.sql ;
- avoir validé les volumes, les identifiants et les valeurs numériques.

Les montants sont exprimés en USD.
Une observation n'est pas assimilée à une commande distincte.
*/

USE [customer shopping];
GO

SET NOCOUNT ON;

-- ============================================================
-- Q1. Quels montants d'achat sont associés à chaque genre ?
-- ============================================================

SELECT
    gender,
    COUNT_BIG(DISTINCT customer_id) AS clients_distincts,
    CAST(
        SUM(CAST(purchase_amount AS DECIMAL(19,4)))
        AS DECIMAL(19,2)
    ) AS montant_total_achats_usd
FROM dbo.customer_shop
GROUP BY gender
ORDER BY montant_total_achats_usd DESC, gender ASC;

-- ============================================================
-- Q2. Quels clients ont bénéficié d'une remise tout en dépensant
-- strictement plus que le montant moyen global d'achat ?
-- ============================================================

SELECT
    customer_id,
    CAST(purchase_amount AS DECIMAL(19,2))
        AS montant_achat_usd
FROM dbo.customer_shop
WHERE discount_applied = N'Yes'
  AND CAST(purchase_amount AS DECIMAL(19,4)) > (
      SELECT AVG(CAST(purchase_amount AS DECIMAL(19,4)))
      FROM dbo.customer_shop
  )
ORDER BY
    CAST(purchase_amount AS DECIMAL(19,4)) DESC,
    customer_id ASC;

-- ============================================================
-- Q3. Quels sont les cinq produits ayant la meilleure note moyenne ?
-- Les notes imputées sont incluses dans le calcul.
-- ============================================================

SELECT TOP (5)
    item_purchased,
    COUNT_BIG(*) AS observations,
    CAST(
        AVG(CAST(review_rating AS DECIMAL(10,4)))
        AS DECIMAL(10,2)
    ) AS note_moyenne
FROM dbo.customer_shop
GROUP BY item_purchased
ORDER BY
    AVG(CAST(review_rating AS DECIMAL(10,4))) DESC,
    item_purchased ASC;

-- ============================================================
-- Q4. Comparer le montant moyen d'achat entre les modes
-- de livraison Standard et Express.
-- ============================================================

SELECT
    shipping_type,
    COUNT_BIG(*) AS observations,
    CAST(
        AVG(CAST(purchase_amount AS DECIMAL(19,4)))
        AS DECIMAL(19,2)
    ) AS montant_moyen_achat_usd
FROM dbo.customer_shop
WHERE shipping_type IN (N'Standard', N'Express')
GROUP BY shipping_type
ORDER BY shipping_type ASC;

-- ============================================================
-- Q5. Comparer les abonnés et les non-abonnés :
-- clients, observations, montant moyen et montant total.
-- ============================================================

SELECT
    subscription_status,
    COUNT_BIG(DISTINCT customer_id) AS clients_distincts,
    COUNT_BIG(*) AS observations,
    CAST(
        AVG(CAST(purchase_amount AS DECIMAL(19,4)))
        AS DECIMAL(19,2)
    ) AS montant_moyen_achat_usd,
    CAST(
        SUM(CAST(purchase_amount AS DECIMAL(19,4)))
        AS DECIMAL(19,2)
    ) AS montant_total_achats_usd
FROM dbo.customer_shop
GROUP BY subscription_status
ORDER BY
    SUM(CAST(purchase_amount AS DECIMAL(19,4))) DESC,
    subscription_status ASC;

-- ============================================================
-- Q6. Quels sont les cinq produits présentant la plus forte
-- proportion d'observations d'achat avec remise ?
-- Il ne s'agit pas du pourcentage de réduction sur le prix.
-- ============================================================

;WITH statistiques_produits AS (
    SELECT
        item_purchased,
        COUNT_BIG(*) AS observations,
        COUNT_BIG(
            CASE WHEN discount_applied = N'Yes' THEN 1 END
        ) AS observations_avec_remise
    FROM dbo.customer_shop
    GROUP BY item_purchased
)
SELECT TOP (5)
    item_purchased,
    observations,
    observations_avec_remise,
    CAST(
        100.0 * observations_avec_remise
        / NULLIF(observations, 0)
        AS DECIMAL(5,2)
    ) AS pourcentage_achats_avec_remise
FROM statistiques_produits
ORDER BY
    100.0 * observations_avec_remise
        / NULLIF(observations, 0) DESC,
    item_purchased ASC;

-- ============================================================
-- Q7. Répartir les clients selon les achats antérieurs.
-- Les conventions du rapport initial sont conservées.
-- Les cas non couverts ne sont pas classés automatiquement Loyal.
-- ============================================================

;WITH segmentation AS (
    SELECT
        customer_id,
        CASE
            WHEN previous_purchases = 1 THEN N'New'
            WHEN previous_purchases BETWEEN 2 AND 10
                THEN N'Returning'
            WHEN previous_purchases > 10 THEN N'Loyal'
            ELSE N'Non classé'
        END AS customer_segment
    FROM dbo.customer_shop
)
SELECT
    customer_segment,
    COUNT_BIG(DISTINCT customer_id) AS clients_distincts,
    COUNT_BIG(*) AS observations
FROM segmentation
GROUP BY customer_segment
ORDER BY
    CASE customer_segment
        WHEN N'New' THEN 1
        WHEN N'Returning' THEN 2
        WHEN N'Loyal' THEN 3
        ELSE 4
    END;

-- ============================================================
-- Q8. Quels sont les trois produits les plus représentés
-- dans les observations de chaque catégorie ?
-- En cas d'égalité, départage alphabétique du produit.
-- ============================================================

;WITH volumes_produits AS (
    SELECT
        category,
        item_purchased,
        COUNT_BIG(*) AS observations
    FROM dbo.customer_shop
    GROUP BY category, item_purchased
),
classement AS (
    SELECT
        category,
        item_purchased,
        observations,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY observations DESC, item_purchased ASC
        ) AS rang_produit
    FROM volumes_produits
)
SELECT
    category,
    rang_produit,
    item_purchased,
    observations
FROM classement
WHERE rang_produit <= 3
ORDER BY category ASC, rang_produit ASC;

-- ============================================================
-- Q9. Parmi les clients ayant plus de cinq achats antérieurs,
-- quelle est la répartition selon le statut d'abonnement ?
-- ============================================================

;WITH clients_recurrents AS (
    SELECT
        subscription_status,
        COUNT_BIG(DISTINCT customer_id) AS nombre_clients_recurrents
    FROM dbo.customer_shop
    WHERE previous_purchases > 5
    GROUP BY subscription_status
)
SELECT
    subscription_status,
    nombre_clients_recurrents,
    CAST(
        100.0 * nombre_clients_recurrents
        / NULLIF(
            SUM(nombre_clients_recurrents) OVER (),
            0
        )
        AS DECIMAL(5,2)
    ) AS part_des_clients_recurrents_pct
FROM clients_recurrents
ORDER BY nombre_clients_recurrents DESC, subscription_status ASC;

-- ============================================================
-- Q10. Quelle est la contribution de chaque groupe d'âge
-- au montant total des achats ?
-- ============================================================

SELECT
    age_group,
    COUNT_BIG(DISTINCT customer_id) AS clients_distincts,
    CAST(
        SUM(CAST(purchase_amount AS DECIMAL(19,4)))
        AS DECIMAL(19,2)
    ) AS montant_total_achats_usd
FROM dbo.customer_shop
GROUP BY age_group
ORDER BY
    SUM(CAST(purchase_amount AS DECIMAL(19,4))) DESC,
    age_group ASC;
