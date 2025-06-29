import pandas as pd
import requests
import time
import google.generativeai as genai


def process_text_with_gemini(text, api_key, prompt_instruction):
    """
    Sendet einen Text zusammen mit einer Prompt-Anweisung an das Google Gemini Modell
    und gibt die generierte Antwort zurück.

    Parameter:
        text (str): Der zu verarbeitende Satz
        api_key (str): Dein Google Gemini API-Schlüssel
        prompt_instruction (str): Die Anweisung an das Modell (z.B. "Übersetze nur den Satz...")

    Rückgabe:
        str: Die vollständige Textantwort des Modells
    """
    if not api_key:
        print("Fehler: Der Gemini API-Schlüssel wurde nicht bereitgestellt.")
        return None

    genai.configure(api_key=api_key)

    # Für die größtmöglichen Free Tokens und eine gute Balance zwischen Geschwindigkeit und Leistung
    # empfehlen wir "gemini-1.5-flash" oder "gemini-1.5-pro".
    # "gemini-1.5-flash" hat in der Regel die höchsten Ratenlimits im Free Tier.
    # Google benennt Modelle manchmal um oder führt neue Versionen ein,
    # daher ist es gut, die offizielle Dokumentation zu prüfen,
    # aber zum Zeitpunkt 2025-06 ist Flash die gängige Empfehlung für Free Tier.
    model_name = 'gemini-1.5-flash'  # Dies ist die Version mit einem sehr großzügigen Free Tier.

    model = genai.GenerativeModel(model_name)

    try:
        # Die Prompt-Anweisung und der Text werden in einer einzigen Nachricht kombiniert.
        full_prompt = f"{prompt_instruction}\n\n{text}"

        # Sende die Anfrage an das Modell
        response = model.generate_content(full_prompt)

        # Die Antwort von Gemini kann komplex sein. Wir extrahieren den Text.
        if response.candidates:
            if response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                print("Gemini hat keine Textantwort generiert.")
                print(f"Raw Response: {response}") # Optional: Für Debugging die gesamte Antwort ausgeben
                return None
        else:
            print("Gemini hat keine Kandidaten in der Antwort zurückgegeben.")
            print(f"Raw Response: {response}") # Optional: Für Debugging die gesamte Antwort ausgeben
            return None

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        # Wenn du detailliertere Fehler möchtest, kannst du hier response.result ausgeben,
        # falls es eine Fehlermeldung enthält, die nicht als Exception geworfen wird.
        return None


def join_sentences(df, col_name, separator="-"):
    """
    Verbindet alle Sätze einer Spalte eines DataFrames zu einem einzigen Text.

    Parameter:
    - df: pandas DataFrame
    - col_name: Name der Spalte mit den Sätzen
    - separator: Zeichenkette zur Trennung der Sätze (z. B. ' ', '\n', ' ||| ')

    Rückgabe:
    - Ein String mit allen Sätzen aneinandergereiht
    """
    # NaN-Werte ignorieren, sicherstellen dass alle Werte Strings sind
    sentences = df[col_name].dropna().astype(str)
    return separator.join(sentences)


def process_translation_batch(df_batch, col_name, api_token, prompt, separator="-"):
    """
    Übersetzt eine Teilmenge eines DataFrames mit Sätzen über die Gemini API.

    Die Funktion nimmt einen DataFrame-Batch, extrahiert die Sätze aus der 'sentence'-Spalte,
    verbindet sie mithilfe eines Separators zu einem einzigen String, und sendet diesen
    zur Übersetzung an die Gemini API. Die Rückgabe ist der zusammenhängende übersetzte Text.

    Args:
        df_batch (pandas.DataFrame): Ein Teil-DataFrame mit einer Spalte 'sentence',
                                     die die zu übersetzenden englischen Sätze enthält.
        api_token (str): Der API-Token für die Authentifizierung bei der Gemini API.
        prompt (str): Der Prompt, der der API mitgegeben wird (z. B. "Übersetze die folgenden Sätze ...").
        separator (str, optional): Trennzeichen zwischen den Sätzen im Anfrage-String.
                                   Muss beim Aufsplitten der Rückgabe konsistent verwendet werden.

    Returns:
        str: Ein einziger String, der alle übersetzten Sätze enthält, getrennt durch das übergebene Separator-Zeichen.

    Raises:
        Exception: Wenn der API-Aufruf fehlschlägt oder ein anderer Fehler auftritt.
    """
    text = join_sentences(df_batch, col_name, separator)
    translated_text = process_text_with_gemini(text, api_token, prompt)
    return translated_text

