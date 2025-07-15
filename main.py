
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
    print(df_female)
    print(df_male)

main()