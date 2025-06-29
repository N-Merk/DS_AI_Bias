'''from src.data_loader import load_excel_data
from src.sentence_generator import generate_sentences
from src.translator import translate_sentences
from src.evaluator import evaluate_bias'''
from data.raw.professions import df_female, df_male
from data.raw.verbs import caring_df, neutral_df, dominant_df
from src.sentence_generator import generate_sentences, generate_sentences_team
from src.translator import process_text_with_gemini, join_sentences, process_translation_batch
from src.data_cleaning import add_translations_to_df
from src.dataframe_generator import generate_whole_dataframe
import pandas as pd
import time
from dotenv import load_dotenv
import os


def main():

    API_Token = os.getenv("GEMINI_API_KEY")
    print("Geladener API-Key:", API_Token)


    sentences = generate_whole_dataframe()

    # Wähle Parameter
    batch_size = 300
    separator = "-"
    translated_batches = []

    # 🧠 PROMPT definieren – beachte: keine zusätzliche Formatierung!
    prompt = "Übersetze die folgenden Sätze ins Deutsche. Gib mir nur die Übersetzung zurück. Füge nichts weiteres hinzu."

    # 🔁 Starte Batch-Verarbeitung
    for i in range(0, len(sentences), batch_size):

        # 1. Slice erstellen
        batch = sentences.iloc[i:i + batch_size].copy()

        # 2. Übersetzung holen mit process_translation_batch()
        translated_text = process_translation_batch(batch, API_Token, prompt, separator=separator)

        # 3. Übersetzung dem Batch hinzufügen
        batch = add_translations_to_df(batch, translated_text, separator, new_columnname="translation")

        # 4. Batch speichern
        translated_batches.append(batch)

        # 5. Wartezeit zur Einhaltung des API-Limits
        print(f"Batch {i // batch_size + 1} übersetzt. Warte 60 Sekunden...")
        time.sleep(60)

    # 🔁 6. Alle Batches zusammenfügen
    translated_df = pd.concat(translated_batches, ignore_index=True)

    # 💾 7. Optional: Speichern
    translated_df.to_csv("uebersetzte_saetze.csv", index=False)
main()