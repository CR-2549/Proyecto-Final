import os
import pandas as pd

# Este ID lo extrajé desde el mismo link que nos proporcionó GOOGLE
sheet_id = "1CzwANfv2tnPCG8SOo2la0zITeUMLz3YA3o3NZk_mzFc"

#Nombres de las hojas de EXCEL
hojas = ["Equipament", "Materials", "Consumables"]

#Locación de destino para los archivos.
carpeta = "Dataset"
os.makedirs(carpeta, exist_ok=True)

for hoja in hojas:
    url_csv = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={hoja}"
    df = pd.read_csv(url_csv)
    ruta = os.path.join(carpeta, f"{hoja}.csv")
    df.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Hoja '{hoja}' guardada como '{ruta}'")
