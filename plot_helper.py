import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

def zeichnung_erstellen(df, Messpaar):
    zeichnungsdf = df[df['Raw data']== Messpaar]
    zeichnungsdf = zeichnungsdf.drop(columns=["Zeitwert", "Raw data"])
    #zeichnungsdf = zeichnungsdf.rename(columns={
    #    "positive control": "positive control " + Messpaar, 
    #    "negative control": "negative control " + Messpaar,
    #    "Humanase H": "Humanase H " + Messpaar,
    #    "zz55": "zz55 " + Messpaar,
    #    "zz58": "zz58 " + Messpaar,
    #    "zz60": "zz60 " + Messpaar,
    #    "zz62": "zz62 " + Messpaar,
    #    "zz63": "zz63 " + Messpaar,
    #    "Unnamed: 9": Messpaar + "9",
    #    "Unnamed: 10": Messpaar + "10",
    #   "Unnamed: 11": Messpaar + "11",
    #    "Unnamed: 12": Messpaar + "12",
    #    })
    return zeichnungsdf