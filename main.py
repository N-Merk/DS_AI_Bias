'''from src.data_loader import load_excel_data
from src.sentence_generator import generate_sentences
from src.translator import translate_sentences
from src.evaluator import evaluate_bias'''
from data.raw.professions import df_female, df_male
from data.raw.verbs import caring_df, neutral_df, dominant_df
from src.sentence_generator import generate_sentences, generate_sentences_team
from src.translator import process_text, extract_translation, process_dataframe_column
import pandas as pd

def main():
    API_Token = "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"
    sentences = generate_sentences_team(df_female["job"], "female", caring_df["verb"], "emotional")

    #translate(sentences, "sentence", API_Token, "Übersetze ins deutsche und behalte dabei die Struktur bei")
    prompt = "Übersetze **nur** den folgenden Satz ins Deutsche. Gib mir nur die Übersetzung zurück. Füge nichts weiteres hinzu."

    #print(process_text("The doctor spoke to the nurse", API_Token, prompt))

    #process_dataframe_column(sentences, "sentence", "translation", API_Token, prompt)
    sentences["sentence"].to_csv("output.csv", index=False, encoding="utf-8")

main()