import pandas as pd
import re
import string


def extract_last_article_and_word(text):
    """
    Geht von hinten durch den Satz und sucht den ersten deutschen Artikel (der, die, das).
    Gibt den Artikel und das darauffolgende Wort als pd.Series zurück.
    Falls kein Artikel gefunden wird, gibt sie [None, None] zurück.
    """
    articles = { "der", "die", "das", "den", "dem", "des"}
    words = text.split()

    for i in range(len(words) - 2, -1, -1):
        if words[i].lower() in articles:
            next_word = words[i + 1]
            # Prüfen, ob erstes Zeichen groß ist
            if next_word[0].isupper():
                return pd.Series([words[i], next_word.strip(string.punctuation)])
            else:
                next_word = words[i+2]
                if next_word[0].isupper():
                    return pd.Series([words[i], next_word.strip(string.punctuation)])
                else:
                    return pd.Series([None, None])

    # Wenn kein Artikel gefunden wurde
    return pd.Series([None, None])

def determine_gender_from_ending(word):
    """
    Bestimmt das grammatische Geschlecht eines deutschen Berufsbezeichnungsworts
    nur anhand typischer Wortendungen.
    """
    word = word.lower()

    if word == "team":
        return "team"

    # Weibliche Endungen
    female_endings = ["in", "erin", "schwester"]
    # Männliche Endungen
    male_endings = ["er", "eur", "iker", "or", "ist", "ent", "ingenieur", "arbeiter", "spezialisten", "chef",
                    "polizisten", "bibliothekar", "logopäden", "referenten"]
    # Neutrale Endungen (selten)
    neutral_endings = ["chen", "lein", "um"]

    for ending in female_endings:
        if word.endswith(ending):
            return "female"

    for ending in male_endings:
        if word.endswith(ending):
            return "male"

    for ending in neutral_endings:
        if word.endswith(ending):
            return "neutral"

    return "unknown"

def determine_gender_from_article(article: str) -> str:
    """
    Bestimmt das Geschlecht anhand des deutschen Artikels.
    """
    if not isinstance(article, str):
        return "unknown"

    article = article.strip().lower()

    if article == "die":
        return "female"
    elif article == "der":
        return "male"
    elif article == "das":
        return "neutral"
    else:
        return "unknown"

def get_gender_Spezialfall(article, noun):
    female_combinations = {
        ("die", "verwaltungsangestellte"),
        ("der", "verwaltungsangestellten"),
        ("die", "zahnmedizinische")
    }

    male_combinations = {
        ("den", "verwaltungsangestellten"),
        ("dem", "verwaltungsangestellten")
    }

    if (article.lower(), noun.lower()) in female_combinations:
        return "female"
    elif (article.lower(), noun.lower()) in male_combinations:
        return "male"
    else:
        return "unknown"



def extract_genders_from_translation(csv_path: str, translation_col: str):
    """
    Extrahiert das Geschlecht von job1 und job2 aus der deutschen Übersetzung,
    berücksichtigt dabei nominative und akkusative Artikel und typische Endungen.
    """
    df = pd.read_csv(csv_path)

    # Führende Leerzeichen entfernen
    df[translation_col] = df[translation_col].str.lstrip()

    # Erste zwei Wörter extrahieren: Artikel1 und Job1
    df[['article1', 'job1_word']] = df[translation_col].str.split(n=2, expand=True)[[0, 1]]

    # Vorletztes und letztes Wort extrahieren: Artikel2 und Job2
    df[['article2', 'job2_word']] = df[translation_col].apply(extract_last_article_and_word)

    gender_job1 = []
    for article1, job1_word in zip(df['article1'], df['job1_word']):
        gender_end = determine_gender_from_ending(job1_word)
        gender_art = determine_gender_from_article(article1)

        if gender_end != "unknown":
            gender_job1.append(gender_end)
        elif gender_art != "unknown":
            gender_job1.append(gender_art)
        else:
            gender_job1.append(gender_art)
            print(f"Unbekanntes Gender für Job1: Artikel='{article1}', Wort='{job1_word}'")

    gender_job2 = []
    for article2, job2_word in zip(df['article2'], df['job2_word']):
        gender_end = determine_gender_from_ending(job2_word)
        special_gender = get_gender_Spezialfall(article2, job2_word)

        if gender_end != "unknown":
            gender_job2.append(gender_end)
        elif special_gender != "unknown":
            gender_job2.append(special_gender)
        else:
            gender_job2.append(gender_end)
            print(f"Unbekanntes Gender für Job2: Artikel='{article2}', Wort='{job2_word}'")

    df["gender_job1_extracted"] = gender_job1
    df["gender_job2_extracted"] = gender_job2

    return df

