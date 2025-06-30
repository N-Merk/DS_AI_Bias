from src.translator import process_translation_batch
from src.data_cleaning import add_translations_to_df
import time
import pandas as pd

def generate_df_with_translation(df, new_col_name, prompt, API_Token):
    # Wähle Parameter
    batch_size = 300
    separator = "|||"
    translated_batches = []
    col_name = "sentence"

    # 🔁 Starte Batch-Verarbeitung
    for i in range(0, len(df), batch_size):
        # 1. Slice erstellen
        batch = df.iloc[i:i + batch_size].copy()

        # 2. Übersetzung holen mit process_translation_batch()
        translated_text = process_translation_batch(batch, col_name, API_Token, prompt, separator=separator)

        # 3. Übersetzung dem Batch hinzufügen
        batch = add_translations_to_df(batch, translated_text, separator, new_columnname=new_col_name)

        # 4. Batch speichern
        translated_batches.append(batch)

        # 5. Wartezeit zur Einhaltung des API-Limits
        print(f"Batch {i // batch_size + 1} übersetzt. Warte 20 Sekunden...")
        time.sleep(20)

    # 🔁 6. Alle Batches zusammenfügen
    translated_df = pd.concat(translated_batches, ignore_index=True)
    return translated_df