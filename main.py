'''from src.data_loader import load_excel_data
from src.sentence_generator import generate_sentences
from src.translator import translate_sentences
from src.evaluator import evaluate_bias'''
from data.raw.professions import df_female, df_male
from data.raw.verbs import caring_df, neutral_df, dominant_df
from src.sentence_generator import generate_sentences, generate_sentences_team
import pandas as pd

def main():
    #excel_data = load_excel_data("data/raw/cpsaat10.xlsx")
    sentences = generate_sentences_team(df_female["job"], "female", caring_df["verb"], "emotional")
    print(sentences["sentence"])

main()