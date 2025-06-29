import pandas as pd


# Funktion zur Generierung von Sätzen aus zwei Job-Listen und Verben
# Die Sätze enthalten Informationen zur Rolle der Berufe, verbale Kategorie und Position im Satz

def generate_sentences(job_list_1, job1_gender, job_list_2, job2_gender, verb_list, verb_category, template="The {subj1} {verb} the {subj2}."):
    sentences = []

    # Iteriere über alle Kombinationen aus Job1, Job2 und Verb
    for job1 in job_list_1:
        for job2 in job_list_2:
            for verb in verb_list:
                # Füge einen Satz hinzu, bei dem job1 das Subjekt ist und job2 das Objekt
                sentences.append({
                    "job1": job1,  # Subjekt im Satz
                    "job2": job2,  # Objekt im Satz
                    "verb": verb,  # verwendetes Verb
                    "verb_category": verb_category,  # Kategorie des Verbs (z. B. dominant, fürsorglich, neutral)
                    "job_gender_1": job1_gender,  # Geschlecht des Subjekts
                    "job_gender_2": job2_gender,  # Geschlecht des Objekts
                    "sentence": template.format(subj1=job1.lower(), verb=verb.lower(), subj2=job2.lower()),  # erzeugter Satz
                    "subject_position": "first"  # Position des Subjekts im Satz (hier: erste Stelle)
                })

    sentences = pd.DataFrame(sentences)
    # Rückgabe der generierten Sätze als pandas DataFrame
    return sentences


def generate_sentences_team(job_list_1, job1_gender, verb_list, verb_category, template="The {subj1} {verb} the {subj2}."):

    # Rückgabe der generierten Sätze als pandas DataFrame
    return generate_sentences(job_list_1, job1_gender, ["team"], "team", verb_list, verb_category, template)