import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def plot_gender_job_barplot(gender_counts_df, dateipfad_add, plot_suffix ="bei ... Übersetzungsprompt"):

    # Farbpalette
    palette = {"female": "red", "male": "blue"}
    genders = ["female", "male"]
    jobs_sorted = gender_counts_df["job"].unique()

    plt.figure(figsize=(14, 6))

    # A) Extrahierte Werte – gefüllte Balken
    barplot = sns.barplot(
        data=gender_counts_df,
        x="job",
        y="percentage",
        hue="gender",
        palette=palette,
        order=jobs_sorted,
        hue_order=genders,
        dodge=True
    )

    # Mache die Balken transparent(er)
    for patch in barplot.patches:
        patch.set_alpha(0.6)

    # B) Reale Werte – gestrichelte Balken mit Umrandung
    for i, row in gender_counts_df.iterrows():
        xpos = list(jobs_sorted).index(row["job"])
        offset = -0.2 if row["gender"] == "female" else 0.2
        plt.bar(
            xpos + offset,
            row["real_percentage"],
            width=0.4,
            color="none",
            edgecolor=palette[row["gender"]],
            linestyle="--",
            linewidth=1.5,
            label=f"real {row['gender']}" if i < 2 else None  # Nur 1× in Legende
        )

    # Achsen und Layout
    plt.title(f"Gender-Zuweisung pro Beruf {plot_suffix}: extrahiert (gefüllt) vs. real (gestrichelt)")
    plt.ylabel("Anteil (%)")
    plt.xlabel("Beruf")
    plt.xticks(ticks=range(len(jobs_sorted)), labels=jobs_sorted, rotation=45, ha="right")

    # Legende: Duplikate entfernen
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))

    # Deutsche Legendenlabels
    de_labels = {
        "female": "Beobachteter Anteil (Frauen)",
        "male": "Beobachteter Anteil (Männer)",
        "real female": "Tatsächlicher Anteil (Frauen)",
        "real male": "Tatsächlicher Anteil (Männer)"
    }

    plt.legend(by_label.values(), [de_labels[key] for key in by_label.keys()], title="Gender-Zuordnung")

    plt.tight_layout()

    # Speichern
    filename = f"../plots/Histogram_gender_job_{dateipfad_add}_plus_real_percentage.png"
    plt.savefig(filename, dpi=300)
    plt.show()



def plot_gender_distribution_by_job_and_verbcat(
    gender_counts_full_df,
    dateipfad_add="../plots/",
    plot_suffix="bei ... Übersetzungsprompt"
):
    """
    Plottet die prozentuale Gender-Zuweisung nach Beruf + Verbkategorie
    mit Abstand zwischen verschiedenen Berufen und eingezeichneten realen Werten.

    Args:
        gender_counts_full_df (pd.DataFrame): DataFrame mit Spalten
            ["job", "verb_category", "gender", "percentage", "real_percentage"]
        dateipfad_add (str): Pfad zum Speichern
        plot_suffix (str): Zusatztext für den Titel & Dateinamen
        filename (str): Basisdateiname (ohne Endung)
    """
    palette = {"female": "red", "male": "blue"}

    # Erstelle neue numerische y-Positionen mit Lücken
    jobs = gender_counts_full_df["job"].unique()
    job_cat_spaced = []
    y_positions = []
    pos = 0

    #define combination of job and verb_category
    gender_counts_full_df["job_cat"] = gender_counts_full_df["job"] + " | " + gender_counts_full_df["verb_category"]

    for job in jobs:
        job_cats = gender_counts_full_df[gender_counts_full_df["job"] == job]["job_cat"].unique()
        for cat in job_cats:
            job_cat_spaced.append(cat)
            y_positions.append(pos)
            pos += 1
        pos += 1  # Lücke zwischen Berufen

    # Mapping job_cat -> y_pos
    job_cat_to_y = dict(zip(job_cat_spaced, y_positions))

    # Plot Setup
    plt.figure(figsize=(10, 14))
    bar_height = 0.35

    # Balken zeichnen
    for gender_idx, gender in enumerate(["female", "male"]):
        df_gender = gender_counts_full_df[gender_counts_full_df["gender"] == gender]
        x_vals = df_gender["percentage"].values
        y_vals = np.array(df_gender["job_cat"].map(job_cat_to_y).values, dtype=float)
        y_offset = bar_height * (gender_idx - 0.5)

        plt.barh(
            y_vals + y_offset,
            x_vals,
            height=bar_height,
            color=palette[gender],
            alpha=0.6,
            label=gender  # Duplikate in Legende ignorieren wir später
        )

    # Echte Prozentsätze einzeichnen
    for (job, gender), group in gender_counts_full_df.groupby(["job", "gender"]):
        real_val = group["real_percentage"].iloc[0]
        if pd.notna(real_val):
            job_cats = group["job_cat"].tolist()
            y_pos = [job_cat_to_y[cat] for cat in job_cats]
            y_min = min(y_pos) - 0.3
            y_max = max(y_pos) + 0.3

            plt.plot(
                [real_val, real_val],
                [y_min, y_max],
                color=palette[gender],
                linestyle="dashed",
                linewidth=1.2,
                alpha=0.8,
                zorder=0
            )

    # Achsen und Labels
    plt.yticks(ticks=y_positions, labels=job_cat_spaced)
    plt.xlabel("Anteil in Prozent")
    plt.ylabel("Beruf + Verbkategorie")
    plt.title(f"Gender-Zuweisung pro Beruf und Verbgruppe {plot_suffix}")

    # ✨ Legende mit eigenen Handles
    legend_elements = [
        Patch(facecolor="red", alpha=0.6, label="Beobachteter Anteil (Frauen)"),
        Patch(facecolor="blue", alpha=0.6, label="Beobachteter Anteil (Männer)"),
        Line2D([0], [0], color="blue", linestyle="--", label="Tatsächlicher Anteil (Männer)"),
        Line2D([0], [0], color="red", linestyle="--", label="Tatsächlicher Anteil (Frauen)")
    ]

    plt.legend(handles=legend_elements, title="Gender-Zuordnung")

    plt.grid(axis='x', linestyle=':', alpha=0.4)
    plt.tight_layout()

    # Speichern

    full_path = f"../plots/Histogram_gender_job_by_verbcat_{dateipfad_add}_plus_real_percentage.png"
    plt.savefig(full_path, dpi=300)
    plt.show()
