from data.raw.professions import df_female, df_male
from data.raw.verbs import caring_df, neutral_df, dominant_df
from src.sentence_generator import generate_sentences, generate_sentences_team
import pandas as pd

def generate_whole_dataframe():
    """
    Generiert einen vollständigen DataFrame mit Sätzen basierend auf Kombinationen von:
    - Geschlecht des Subjekts (job1)
    - Geschlecht des Objekts (job2)
    - Verbtypen (caring, neutral, dominant)

    Für jede Kombination werden:
    1. Sätze generiert, bei denen ein Subjekt (job1) ein Team adressiert → `generate_sentences_team`
    2. Sätze generiert, bei denen ein Subjekt (job1) ein Objekt (job2) adressiert → `generate_sentences`

    Die Jobs und Verben werden dabei aus globalen DataFrames bezogen, z. B.:
        - df_female, df_male
        - caring_df, neutral_df, dominant_df

    Rückgabe:
        pandas.DataFrame: Ein gemischter (geshuffelter) DataFrame aller generierten Sätze mit den Spalten:
            - job1, job2 (optional), verb, verb_category, job_gender_1, job_gender_2, sentence, subject_position
    """

    all_dfs = []

    for gender in ["male", "female"]:
        for verb_type in ["caring", "neutral", "dominant"]:
            # Hole Jobliste für das Subjekt basierend auf Geschlecht
            job_list_1 = globals()[f"df_{gender}"]["job"].tolist()

            # Hole Liste der Verben für die aktuelle Kategorie
            verb_list = globals()[f"{verb_type}_df"]["verb"].tolist()

            # Generiere Sätze, bei denen das Subjekt ein Team adressiert
            df = generate_sentences_team(job_list_1, gender, verb_list, verb_type)
            all_dfs.append(df)

            # Erzeuge Kombinationen mit beiden Objekt-Geschlechtern
            for gender2 in ["male", "female"]:
                # Hole Jobliste für das Objekt basierend auf Geschlecht
                job_list_2 = globals()[f"df_{gender2}"]["job"].tolist()

                # Generiere Sätze, bei denen job1 das Subjekt und job2 das Objekt ist
                df = generate_sentences(job_list_1, gender, job_list_2, gender2, verb_list, verb_type)
                all_dfs.append(df)

    # Füge alle Einzeldatenframes zusammen, mische die Reihenfolge zufällig und resette den Index
    return pd.concat(all_dfs, ignore_index=True).sample(frac=1).reset_index(drop=True)
