import pandas as pd
import mysql.connector

# Cargar los datos y reemplazar NaN con None para compatibilidad con MySQL
consumibles = pd.read_csv("DatasetLimpios/Consumables.csv")


equipamiento = pd.read_csv("DatasetLimpios/Equipament.csv")


materiales = pd.read_csv("DatasetLimpios/Materials.csv")


# Conectar a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="haloce123",
)
cursor = conexion.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS ZeldaItemsBD")
cursor.execute("USE ZeldaItemsBD")

# Crear tabla Consumibles
cursor.execute("""
CREATE TABLE IF NOT EXISTS Consumables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    subclass VARCHAR(50),
    description TEXT,
    ingredients TEXT
);
""")

# Crear tabla Equipamiento
cursor.execute("""
CREATE TABLE IF NOT EXISTS Equipament (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    class VARCHAR(50),
    subclass VARCHAR(50),
    durability INT,
    strength INT,
    description TEXT
);
""")

# Crear tabla Materiales
cursor.execute("""
CREATE TABLE IF NOT EXISTS Materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    subclass VARCHAR(50),
    description TEXT
);
""")

# Insertar datos en Consumibles
for i, fila in consumibles.iterrows():
    cursor.execute("""
        INSERT INTO Consumables (name, subclass, description, ingredients)
        VALUES (%s, %s, %s, %s)
    """, (fila['name'], fila['subclass'], fila['description'], fila['ingredients']))

# Insertar datos en Equipamiento
for i, fila in equipamiento.iterrows():
    cursor.execute("""
        INSERT INTO Equipament (name, class, subclass, durability, strength, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (fila['name'], fila['class'], fila['subclass'], fila['durability'], fila['strength'], fila['description']))

# Insertar datos en Materiales
for i, fila in materiales.iterrows():
    cursor.execute("""
        INSERT INTO Materials (name, subclass, description)
        VALUES (%s, %s, %s)
    """, (fila['name'], fila['subclass'], fila['description']))


# Confirmar cambios y cerrar
conexion.commit()
print("Los datos se insertaron correctamente en la base de Datos: ZeldaItemsBD ")
cursor.close()
conexion.close()
