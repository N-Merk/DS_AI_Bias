import pandas as pd
# Berufe mit hohem Frauenanteil
female_jobs = [
        "Nurse",
        "Kindergarten Teacher",
        "Flight Attendant",
        "Administrative Assistant",
        "Dental Hygienist",
        "Social Worker",
        "Speech Therapist",
        "Librarian",
        "HR Specialist",
        "Primary School Teacher"
    ]
#Prozentual Frauen in diesem Beruf
female_pct = [86.8, 96.8, 77.2, 91.4, 93.9, 79.8, 95.4, 89.2, 76.1, 77.7]

    # Berufe mit hohem Männeranteil
male_jobs = [
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

not_male_pct = [4.3, 11.4, 2.9, 7.9, 20.9, 6.0, 3.2, 14.2, 3.2, 17.2]

    # DataFrames erstellen
df_female = pd.DataFrame({
    "job": female_jobs,
    "percent_female": female_pct
})

df_male = pd.DataFrame({
    "job": male_jobs,
    "percent_female": not_male_pct
})