/*
Projet : Analyse des comportements d'achat des clients
Objet  : Comparer la table active et le chargement de validation
Cible  : Microsoft SQL Server

Script en lecture seule.

Les montants et les notes sont comparés à quatre décimales.
Les textes sont comparés selon la collation de la base.
Il ne s'agit pas d'une comparaison binaire des fichiers CSV.
*/

USE [customer shopping];
GO

SET NOCOUNT ON;

IF OBJECT_ID(N'dbo.customer_shop', N'U') IS NULL
BEGIN
    THROW 50010, N'La table active dbo.customer_shop est introuvable.', 1;
END;

IF OBJECT_ID(N'dbo.customer_shop_validation', N'U') IS NULL
BEGIN
    THROW 50011, N'Exécuter le chargement Python de validation avant cette comparaison.', 1;
END;

-- ============================================================
-- 1. Comparaison des volumes et des principaux agrégats
-- ============================================================

SELECT
    N'Table active' AS origine,
    COUNT_BIG(*) AS observations,
    COUNT_BIG(DISTINCT customer_id) AS clients_distincts,
    CAST(
        SUM(CAST(purchase_amount AS DECIMAL(19,4)))
        AS DECIMAL(19,2)
    ) AS montant_total_achats_usd,
    CAST(
        AVG(CAST(purchase_amount AS DECIMAL(19,4)))
        AS DECIMAL(19,2)
    ) AS montant_moyen_achat_usd,
    CAST(
        AVG(CAST(review_rating AS DECIMAL(10,4)))
        AS DECIMAL(10,2)
    ) AS note_moyenne
FROM dbo.customer_shop

UNION ALL

SELECT
    N'Table de validation',
    COUNT_BIG(*),
    COUNT_BIG(DISTINCT customer_id),
    CAST(
        SUM(CAST(purchase_amount AS DECIMAL(19,4)))
        AS DECIMAL(19,2)
    ),
    CAST(
        AVG(CAST(purchase_amount AS DECIMAL(19,4)))
        AS DECIMAL(19,2)
    ),
    CAST(
        AVG(CAST(review_rating AS DECIMAL(10,4)))
        AS DECIMAL(10,2)
    )
FROM dbo.customer_shop_validation;

-- ============================================================
-- 2. Comparaison des 19 colonnes métier
--
-- EXCEPT renvoie les lignes distinctes présentes d'un côté
-- et absentes de l'autre.
-- À interpréter avec les contrôles de volumes et d'unicité.
-- ============================================================

;WITH table_active AS (
    SELECT
        customer_id,
        age,
        gender,
        item_purchased,
        category,
        CAST(purchase_amount AS DECIMAL(19,4)) AS purchase_amount,
        location,
        size,
        color,
        season,
        CAST(review_rating AS DECIMAL(10,4)) AS review_rating,
        subscription_status,
        shipping_type,
        discount_applied,
        previous_purchases,
        payment_method,
        frequency_of_purchases,
        age_group,
        purchase_frequency_days
    FROM dbo.customer_shop
),
table_validation AS (
    SELECT
        customer_id,
        age,
        gender,
        item_purchased,
        category,
        CAST(purchase_amount AS DECIMAL(19,4)) AS purchase_amount,
        location,
        size,
        color,
        season,
        CAST(review_rating AS DECIMAL(10,4)) AS review_rating,
        subscription_status,
        shipping_type,
        discount_applied,
        previous_purchases,
        payment_method,
        frequency_of_purchases,
        age_group,
        purchase_frequency_days
    FROM dbo.customer_shop_validation
)
SELECT
    N'Active vers validation' AS sens_comparaison,
    COUNT_BIG(*) AS lignes_en_ecart
FROM (
    SELECT * FROM table_active
    EXCEPT
    SELECT * FROM table_validation
) AS ecarts_actifs

UNION ALL

SELECT
    N'Validation vers active',
    COUNT_BIG(*)
FROM (
    SELECT * FROM table_validation
    EXCEPT
    SELECT * FROM table_active
) AS ecarts_validation;
