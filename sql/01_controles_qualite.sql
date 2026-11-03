/*
Projet : Analyse des comportements d'achat des clients
Objet  : Contrôles de structure et premiers rapprochements
Cible  : Microsoft SQL Server
Source : dbo.customer_shop

Script en lecture seule.
Aucune modification de la table ou de ses données.
*/

USE [customer shopping];
GO

SET NOCOUNT ON;

-- ============================================================
-- 1. Structure physique de la table
-- ============================================================

SELECT
    ORDINAL_POSITION AS position_colonne,
    COLUMN_NAME AS nom_colonne,
    DATA_TYPE AS type_donnee,
    CHARACTER_MAXIMUM_LENGTH AS longueur_maximale,
    NUMERIC_PRECISION AS precision_numerique,
    NUMERIC_SCALE AS nombre_decimales,
    IS_NULLABLE AS accepte_null
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = N'dbo'
  AND TABLE_NAME = N'customer_shop'
ORDER BY ORDINAL_POSITION;

-- ============================================================
-- 2. Volumes et identifiants
-- ============================================================

SELECT
    COUNT_BIG(*) AS observations,
    COUNT_BIG(DISTINCT customer_id) AS clients_distincts,
    COUNT_BIG(*) - COUNT_BIG(customer_id)
        AS identifiants_manquants,
    COUNT_BIG(customer_id) - COUNT_BIG(DISTINCT customer_id)
        AS repetitions_identifiants
FROM dbo.customer_shop;

-- Détail des identifiants répétés.
-- Un résultat vide est attendu pour la version actuelle du fichier.

SELECT
    customer_id,
    COUNT_BIG(*) AS nombre_observations
FROM dbo.customer_shop
GROUP BY customer_id
HAVING COUNT_BIG(*) > 1
ORDER BY nombre_observations DESC, customer_id;

-- ============================================================
-- 3. Contrôle des montants et des notes
-- ============================================================

DECLARE @MontantsInvalides BIGINT;
DECLARE @NotesInvalides BIGINT;

SELECT
    @MontantsInvalides = COUNT_BIG(
        CASE
            WHEN NULLIF(
                LTRIM(RTRIM(CONVERT(NVARCHAR(100), purchase_amount))),
                N''
            ) IS NULL
            OR TRY_CONVERT(DECIMAL(19,4), purchase_amount) IS NULL
            THEN 1
        END
    ),
    @NotesInvalides = COUNT_BIG(
        CASE
            WHEN NULLIF(
                LTRIM(RTRIM(CONVERT(NVARCHAR(100), review_rating))),
                N''
            ) IS NULL
            OR TRY_CONVERT(DECIMAL(10,4), review_rating) IS NULL
            THEN 1
        END
    )
FROM dbo.customer_shop;

SELECT
    @MontantsInvalides AS montants_absents_ou_invalides,
    @NotesInvalides AS notes_absentes_ou_invalides;

-- Ne pas produire de moyennes trompeuses si des valeurs sont invalides.
-- TRY_CONVERT sert ici au diagnostic, pas à ignorer des erreurs.

IF @MontantsInvalides > 0 OR @NotesInvalides > 0
BEGIN
    THROW 50001,
        N'Contrôle non validé : des montants ou des notes sont absents ou invalides. Examiner le chargement avant de poursuivre.',
        1;
END;

-- ============================================================
-- 4. Agrégats de référence
-- ============================================================

SELECT
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
FROM dbo.customer_shop;

-- ============================================================
-- 5. Effectifs des groupes d'âge
-- À rapprocher du rapport qualité Python.
-- ============================================================

SELECT
    age_group,
    COUNT_BIG(*) AS observations,
    COUNT_BIG(DISTINCT customer_id) AS clients_distincts
FROM dbo.customer_shop
GROUP BY age_group
ORDER BY
    CASE age_group
        WHEN N'Young Adult' THEN 1
        WHEN N'Adult' THEN 2
        WHEN N'Middle-aged' THEN 3
        WHEN N'Senior' THEN 4
        ELSE 5
    END;
