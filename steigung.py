import pandas as pd

def berechne_durchschnittliche_steigung(df, start_index, end_index, Reihe):
    """
    Berechnet die durchschnittliche Steigung zwischen zwei Indexwerten,
    basierend auf den Werten in der ersten Spalte des DataFrames.
    
    Parameter:
    df -- DataFrame mit mindestens einer Spalte
    start_index -- Startindex für die Berechnung
    end_index -- Endindex für die Berechnung
    Reihe: Wert, der ausgelesen werden soll, ein Wert zwischen 1 und 12
    
    Rückgabe:
    Dictionary mit der Steigung und zusätzlichen Informationen zur Berechnung
    """
    # Werte der angegebenen Spalte auslesen
    Werte = df[Reihe]
    
    start_wert = Werte.iloc[start_index]
    end_wert = Werte.iloc[end_index]
    
    steigung = (end_wert - start_wert) / (end_index - start_index)
    
    return {
        'Name': Reihe,
        'steigung': steigung,
        'start_wert': start_wert,
        'end_wert': end_wert,
        'indexstartwert': start_index,
        'indexendwert': end_index,
        'index_differenz': end_index - start_index,
        'wert_differenz': end_wert - start_wert
    }

def gesamtergebnis_berechnen(delta_ODc, delta_T, dilution, df, volume):
    """
    berechnet das gesamtergebnis der Collagenase Activity.

    Parameter:
    delta_ODc -- Steigung zwischen A und B
    delta_T -- vergangener Zeitraum in Minuten zwischen Zeitpunkt A und B
    dilution -- D (Dilution) innerhalb des Samples. Da 10 µl Sample + 90 µl Assay-Buffer D=0.1. Sollte eine zusätzliche Verdünnung stattgefunden haben (wie Humanase 1:10), dann (ΔOD/ΔT x 0,2 x 0.1)x10
    df -- Sample Dilution Factor
    volume -- sample volume added into the reaction well
    """
    return ((delta_ODc/delta_T)*0.2 * dilution * df)/(0.53*volume)