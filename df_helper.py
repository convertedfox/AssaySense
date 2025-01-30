import pandas as pd

def excel_aufbereiten(df):
    """Filtert die Zeilen, die Buchstaben von A-H in der Spalte 'Raw data' enthalten.
    Bereinigt die Excel-Daten durch Entfernen leerer Spalten und Zeilen."""
    df = df[df['Raw data'].str.match(r'^[A-H]$', na=False)].reset_index(drop=True)
    df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
    
    condition = df.iloc[:, 2:].isna().all(axis=1)
    # Zeilen löschen, bei denen die Bedingung erfüllt ist: Leere Zeilen, die keinen Wert haben ab der 3.Spalte
    df= df[~condition]
    return df

def blank_subratct(df):
    # Die letzten Spaltenwerte pro Zeile bestimmen
    last_column = df.iloc[:, -1]  # Letzte Spalte

    # Werte ab Spalte 3 bis vorletzte Spalte reduzieren
    df.iloc[:, 2:-1] = df.iloc[:, 2:-1].sub(last_column, axis=0)
    return df

def calculate_mean_for_pairs(df):
    """Berechnet den Mittelwert für jedes Buchstabenpaar (z. B. A/B, C/D).
    Am Ende werden die Spalten noch umbenannt.
    """
    # Identifiziere eindeutige Buchstaben
    unique_letters = df['Raw data'].unique()
    # Erstelle Paare (A-B, C-D, etc.)
    letter_pairs = [(unique_letters[i], unique_letters[i + 1]) for i in range(0, len(unique_letters), 2)]

    # Ergebnis-DataFrame
    mean_dataframes = []

    for pair in letter_pairs:
        # Wähle die entsprechenden Zeilen für das Paar aus
        df_1 = df[df['Raw data'] == pair[0]].iloc[:, 1:]  # Werte für den ersten Buchstaben
        df_2 = df[df['Raw data'] == pair[1]].iloc[:, 1:]  # Werte für den zweiten Buchstaben

        # Stelle sicher, dass alle Werte numerisch sind
        df_1 = df_1.apply(pd.to_numeric, errors='coerce')
        df_2 = df_2.apply(pd.to_numeric, errors='coerce')

        # Angleich der Zeilenanzahl durch Trimmen auf die kleinste Anzahl von Zeilen
        min_len = min(len(df_1), len(df_2))
        df_1 = df_1.iloc[:min_len, :]
        df_2 = df_2.iloc[:min_len, :]

        # Berechne den Mittelwert
        mean_df = (df_1.values + df_2.values) / 2
        mean_df = pd.DataFrame(mean_df, columns=df_1.columns)

        # Füge eine Spalte hinzu, um das Paar zu identifizieren
        mean_df.insert(0, 'Raw data', f'Mean {pair[0]}/{pair[1]}')
        # Speichere das Ergebnis
        mean_dataframes.append(mean_df)

    # Kombiniere alle Ergebnisse in einem DataFrame
    result_df = pd.concat(mean_dataframes, ignore_index=True)
    
    # Indexspalte hinzufügen
    result_df["Zeitwert"] = result_df.groupby("Raw data").cumcount()
    spalte = result_df.pop("Zeitwert") # Spalte entfernen und speichern
    result_df.insert(0, "Zeitwert", spalte) # Spalte an erster Stelle einfügen

    # Spalten umbenennen
    result_df = result_df.rename(columns={
    "Unnamed: 1": "negative control",
    "Unnamed: 2": "positive control",
    "Unnamed: 3": "Humanase H",
    "Unnamed: 4": "zz55",
    "Unnamed: 5": "zz58",
    "Unnamed: 6": "zz60",
    "Unnamed: 7": "zz62",
    "Unnamed: 8": "zz63",
    })

    # Letzte Spalte umbenennen
    result_df.columns.values[-1] = "blank"

    return result_df