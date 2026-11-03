"""Préparer les données d'achat et générer un rapport de contrôle qualité."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import platform
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


# Les chemins sont calculés depuis le script, sans chemin personnel.
RACINE = Path(__file__).resolve().parents[1]
SOURCE = RACINE / "data" / "customer_shopping_behavior.csv"
SORTIE = RACINE / "data" / "customer_shopping_behavior_cleaned.csv"
RAPPORT = RACINE / "data" / "rapport_qualite.json"

COLONNES_ATTENDUES = {
    "customer_id", "age", "gender", "item_purchased", "category",
    "purchase_amount", "location", "size", "color", "season",
    "review_rating", "subscription_status", "shipping_type",
    "discount_applied", "promo_code_used", "previous_purchases",
    "payment_method", "frequency_of_purchases",
}

TYPES_NUMERIQUES = {
    "customer_id": "Int64",
    "age": "Int64",
    "purchase_amount": "Float64",
    "review_rating": "Float64",
    "previous_purchases": "Int64",
}

GROUPES_AGE = ["Young Adult", "Adult", "Middle-aged", "Senior"]

FREQUENCES_JOURS = {
    "Fortnightly": 14,
    "Weekly": 7,
    "Monthly": 30,
    "Quarterly": 90,
    "Bi-Weekly": 14,
    "Annually": 365,
    "Every 3 Months": 90,
}


def empreinte_sha256(chemin: Path) -> str:
    """Calculer une empreinte permettant d'identifier le fichier utilisé."""
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def compter_valeurs_manquantes(data: pd.DataFrame) -> dict[str, int]:
    """Retourner des nombres entiers compatibles avec l'export JSON."""
    return {
        colonne: int(nombre)
        for colonne, nombre in data.isna().sum().items()
    }


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Nettoyer le CSV et produire un rapport qualité."
    )
    parser.add_argument(
        "--ecraser",
        action="store_true",
        help="Autoriser le remplacement des exports locaux existants.",
    )
    arguments = parser.parse_args()

    if not SOURCE.is_file():
        raise FileNotFoundError(
            "Fichier source introuvable. Placez "
            "'customer_shopping_behavior.csv' dans le dossier 'data'."
        )

    for fichier in (SORTIE, RAPPORT):
        if fichier.exists() and not arguments.ecraser:
            raise FileExistsError(
                f"Le fichier '{fichier.name}' existe déjà. "
                "Conservez une copie si nécessaire, puis utilisez "
                "--ecraser pour autoriser son remplacement."
            )

    # Lecture initiale en texte pour contrôler explicitement les conversions.
    data = pd.read_csv(
        SOURCE,
        sep=",",
        encoding="utf-8-sig",
        dtype="string",
    )

    if data.empty:
        raise ValueError("Le fichier source ne contient aucune observation.")

    lignes_source = len(data)

    # Normalisation des noms, sans modifier les valeurs métier.
    data.columns = [
        re.sub(r"[^a-z0-9]+", "_", colonne.strip().lower()).strip("_")
        for colonne in data.columns
    ]
    data = data.rename(
        columns={"purchase_amount_usd": "purchase_amount"}
    )

    if data.columns.has_duplicates:
        raise ValueError(
            "La normalisation produit des noms de colonnes dupliqués."
        )

    colonnes_manquantes = sorted(
        COLONNES_ATTENDUES - set(data.columns)
    )
    colonnes_inattendues = sorted(
        set(data.columns) - COLONNES_ATTENDUES
    )

    if colonnes_manquantes or colonnes_inattendues:
        raise ValueError(
            f"Colonnes manquantes : {colonnes_manquantes}. "
            f"Colonnes inattendues : {colonnes_inattendues}."
        )

    # Suppression des espaces périphériques et détection des cases vides.
    for colonne in data.columns:
        data[colonne] = data[colonne].str.strip().replace("", pd.NA)

    manquantes_avant = compter_valeurs_manquantes(data)

    # Dans ce traitement, seule la note peut être imputée automatiquement.
    colonnes_obligatoires = sorted(
        COLONNES_ATTENDUES - {"review_rating"}
    )
    incompletes = [
        colonne
        for colonne in colonnes_obligatoires
        if data[colonne].isna().any()
    ]

    if incompletes:
        raise ValueError(
            "Valeurs manquantes dans des colonnes obligatoires : "
            f"{incompletes}. Une décision de traitement est nécessaire."
        )

    # Conversion stricte : une valeur invalide provoque une erreur.
    for colonne, type_cible in TYPES_NUMERIQUES.items():
        valeurs = pd.to_numeric(data[colonne], errors="raise")
        valeurs_presentes = valeurs.dropna()

        if not valeurs_presentes.map(math.isfinite).all():
            raise ValueError(
                f"La colonne '{colonne}' contient une valeur non finie."
            )

        if (
            type_cible == "Int64"
            and (valeurs_presentes % 1 != 0).any()
        ):
            raise ValueError(
                f"La colonne '{colonne}' doit contenir des entiers."
            )

        data[colonne] = valeurs.astype(type_cible)

    if (data["customer_id"] <= 0).any():
        raise ValueError("Les identifiants clients doivent être positifs.")

    if (data["age"] <= 0).any():
        raise ValueError("Les âges doivent être strictement positifs.")

    if (data["purchase_amount"] < 0).any():
        raise ValueError(
            "Un montant négatif nécessite une analyse métier préalable."
        )

    if (data["previous_purchases"] < 0).any():
        raise ValueError(
            "Le nombre d'achats antérieurs ne peut pas être négatif."
        )

    # Contrôle des modalités utilisées par les indicateurs du rapport.
    for colonne in (
        "discount_applied",
        "promo_code_used",
        "subscription_status",
    ):
        inconnues = sorted(
            set(data[colonne].unique()) - {"Yes", "No"}
        )
        if inconnues:
            raise ValueError(
                f"Modalités non reconnues dans '{colonne}' : {inconnues}."
            )

    doublons_lignes = int(data.duplicated().sum())

    if doublons_lignes:
        raise ValueError(
            f"{doublons_lignes} ligne(s) strictement dupliquée(s) "
            "après normalisation. Aucune suppression automatique : "
            "vérifiez leur origine avant de poursuivre."
        )

    repetitions_identifiants = int(
        data["customer_id"].duplicated().sum()
    )

    if repetitions_identifiants:
        logging.warning(
            "%s répétition(s) d'identifiants clients détectée(s). "
            "Les lignes sont conservées ; distinguez observations "
            "et clients uniques.",
            repetitions_identifiants,
        )

    # Imputation de la note par la médiane de sa catégorie.
    notes_a_imputer = int(data["review_rating"].isna().sum())
    medianes = data.groupby("category")["review_rating"].transform("median")

    data["review_rating"] = data["review_rating"].fillna(medianes)

    if data["review_rating"].isna().any():
        categories_sans_note = sorted(
            data.loc[
                data["review_rating"].isna(), "category"
            ].unique().tolist()
        )
        raise ValueError(
            "Imputation impossible : aucune note exploitable pour "
            f"les catégories suivantes : {categories_sans_note}."
        )

    # Les quartiles sont conservés pour documenter les groupes d'âge.
    try:
        data["age_group"], bornes_age = pd.qcut(
            data["age"],
            q=4,
            labels=GROUPES_AGE,
            retbins=True,
        )
    except ValueError as erreur:
        raise ValueError(
            "Impossible de construire quatre groupes d'âge distincts. "
            "Vérifiez la distribution des âges ; les groupes ne seront "
            "pas modifiés automatiquement."
        ) from erreur

    frequences_inconnues = sorted(
        set(data["frequency_of_purchases"].unique())
        - set(FREQUENCES_JOURS)
    )

    if frequences_inconnues:
        raise ValueError(
            "Fréquences d'achat sans correspondance : "
            f"{frequences_inconnues}."
        )

    data["purchase_frequency_days"] = (
        data["frequency_of_purchases"]
        .map(FREQUENCES_JOURS)
        .astype("Int64")
    )

    # Suppression conditionnelle, et non aveugle, de la colonne redondante.
    colonnes_identiques = data["discount_applied"].eq(
        data["promo_code_used"]
    ).all()

    if not colonnes_identiques:
        raise ValueError(
            "'discount_applied' et 'promo_code_used' diffèrent. "
            "La suppression du code promotionnel doit être réexaminée."
        )

    data = data.drop(columns="promo_code_used")

    if data.isna().any().any():
        raise ValueError(
            "Le contrôle final détecte encore des valeurs manquantes."
        )

    # Export : le fichier brut n'est jamais modifié.
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(
        SORTIE,
        sep=",",
        index=False,
        encoding="utf-8",
        lineterminator="\n",
    )

    rapport = {
        "execution_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        ),
        "version_python": platform.python_version(),
        "version_pandas": pd.__version__,
        "fichier_source": SOURCE.name,
        "sha256_source": empreinte_sha256(SOURCE),
        "fichier_nettoye": SORTIE.name,
        "sha256_nettoye": empreinte_sha256(SORTIE),
        "lignes_source": lignes_source,
        "lignes_sortie": len(data),
        "colonnes_sortie": len(data.columns),
        "clients_distincts": int(data["customer_id"].nunique()),
        "repetitions_identifiants": repetitions_identifiants,
        "lignes_dupliquees_detectees": doublons_lignes,
        "notes_imputees": notes_a_imputer,
        "valeurs_manquantes_avant": manquantes_avant,
        "valeurs_manquantes_apres": compter_valeurs_manquantes(data),
        "bornes_quartiles_age": [
            float(borne) for borne in bornes_age
        ],
        "effectifs_groupes_age": {
            str(groupe): int(effectif)
            for groupe, effectif in data["age_group"]
            .value_counts(sort=False)
            .items()
        },
        "correspondance_frequences_jours": FREQUENCES_JOURS,
        "promo_code_used_supprime_apres_verification": True,
        "montant_total_achats": float(data["purchase_amount"].sum()),
        "montant_moyen_achat": float(data["purchase_amount"].mean()),
        "note_moyenne": float(data["review_rating"].mean()),
        "liste_colonnes_sortie": data.columns.tolist(),
    }

    RAPPORT.write_text(
        json.dumps(
            rapport,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )

    logging.info(
        "Nettoyage terminé : %s observations ; %s clients distincts.",
        len(data),
        rapport["clients_distincts"],
    )
    logging.info("Notes imputées : %s.", notes_a_imputer)
    logging.info(
        "Montant total des achats : %.2f USD.",
        rapport["montant_total_achats"],
    )
    logging.info("Export : %s", SORTIE.name)
    logging.info("Rapport qualité : %s", RAPPORT.name)


if __name__ == "__main__":
    main()
