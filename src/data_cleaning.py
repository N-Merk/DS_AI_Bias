import pandas as pd
import numpy as np

def add_translations_to_df(df, translated_text, separator, new_columnname="translation"):
    """
    Fügt einem bestehenden DataFrame eine neue Spalte mit übersetzten Sätzen hinzu.

    Die Funktion nimmt einen zusammenhängenden Übersetzungstext, bei dem alle Sätze durch 
    einen bestimmten Separator getrennt sind, und teilt diesen Text in einzelne Sätze auf.
    Anschließend wird jeder übersetzte Satz zeilenweise der neuen Spalte im DataFrame zugeordnet.

    Args:
        df (pandas.DataFrame): Der originale DataFrame mit den Ausgangssätzen.
        translated_text (str): Ein zusammenhängender String mit allen übersetzten Sätzen,
                               getrennt durch den angegebenen Separator.
        separator (str): Das Trennzeichen, mit dem die übersetzten Sätze im String getrennt sind.
        new_columnname (str, optional): Name der neuen Spalte für die Übersetzungen im DataFrame.
                                        Standard ist "translation".

    Returns:
        pandas.DataFrame: Der DataFrame mit der neuen Spalte, in der jede Zeile die passende
                          Übersetzung zum Originalsatz enthält.

    Raises:
        ValueError: Wenn die Anzahl der übersetzten Sätze nicht mit der Anzahl der DataFrame-Zeilen übereinstimmt.
    """

    # Übersetzung anhand Separator aufsplitten
    splitted_translations = translated_text.split(separator)

    # Achtung: Bei Trennzeichen wie ". " kann das letzte Element leer oder mit abschließendem Punkt sein
    # Optional: Trim spaces bei jedem Element
    splitted_translations = [t.strip() for t in splitted_translations if t.strip() != ""]

    print(f"Textlänge Sätze: {len(df)}, Anzahl Separatoren: {translated_text.count(separator)}")

    # Prüfe, ob die Anzahl der Sätze übereinstimmt
    if len(splitted_translations) != len(df):
        # Optional: auffüllen
        if len(splitted_translations) < len(df):
            print("Warnung: Nicht alle Sätze wurden erfolgreich übersetzt. Fülle unübersetzte mit NaN.")
            # Fülle mit NaNs auf
            splitted_translations += [np.nan] * (len(df) - len(splitted_translations))
        elif len(splitted_translations) > len(df):
            print("Warnung: Nicht alle Sätze wurden erfolgreich übersetzt. Schneide überschüssige ab.")
            # Schneide Überschuss ab (sollte eigentlich nie passieren)
            splitted_translations = splitted_translations[:len(df)]

    # Neue Spalte hinzufügen
    df[new_columnname] = splitted_translations

    return df