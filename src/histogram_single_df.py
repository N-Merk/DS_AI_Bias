import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_gender_job_barplot(gender_counts_df, dateipfad_add, plot_suffix):

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