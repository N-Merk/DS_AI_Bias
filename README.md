# DS_AI_Bias

genderbias_test_project/
│
├── data/
│ ├── raw/ # Rohdaten (Original Excel-Dateien mit Berufsbezeichnungen)
│ ├── processed/ # Aufbereitete Daten (z.B. CSV, JSON)
│ └── translations/ # Übersetzte Sätze (z.B. Deutsch)
│
├── notebooks/ # Jupyter Notebooks für explorative Datenanalyse und Tests
│
├── src/ # Quellcode des Projekts
│ ├── init.py
│ ├── data_loader.py # Modul zum Laden und Vorverarbeiten der Excel-Daten
│ ├── sentence_generator.py# Erzeugt Sätze aus Berufsbezeichnungen
│ ├── translator.py # Schnittstelle zur Übersetzung (z.B. API oder lokale Lösung)
│ ├── evaluator.py # Auswertung und Analyse der Genderbias-Tests
│ ├── utils.py # Hilfsfunktionen (z.B. Dateioperationen, Logging)
│
├── tests/ # Unit-Tests für die Module im src-Ordner
│ ├── test_data_loader.py
│ ├── test_sentence_generator.py
│ └── test_translator.py
│
├── requirements.txt # Abhängigkeiten des Projekts
├── config.yaml # Konfigurationsdatei (z.B. Pfade, API-Schlüssel)
├── main.py # Hauptskript zum Ausführen der gesamten Pipeline
└── README.md # Projektbeschreibung und Anleitung
