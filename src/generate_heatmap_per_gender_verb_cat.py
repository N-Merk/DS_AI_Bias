import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_heatmap_per_gender_verb_cat_job1(df, name_df, addprompt="bei neutralem Übersetzungsprompt"):
    df["comparison_group1"] = df["verb_category"] + "_" + df["gender_job2_extracted"]
    # Gruppieren und den Anteil von job1 == "female" berechnen
    pivot_df = (
        df.groupby(["job1", "comparison_group1"])
        .apply(lambda x: (x["gender_job1_extracted"] == "female").mean() * 100)
        .reset_index(name="percent_female")
    )

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

    # Pivot für Heatmap-Plot
    heatmap_data = pivot_df.pivot(index="job1", columns="comparison_group1", values="percent_female")
    heatmap_data = heatmap_data.loc[jobs]  # sortiere Zeilen

    # Plot
    plt.figure(figsize=(14, 8))
    sns.heatmap(
        heatmap_data,
        annot=True,
        cmap="Reds",
        fmt=".1f",
        linewidths=0.5,
        cbar_kws={'label': 'Anteil weiblich (%)'}
    )

    plt.title(f"Gender-Zuweisung für job1 nach Verbkategorie & übersetztem Gender von job2 bei {addprompt} Übersetzungsprompt")
    plt.xlabel("Vergleichsgruppe (Verb + Gender von job2)")
    plt.ylabel("Job1 (Zielberuf)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    filename = f"../plots/Heatmap_gender_job1_per_job2_verbcat_{name_df}.png"
    plt.savefig(filename, dpi=300)
    plt.show()

def generate_heatmap_per_gender_verb_cat_job2(df, name_df, addprompt="bei neutralem Übersetzungsprompt"):
    df["comparison_group2"] = df["verb_category"] + "_" + df["gender_job1_extracted"]
    # Gruppieren und den Anteil von job1 == "female" berechnen
    pivot_df = (
        df.groupby(["job2", "comparison_group2"])
        .apply(lambda x: (x["gender_job2_extracted"] == "female").mean() * 100)
        .reset_index(name="percent_female")
    )

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

    # Pivot für Heatmap-Plot
    heatmap_data = pivot_df.pivot(index="job2", columns="comparison_group2", values="percent_female")
    heatmap_data = heatmap_data.loc[jobs]  # sortiere Zeilen

    # Plot
    plt.figure(figsize=(14, 8))
    sns.heatmap(
        heatmap_data,
        annot=True,
        cmap="Reds",
        fmt=".1f",
        linewidths=0.5,
        cbar_kws={'label': 'Anteil weiblich (%)'}
    )

    plt.title(f"Gender-Zuweisung für job2 nach Verbkategorie & übersetztem Gender von job1 bei {addprompt} Übersetzungsprompt")
    plt.xlabel("Vergleichsgruppe (Verb + Gender von job1)")
    plt.ylabel("Job1 (Zielberuf)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    filename = f"../plots/Heatmap_gender_job2_per_job1_verbcat_{name_df}.png"
    plt.savefig(filename, dpi=300)
    plt.show()