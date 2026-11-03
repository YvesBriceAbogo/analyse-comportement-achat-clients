"""Charger le CSV nettoyé dans une table SQL de validation distincte."""

from __future__ import annotations

import hashlib
import json
import logging
import os
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pyodbc
from sqlalchemy import (
    BigInteger,
    Integer,
    Numeric,
    Unicode,
    create_engine,
    inspect,
    text,
)
from sqlalchemy.engine import URL


RACINE = Path(__file__).resolve().parents[1]

FICHIER_CSV = (
    RACINE / "data" / "customer_shopping_behavior_cleaned.csv"
)
FICHIER_QUALITE = RACINE / "data" / "rapport_qualite.json"

SCHEMA_SQL = "dbo"
TABLE_VALIDATION = "customer_shop_validation"

# La table active customer_shop n'est jamais une cible de ce script.
TYPES_SQL = {
    "customer_id": BigInteger(),
    "age": Integer(),
    "gender": Unicode(30),
    "item_purchased": Unicode(100),
    "category": Unicode(50),
    "purchase_amount": Numeric(19, 4),
    "location": Unicode(100),
    "size": Unicode(10),
    "color": Unicode(50),
    "season": Unicode(30),
    "review_rating": Numeric(10, 4),
    "subscription_status": Unicode(3),
    "shipping_type": Unicode(50),
    "discount_applied": Unicode(3),
    "previous_purchases": Integer(),
    "payment_method": Unicode(50),
    "frequency_of_purchases": Unicode(50),
    "age_group": Unicode(30),
    "purchase_frequency_days": Integer(),
}

COLONNES_ENTIERES = [
    "customer_id",
    "age",
    "previous_purchases",
    "purchase_frequency_days",
]

COLONNES_DECIMALES = [
    "purchase_amount",
    "review_rating",
]


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    # --------------------------------------------------------
    # 1. Vérifier les fichiers et leur cohérence
    # --------------------------------------------------------

    if not FICHIER_CSV.is_file() or not FICHIER_QUALITE.is_file():
        raise FileNotFoundError(
            "Le CSV nettoyé et le rapport qualité doivent être "
            "présents dans le dossier data."
        )

    rapport = json.loads(
        FICHIER_QUALITE.read_text(encoding="utf-8")
    )

    empreinte_csv = hashlib.sha256(
        FICHIER_CSV.read_bytes()
    ).hexdigest()

    if empreinte_csv != rapport["sha256_nettoye"]:
        raise ValueError(
            "Le CSV ne correspond pas à l'empreinte enregistrée "
            "dans le rapport qualité. Vérifiez les fichiers utilisés."
        )

    # Lecture en texte pour maîtriser les conversions.
    data = pd.read_csv(
        FICHIER_CSV,
        sep=",",
        encoding="utf-8",
        dtype="string",
        keep_default_na=False,
    )

    if set(data.columns) != set(TYPES_SQL):
        raise ValueError(
            "Le schéma du CSV ne correspond pas aux 19 colonnes attendues."
        )

    # Ordre déterministe pour le chargement et la comparaison.
    data = data[list(TYPES_SQL)].copy()

    if data.empty:
        raise ValueError("Le CSV nettoyé est vide.")

    if data.isna().any().any() or data.eq("").any().any():
        raise ValueError(
            "Le CSV nettoyé contient des valeurs absentes."
        )

    if len(data) != int(rapport["lignes_sortie"]):
        raise ValueError(
            "Le nombre de lignes diffère de celui du rapport qualité."
        )

    # --------------------------------------------------------
    # 2. Préparer les types Python avant insertion
    # --------------------------------------------------------

    for colonne in COLONNES_ENTIERES:
        # int() refuse notamment une chaîne décimale telle que "1.5".
        data[colonne] = data[colonne].map(int)

    for colonne in COLONNES_DECIMALES:
        type_sql = TYPES_SQL[colonne]
        pas_decimal = Decimal(1).scaleb(-type_sql.scale)
        limite = Decimal(10) ** (
            type_sql.precision - type_sql.scale
        )

        valeurs = data[colonne].map(Decimal)

        for valeur in valeurs:
            if not valeur.is_finite():
                raise ValueError(
                    f"Valeur non finie dans '{colonne}'."
                )

            if (
                abs(valeur) >= limite
                or valeur != valeur.quantize(pas_decimal)
            ):
                raise ValueError(
                    f"Une valeur de '{colonne}' ne peut pas être "
                    "stockée dans le type SQL prévu sans perte."
                )

        data[colonne] = valeurs.map(
            lambda valeur: valeur.quantize(pas_decimal)
        )

    for colonne, type_sql in TYPES_SQL.items():
        if isinstance(type_sql, Unicode):
            if data[colonne].str.len().gt(type_sql.length).any():
                raise ValueError(
                    f"Texte trop long dans '{colonne}' pour "
                    f"la longueur SQL prévue : {type_sql.length}."
                )

    if not data["customer_id"].is_unique:
        raise ValueError(
            "Ce chargement de validation attend une observation "
            "par client. Des identifiants sont répétés."
        )

    if (
        data["customer_id"].nunique()
        != int(rapport["clients_distincts"])
    ):
        raise ValueError(
            "Le nombre de clients distincts diffère du rapport qualité."
        )

    # --------------------------------------------------------
    # 3. Préparer la connexion Windows
    # --------------------------------------------------------

    serveur = os.getenv("SQLSERVER_SERVER", "localhost")
    base = os.getenv("SQLSERVER_DATABASE", "customer shopping")

    pilotes_installes = pyodbc.drivers()

    pilote = next(
        (
            nom
            for nom in (
                "ODBC Driver 18 for SQL Server",
                "ODBC Driver 17 for SQL Server",
            )
            if nom in pilotes_installes
        ),
        None,
    )

    if pilote is None:
        raise RuntimeError(
            "Aucun pilote Microsoft ODBC 18 ou 17 pour SQL Server "
            "n'est disponible. Installez le pilote Microsoft adapté."
        )

    # TrustServerCertificate=yes est limité ici à l'environnement
    # local de développement. Pour une infrastructure de production,
    # utiliser un certificat approuvé et sa validation.
    chaine_odbc = (
        f"DRIVER={{{pilote}}};"
        f"SERVER={serveur};"
        f"DATABASE={base};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    url = URL.create(
        "mssql+pyodbc",
        query={"odbc_connect": chaine_odbc},
    )

    moteur = create_engine(
        url,
        fast_executemany=True,
        pool_pre_ping=True,
    )

    # --------------------------------------------------------
    # 4. Charger et vérifier dans une même transaction
    # --------------------------------------------------------

    try:
        with moteur.begin() as connexion:
            if inspect(connexion).has_table(
                TABLE_VALIDATION,
                schema=SCHEMA_SQL,
            ):
                raise FileExistsError(
                    "La table dbo.customer_shop_validation existe "
                    "déjà. Aucun remplacement automatique n'est autorisé."
                )

            data.to_sql(
                name=TABLE_VALIDATION,
                schema=SCHEMA_SQL,
                con=connexion,
                if_exists="fail",
                index=False,
                dtype=TYPES_SQL,
                chunksize=1000,
                method=None,
            )

            # Les noms viennent exclusivement du schéma défini ci-dessus.
            liste_colonnes = ", ".join(
                f"[{colonne}]" for colonne in TYPES_SQL
            )

            requete = text(
                f"SELECT {liste_colonnes} "
                f"FROM [{SCHEMA_SQL}].[{TABLE_VALIDATION}] "
                "ORDER BY [customer_id];"
            )

            lignes_sql = [
                tuple(ligne)
                for ligne in connexion.execute(requete).all()
            ]

            lignes_python = list(
                data.sort_values("customer_id").itertuples(
                    index=False,
                    name=None,
                )
            )

            if lignes_sql != lignes_python:
                raise ValueError(
                    "La relecture SQL ne correspond pas aux données "
                    "préparées. Le chargement est annulé."
                )

    finally:
        moteur.dispose()

    logging.info(
        "Chargement validé : %s observations et %s clients distincts.",
        len(data),
        data["customer_id"].nunique(),
    )
    logging.info(
        "Les 19 colonnes ont été vérifiées après relecture SQL."
    )
    logging.info(
        "Table créée : %s.%s.",
        SCHEMA_SQL,
        TABLE_VALIDATION,
    )
    logging.info(
        "La table active dbo.customer_shop n'a pas été modifiée."
    )


if __name__ == "__main__":
    main()
