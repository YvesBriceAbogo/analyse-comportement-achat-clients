let
    // Connexion à la base SQL avec les paramètres du projet.
    Source = Sql.Database(
        pServeurSQL,
        pBaseSQL,
        [CreateNavigationProperties = false]
    ),

    // La table active reste la source du rapport.
    TableSource = Source{
        [Schema = "dbo", Item = "customer_shop"]
    }[Data],

    // Périmètre attendu : les 19 colonnes du fichier nettoyé.
    ColonnesAttendues = {
        "customer_id",
        "age",
        "gender",
        "item_purchased",
        "category",
        "purchase_amount",
        "location",
        "size",
        "color",
        "season",
        "review_rating",
        "subscription_status",
        "shipping_type",
        "discount_applied",
        "previous_purchases",
        "payment_method",
        "frequency_of_purchases",
        "age_group",
        "purchase_frequency_days"
    },

    // Une colonne absente provoque une erreur explicite.
    ColonnesSelectionnees = Table.SelectColumns(
        TableSource,
        ColonnesAttendues,
        MissingField.Error
    ),

    // Typage destiné au modèle Power BI.
    TypesDefinis = Table.TransformColumnTypes(
        ColonnesSelectionnees,
        {
            {"customer_id", Int64.Type},
            {"age", Int64.Type},
            {"gender", type text},
            {"item_purchased", type text},
            {"category", type text},
            {"purchase_amount", Currency.Type},
            {"location", type text},
            {"size", type text},
            {"color", type text},
            {"season", type text},
            {"review_rating", type number},
            {"subscription_status", type text},
            {"shipping_type", type text},
            {"discount_applied", type text},
            {"previous_purchases", Int64.Type},
            {"payment_method", type text},
            {"frequency_of_purchases", type text},
            {"age_group", type text},
            {"purchase_frequency_days", Int64.Type}
        }
    )
in
    TypesDefinis
