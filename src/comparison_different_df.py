import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from src.data_preperation import group_verb_assignments, compute_gender_percentages_per_job


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_gender_distribution_comparison(datasets: dict, df_real, dateipfad_add):
    """
    Vergleichsplot der beobachteten und tatsächlichen Genderverteilungen pro Job
    für mehrere Datensätze.
    """
    all_frames = []

    for label, df in datasets.items():
        grouped = group_verb_assignments(df)
        gender_df = compute_gender_percentages_per_job(grouped, df_real)
        gender_df["dataset"] = label
        all_frames.append(gender_df)

    df_plot = pd.concat(all_frames, ignore_index=True)

    # Definiere Reihenfolge
    jobs = [
        "Nurse",
        "Kindergarten Teacher",
        "Flight Attendant",
        "Administrative Assistant",
        "Dental Hygienist",
        "Social Worker",
        "Speech Therapist",
        "Librarian",
        "HR Specialist",
        "Primary School Teacher",
        "Construction Worker",
        "Mechanical Engineer",
        "Electrician",
        "Truck Driver",
        "Software Developer",
        "Welder",
        "Car Mechanic",
        "Police Officer",
        "Plumber",
        "Civil Engineer"
    ]

    #jobs = sorted(df_plot["job"].unique())
    x = np.arange(len(jobs))

    genders = ["female", "male"]
    datasets_order = list(datasets.keys())
    total_bars = len(datasets_order) * len(genders)
    bar_width = 0.8 / total_bars  # Gesamtbreite auf 80% begrenzt

    fig, ax = plt.subplots(figsize=(22, 8))

    # Deutlich unterscheidbare Farben
    color_map = {
        ("neutral", "female"): "#e41a1c",
        ("neutral", "male"): "#377eb8",
        ("feminist", "female"): "#fb8072",
        ("feminist", "male"): "#80b1d3",
        ("incel", "female"): "#f781bf",
        ("incel", "male"): "#4daf4a",
        ("female", "female"): "#fbb4ae",
        ("female", "male"): "#b3cde3",
        ("male", "female"): "#decbe4",
        ("male", "male"): "#ccebc5",
    }

    # Plot der Balken
    for i, (dataset, gender) in enumerate([(d, g) for d in datasets_order for g in genders]):
        subset = (
            df_plot[(df_plot["dataset"] == dataset) & (df_plot["gender"] == gender)]
            .set_index("job")
            .loc[jobs]
            .reset_index()
        )
        offset = (i - total_bars / 2) * bar_width + bar_width / 2

        ax.bar(
            x + offset,
            subset["percentage"],
            width=bar_width,
            label=f"{dataset.title()} ({'w' if gender == 'female' else 'm'})",
            color=color_map[(dataset, gender)],
            edgecolor="black",
            alpha=0.9
        )

    # Tatsächliche Werte (Linien)
    real_data = df_plot[df_plot["dataset"] == datasets_order[0]]
    for gender, linestyle, color in zip(
        ["female", "male"],
        ["--", "--"],
        ["#990000", "#003366"]
    ):
        real = (
            real_data[real_data["gender"] == gender]
            .set_index("job")
            .loc[jobs]
            .reset_index()
        )
        ax.plot(
            x,
            real["real_percentage"],
            linestyle=linestyle,
            color=color,
            linewidth=2.5,
            label=f"Tatsächlich ({'w' if gender == 'female' else 'm'})",
            alpha=0.7
        )

    ax.set_xticks(x)
    ax.set_xticklabels(jobs, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Anteil in %")
    ax.set_title("Beobachtete vs. tatsächliche Genderverteilung pro Beruf", fontsize=14)
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle=":", alpha=0.5)

    # Legende aufräumen
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), title="Gender-Zuordnung", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.tight_layout()

    # Speichern
    filename = f"../plots/Histogram_gender_job_comparison_{dateipfad_add}_plus_real_percentage.png"
    plt.savefig(filename, dpi=300)

    plt.show()

