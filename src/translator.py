import pandas as pd
import requests
import time

def process_text(text, api_token, prompt_instruction):
    """
        Sendet einen Text zusammen mit einer Prompt-Anweisung an das Hugging Face Modell
        und gibt die vollständige generierte Antwort zurück.

        Parameter:
            text (str): Der zu übersetzende Satz
            prompt_instruction (str): Die Anweisung an das Modell (z. B. "Übersetze nur den Satz...")
            api_token (str): Dein Hugging Face API-Token

        Rückgabe:
            str: Die vollständige Textantwort des Modells (inkl. Prompt und ggf. zusätzlichem Output)
        """

    API_TOKEN = api_token
    #API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

    # Funktion zur Anfrage an das Hugging Face Modell
    prompt = f"[INST]{prompt_instruction}\n\n{text}[/INST]"
    payload = {"inputs": prompt, "parameters": {"return_full_text": False}}

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    # Warte, falls Modell noch nicht bereit (503)
    while response.status_code == 503:
        print("Warte auf freien Modell-Server...")
        time.sleep(5)
        response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()
        # Antwort parsen (erwartet: Liste mit Dict und 'generated_text')
        if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
            return result[0]['generated_text']
        else:
            print("Unerwartete Antwortstruktur:", result)
            return None
    else:
        print(f"Fehler {response.status_code}: {response.text}")
        return None


def extract_translation(response_text):
    """
    Extrahiert aus der vollständigen Modellantwort nur die tatsächliche Übersetzung,
    indem die letzte nicht-leere Zeile verwendet wird.

    Parameter:
        response_text (str): Die Rückgabe von `translate_text`

    Rückgabe:
        str: Die reine Übersetzung des Satzes
    """
    if not response_text:
        return None

    # Entferne leere Zeilen und führende/abschließende Leerzeichen
    lines = [line.strip() for line in response_text.strip().split("\n") if line.strip()]

    # Die letzte nicht-leere Zeile ist in der Regel die reine Übersetzung
    return lines[-1] if lines else None


def process_dataframe_column(df, input_col, output_col, api_token, prompt_instruction):
    """
    Sendet die Inhalte einer Spalte eines DataFrames jeweils einzeln zusammen mit einer Prompt-Anweisung
    an ein Hugging Face Sprachmodell und speichert die resultierende Antwort (z. B. Übersetzung oder Transformation)
    in einer neuen Spalte.

    Parameter:
        df (pd.DataFrame): Der DataFrame mit den zu verarbeitenden Texten
        input_col (str): Der Spaltenname mit den Eingabetexten
        output_col (str): Der gewünschte Spaltenname für die Modellantworten
        api_token (str): Hugging Face API-Token
        prompt_instruction (str): Die Anweisung, die das Modell ausführen soll
                                  (z. B. "Übersetze den Satz", "Formuliere höflicher", etc.)

    Rückgabe:
        pd.DataFrame: Der ursprüngliche DataFrame mit einer zusätzlichen Spalte mit den Modellantworten
    """
    translations = []

    for index, row in df.iterrows():
        text = row[input_col]
        print(f"Verarbeite Zeile {index + 1}/{len(df)}: {text}")

        # Kombinierte Eingabe an das Modell senden
        full_response = process_text(text, api_token, prompt_instruction)

        # Nur die relevante Ausgabe extrahieren (letzte Zeile)
        result = full_response#extract_translation(full_response)

        # Speichern der Ausgabe
        translations.append(result)

        # Kurze Pause zur Vermeidung von Rate Limits (optional)
        time.sleep(1)

    # Neue Spalte mit den Modellantworten hinzufügen
    df[output_col] = translations