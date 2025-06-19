'''from src.data_loader import load_excel_data
from src.sentence_generator import generate_sentences
from src.translator import translate_sentences
from src.evaluator import evaluate_bias'''
import pandas as pd

def main():
    #excel_data = load_excel_data("data/raw/cpsaat10.xlsx")
    df = pd.read_excel("data/raw/cpsaat10.xlsx", skiprows=3)
    df.to_csv("output.csv", index=False)

main()