import os
import pandas as pd

# Carpetas
carpeta_entrada = "Dataset"
carpeta_salida = "DatasetLimpios"
os.makedirs(carpeta_salida, exist_ok=True)

# Columnas a eliminar para cada archivo
cols_a_eliminar = {
    "Consumables.csv": [
        "image", "class", "hp", "effect"
    ],
    "Equipament.csv": [
        "image", "tags", "range", "arrows", "defense", "defense_upgrade_lvl1", "defense_upgrade_lvl2",
        "defense_upgrade_lvl3", "defense_upgrade_lvl4", "bonus", "selling_price", "bonus_set",
        "upgrade_1", "upgrade_2", "upgrade_3", "upgrade_4", "armor_upgrade", "where_to_find", "notes"
    ],
    "Materials.csv": [
        "image", "class", "hp", "hp_backed", "hp_cooked", "effect_cooked", "quality_lvl",
        "potential", "duration_bonus_cooked", "selling_price", "selling_mon", "dye_color",
        "food_recipe", "armor_upgrade", "compendium_id", "notes", "buying_price", "shop"
    ]
}

for archivo in os.listdir(carpeta_entrada):
    if archivo.endswith(".csv"):
        ruta_in = os.path.join(carpeta_entrada, archivo)
        df = pd.read_csv(ruta_in)

        # Eliminar columnas si existen en el dataframe
        cols_remove = cols_a_eliminar.get(archivo, [])
        cols_remove_existentes = [col for col in cols_remove if col in df.columns]
        df.drop(columns=cols_remove_existentes, inplace=True)

        # Limpieza básica extra
        df.dropna(how="all", inplace=True)
        df.dropna(axis=1, how="all", inplace=True)
        df.columns = [col.strip() for col in df.columns]
        df.drop_duplicates(inplace=True)

        # Rellenar columnas numéricas vacías con 0
        for col in df.select_dtypes(include=["number"]).columns:
            df[col] = df[col].fillna(0)
        # Rellenar columnas de texto con "not apply"
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].fillna("not apply")

        # Guardar archivo limpio
        ruta_out = os.path.join(carpeta_salida, archivo)
        df.to_csv(ruta_out, index=False, encoding="utf-8")
        print(f"'{archivo}' limpiado y guardado en '{ruta_out}'")
