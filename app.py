import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from df_helper import excel_aufbereiten, calculate_mean_for_pairs, blank_subratct
from plot_helper import zeichnung_erstellen
from steigung import berechne_durchschnittliche_steigung, gesamtergebnis_berechnen
import pandas as pd

# Initialisierung des Session-States
if "result_df" not in st.session_state:
    st.session_state.result_df = None

if "messpaare" not in st.session_state:
    st.session_state.messpaare = None

if "uploaded_excel" not in st.session_state:
    st.session_state.uploaded_excel = None

if "zeichnungsdf" not in st.session_state:
    st.session_state.zeichnungsdf = None

Titel = "AssaySense 1.0"
###################################################
st.set_page_config(
    page_title= Titel,
    page_icon= "🧬",
    layout="wide"
)

print("\x1b[1;92mStreamlit script running...\x1b[0m")
st.image("banner.jpg", width=800)

# UI
st.header(Titel)
st.markdown(
    """
Dieses kleine Programm soll helfen, Kollagensase-Daten aufzubereiten und auszuwerten.

**ToDo:**

✅ Blank abziehen (immer den Wert in der letzten Spalte abziehen von allen Werten in derselben Spalte)

✅ Steigung zur Verfügung stellen

❓ Werte überprüfen


"""
)

st.subheader("Excel hochladen")
st.markdown(
    """
Die Excel muss bitte immer dasselbe Format haben.
Im Demo-Modus wird mit einer vorgefertigten Demo-Datei gearbeitet; damit man sich einen Eindruck machen kann.        
Im anderen Modus kann eine eigene Liste hochgeladen werden.
"""
)

modus = st.radio('Welcher Modus?', ['Demo','Eigene Excel'])
if modus == "Eigene Excel":
    st.session_state.uploaded_excel = st.file_uploader("Wählen Sie eine Excel-Datei aus", type="xlsx")
else:
    st.session_state.uploaded_excel = ("./Demo.xlsx")

st.subheader("Auswertungsparameter festlegen")

if st.button("Daten analysieren"):
    try:
        # Daten einlesen
        df = pd.read_excel(st.session_state.uploaded_excel, "Magellan Pro Sheet 1")

        # Excel-Daten aufbereiten
        df_clean = excel_aufbereiten(df)

        # Mittelwerte berechnen
        result_df = calculate_mean_for_pairs(df_clean)
        st.session_state["result_df"] = result_df

        # Blank abziehen
        result_df = blank_subratct(result_df)
        st.session_state["result_df"] = result_df

        # Messpaare bestimmen
        st.session_state["messpaare"] = result_df["Raw data"].unique().tolist()
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {str(e)}")
        st.error("Bitte stellen Sie sicher, dass die hochgeladenen Dateien gültig sind!")

if st.session_state.result_df is not None:
    st.subheader("Auswertung")
    st.markdown(
        """
        Diese Daten wurden erkannt:
        """
        )
    st.dataframe(st.session_state.result_df)

if st.session_state.messpaare is not None:
    st.subheader("Grafik parametrisieren")
    Messpaar = st.selectbox("Welche Messpaare sollen dargestellt werden?", st.session_state.messpaare, index = 0)

    try:
        if st.session_state["result_df"] is not None:
            zeichnungsdf = zeichnung_erstellen(st.session_state["result_df"], Messpaar)
            st.session_state.zeichnungsdf = zeichnungsdf
            st.line_chart(st.session_state.zeichnungsdf)
        else:
            st.error("Keine Daten vorhanden. Bitte zuerst 'Daten analysieren' ausführen.")
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

if st.session_state.zeichnungsdf is not None:
    st.subheader("Steigung ermitteln")
    reihe = st.selectbox("Auf welchem Graph soll eine Steigung ermittelt werden?",  st.session_state.zeichnungsdf.columns[0:].tolist())
    start_value, end_value = st.slider(
        'Wähle einen Bereich',
        min_value=0,
        max_value=180,
        value=(25, 75)  # Standardwerte für Start- und Endpunkt
    )
    steigungsergebnis = berechne_durchschnittliche_steigung(st.session_state.zeichnungsdf, start_value, end_value, reihe)
    st.markdown(f"""
        Die **Steigung** für {reihe} zwischen Minute {start_value} und Minute {end_value} beträgt `{steigungsergebnis['steigung']:.6f}` pro Minute.
        
        **Startwert** bei Minute {steigungsergebnis['indexstartwert']}: `{steigungsergebnis['start_wert']:.6f}`

        **Endwert** bei Minute {steigungsergebnis['indexendwert']}: `{steigungsergebnis['end_wert']:.6f}`
    """)
    st.subheader("Auswertung und Erklärung")
   #  st.image("Grafik Formel.png", width=400)
    st.markdown("Die allgemeine Formel lautet:")
    st.markdown(r"$$\text{Collagenase Activity } \left[\frac{U}{ml}\right] = \left[\frac{U}{ml}\right] = \frac{((\Delta ODc / \Delta T) \times 0.2 \times D) \times DF}{0.53 \times V}$$")
    delta_ODc = round(steigungsergebnis['wert_differenz'], 6)
    delta_T = end_value - start_value 
    dilution = 0.1    # Beispielwert
    df = 10           # Beispielwert
    volume = 0.1      # Beispielwert
    ergebnis= ((delta_ODc/delta_T)*0.2 * dilution * df)/(0.53*volume)
    # Formel mit dynamischen Werten
    st.markdown("Nun setzen wir die Werte ein:")
    formula = rf"""
    $$\text{{Collagenase Activity }} \left[\frac{{U}}{{ml}}\right] = \left[\frac{{U}}{{ml}}\right] = \frac{{(({delta_ODc} / {delta_T}) \times 0.2 \times {dilution}) \times {df}}}{{0.53 \times {volume}}} = {ergebnis}$$
    """
    st.markdown(formula)

    # Ergebnis-Tabelle in Streamlit anzeigen
    st.subheader("Ergebnis-Tabelle")
    falgpa_humanase_h = berechne_durchschnittliche_steigung(st.session_state.zeichnungsdf, start_value, end_value,"Humanase H")
    falgpa_humanase_h_ergebnis= gesamtergebnis_berechnen(falgpa_humanase_h['wert_differenz'], falgpa_humanase_h['index_differenz'], dilution, df, volume)
    
    falgpa_ZZ55 = berechne_durchschnittliche_steigung(st.session_state.zeichnungsdf, start_value, end_value,"zz55")
    falgpa_ZZ55_ergebnis = gesamtergebnis_berechnen(falgpa_ZZ55['wert_differenz'], falgpa_ZZ55['index_differenz'], dilution, df, volume)

    falgpa_ZZ58 = berechne_durchschnittliche_steigung(st.session_state.zeichnungsdf, start_value, end_value,"zz58")
    falgpa_ZZ58_ergebnis = gesamtergebnis_berechnen(falgpa_ZZ58['wert_differenz'], falgpa_ZZ58['index_differenz'], dilution, df, volume)

    falgpa_ZZ60 = berechne_durchschnittliche_steigung(st.session_state.zeichnungsdf, start_value, end_value,"zz60")
    falgpa_ZZ60_ergebnis = gesamtergebnis_berechnen(falgpa_ZZ60['wert_differenz'], falgpa_ZZ60['index_differenz'], dilution, df, volume)

    falgpa_ZZ62 = berechne_durchschnittliche_steigung(st.session_state.zeichnungsdf, start_value, end_value,"zz62")
    falgpa_ZZ62_ergebnis = gesamtergebnis_berechnen(falgpa_ZZ62['wert_differenz'], falgpa_ZZ62['index_differenz'], dilution, df, volume)

    falgpa_ZZ63 = berechne_durchschnittliche_steigung(st.session_state.zeichnungsdf, start_value, end_value,"zz63")
    falgpa_ZZ63_ergebnis = gesamtergebnis_berechnen(falgpa_ZZ63['wert_differenz'], falgpa_ZZ63['index_differenz'], dilution, df, volume)

    # st.write(falgpa_humanase_h)
    
    # Daten erstellen
    data = {
        "Probe": ["Humanase H", "ZZ55", "ZZ58", "ZZ60", "ZZ62", "ZZ63"],
        "FALGPA": [falgpa_humanase_h_ergebnis, falgpa_ZZ55_ergebnis, falgpa_ZZ58_ergebnis, falgpa_ZZ60_ergebnis, falgpa_ZZ62_ergebnis, falgpa_ZZ63_ergebnis],
        " %-Anteil ": [ "100%" , "%", "%", "%", "%", "%" ]
    }
    df_ergebnisse = pd.DataFrame(data)
    st.table(df_ergebnisse)
