import pandas as pd
import numpy as np

def group_verb_assignments(df):
    """
    Gruppiert den DataFrame nach einzigartigen Kombinationen von job1, job2,
    deren extrahiertem Geschlecht sowie der Verb-Kategorie, und zählt, wie oft
    jede Kombination im Datensatz vorkommt.

    Parameter:
    ----------
    df : pd.DataFrame
        Ein DataFrame mit den Spalten:
        - 'job1'
        - 'gender_job1_extracted'
        - 'job2'
        - 'gender_job2_extracted'
        - 'verb_category'

    Rückgabe:
    ---------
    pd.DataFrame
        Gruppierter DataFrame mit Spalten:
        - job1
        - gender_job1_extracted
        - job2
        - gender_job2_extracted
        - verb_category
        - count
    """
    # Nur relevante Spalten auswählen
    df_subset = df[[
        "job1", "gender_job1_extracted",
        "job2", "gender_job2_extracted",
        "verb_category"
    ]]

    # Gruppieren und zählen
    grouped_df = (
        df_subset
        .groupby([
            "job1", "gender_job1_extracted",
            "job2", "gender_job2_extracted",
            "verb_category"
        ])
        .size()
        .reset_index(name="count")
    )

    return grouped_df

def compute_gender_percentages_per_job(grouped_df, df_real):
    """
    Berechnet beobachtete und tatsächliche Geschlechterverteilungen je Beruf.

    Schritte:
    1. Aggregiere die Anzahl der Beobachtungen nach job1 und job2 je Geschlecht.
    2. Führe beide Aggregationen zusammen und berechne Prozentwerte.
    3. Ergänze fehlende job × gender-Kombinationen (vollständige Matrix).
    4. Berechne erneut Prozentwerte (inkl. gefüllter NAs mit 0).
    5. Ergänze tatsächliche Verteilung (real percentages) aus df_real.

    Parameter:
    ----------
    grouped_df : pd.DataFrame
        DataFrame mit Spalten:
        - job1, gender_job1_extracted
        - job2, gender_job2_extracted
        - count

    df_real : pd.DataFrame
        DataFrame mit tatsächlichem Frauenanteil je Beruf:
        - 'job'
        - 'percent_female'

    Rückgabe:
    ---------
    pd.DataFrame mit Spalten:
        - job
        - gender
        - count
        - percentage (beobachtet)
        - real_percentage (tatsächlich)
    """

    # 1. Aggregiere job1
    gender_counts_job1_df = (
        grouped_df
        .groupby(["job1", "gender_job1_extracted"])["count"]
        .sum()
        .reset_index()
        .rename(columns={"job1": "job", "gender_job1_extracted": "gender"})
    )

    # 2. Aggregiere job2
    gender_counts_job2_df = (
        grouped_df
        .groupby(["job2", "gender_job2_extracted"])["count"]
        .sum()
        .reset_index()
        .rename(columns={"job2": "job", "gender_job2_extracted": "gender"})
    )

    # 3. Zusammenführen und Summieren
    gender_counts_df = pd.concat([gender_counts_job1_df, gender_counts_job2_df], ignore_index=True)
    gender_counts_df = (
        gender_counts_df
        .groupby(["job", "gender"])["count"]
        .sum()
        .reset_index()
    )

    # ==========================================================================
    # Ergänze alle job × gender-Kombinationen (auch die mit 0 Beobachtungen)
    # ==========================================================================
    all_jobs = df_real["job"].unique()
    all_genders = ["male", "female"]
    full_index = pd.MultiIndex.from_product([all_jobs, all_genders], names=["job", "gender"])
    full_df = pd.DataFrame(index=full_index).reset_index()

    # Mergen mit beobachteten counts
    gender_counts_df = full_df.merge(gender_counts_df, on=["job", "gender"], how="left")
    gender_counts_df["count"] = gender_counts_df["count"].fillna(0)

    # Prozentwerte berechnen
    total_counts = gender_counts_df.groupby("job")["count"].transform("sum")
    gender_counts_df["percentage"] = np.where(
        total_counts > 0,
        gender_counts_df["count"] / total_counts * 100,
        0
    )

    # ==========================================================================
    # Ergänze reale Prozentwerte aus df_real
    # ==========================================================================
    # A) Frauenanteil
    df_real_female = df_real[["job", "percent_female"]].copy()
    df_real_female["gender"] = "female"
    df_real_female = df_real_female.rename(columns={"percent_female": "real_percentage"})

    # B) Männeranteil = 100 - Frauenanteil
    df_real_male = df_real[["job", "percent_female"]].copy()
    df_real_male["gender"] = "male"
    df_real_male["real_percentage"] = 100 - df_real_male["percent_female"]

    # Zusammenführen
    df_real_expanded = pd.concat([df_real_female, df_real_male], ignore_index=True)[
        ["job", "gender", "real_percentage"]
    ]

    # Merge
    gender_counts_df = gender_counts_df.merge(df_real_expanded, on=["job", "gender"], how="left")

    return gender_counts_df


def compute_gender_percentages_per_job_and_verbcategory(grouped_df, df_real):
    """
    Erstellt eine vollständige Matrix aller Kombinationen aus job × gender × verb_category
    mit beobachteten Anteilen sowie den realen Gender-Verteilungen pro Beruf.

    Parameters
    ----------
    grouped_df : pd.DataFrame
        DataFrame mit den Spalten: job1, gender_job1_extracted, job2, gender_job2_extracted, verb_category, count.
        Erwartet wird ein vorher aggregierter DataFrame.

    df_real : pd.DataFrame
        DataFrame mit den Spalten: job, percent_female – enthält reale Genderanteile pro Beruf.

    Returns
    -------
    gender_counts_full : pd.DataFrame
        Enthält für jede Kombination aus job × gender × verb_category:
        - count (beobachtete Häufigkeit)
        - percentage (relativer Anteil je Job+Kategorie)
        - real_percentage (realer Gender-Anteil aus df_real)
    """
    import pandas as pd
    import numpy as np

    # 1. Aggregiere Counts nach job1 (ohne "team"), gender und verb_category
    gender_counts_job1_verb = (
        grouped_df[grouped_df["job1"] != "team"]
        .groupby(["job1", "gender_job1_extracted", "verb_category"])["count"]
        .sum()
        .reset_index()
        .rename(columns={"job1": "job", "gender_job1_extracted": "gender"})
    )

    # 2. Erzeuge vollständige Matrix aller Kombinationen
    jobs = df_real["job"].unique()
    genders = ["female", "male"]
    verb_categories = grouped_df["verb_category"].unique()

    full_index = pd.MultiIndex.from_product(
        [jobs, genders, verb_categories],
        names=["job", "gender", "verb_category"]
    )
    full_df = pd.DataFrame(index=full_index).reset_index()

    # 3. Merge beobachtete Counts mit vollständiger Matrix
    gender_counts_full = full_df.merge(
        gender_counts_job1_verb,
        on=["job", "gender", "verb_category"],
        how="left"
    )
    gender_counts_full["count"] = gender_counts_full["count"].fillna(0)

    # 4. Prozentwerte berechnen pro (job, verb_category)
    total_counts = gender_counts_full.groupby(["job", "verb_category"])["count"].transform("sum")
    gender_counts_full["percentage"] = np.where(
        total_counts > 0,
        gender_counts_full["count"] / total_counts * 100,
        0
    )

    # 5. Reale Werte vorbereiten
    df_real_female = df_real[["job", "percent_female"]].copy()
    df_real_female["gender"] = "female"
    df_real_female = df_real_female.rename(columns={"percent_female": "real_percentage"})

    df_real_male = df_real[["job", "percent_female"]].copy()
    df_real_male["gender"] = "male"
    df_real_male["real_percentage"] = 100 - df_real_male["percent_female"]

    df_real_expanded = pd.concat(
        [df_real_female, df_real_male],
        ignore_index=True
    )[["job", "gender", "real_percentage"]]

    # 6. Merge reale Prozentwerte
    gender_counts_full = gender_counts_full.merge(
        df_real_expanded,
        on=["job", "gender"],
        how="left"
    )

    return gender_counts_full
