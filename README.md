# DS_AI_Bias

genderbias_test_project/
│
├── data/
│   ├── raw/                 # Originale Excel-Datei(en)
│   ├── processed/           # Aufbereitete CSVs oder JSONs
│   └── translations/        # Übersetzte Sätze (z.B. als CSV/JSON)
│
├── notebooks/               # Jupyter Notebooks für Explorative Datenanalyse (optional)
│
├── src/                     # Quellcode
│   ├── __init__.py
│   ├── data_loader.py       # Laden und Vorverarbeiten der Excel-Daten
│   ├── sentence_generator.py# Sätze generieren aus Berufsbezeichnungen
│   ├── translator.py        # Schnittstelle zur Übersetzung (z.B. API-Wrapper)
│   ├── evaluator.py         # Auswertung der Bias Tests (Metriken etc.)
│   ├── utils.py             # Hilfsfunktionen (z.B. Logging, Datei-IO)
│
├── tests/                   # Unit-Tests für die Module
│   ├── test_data_loader.py
│   ├── test_sentence_generator.py
│   └── test_translator.py
│
├── requirements.txt         # Python-Abhängigkeiten
├── README.md                # Projektbeschreibung
├── config.yaml              # Konfigurationsdatei (z.B. API-Keys, Pfade)
└── main.py                  # Hauptskript / Pipeline-Runner
