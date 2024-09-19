import pandas as pd

# Cargar el archivo CSV
file_path = 'ID,Nombre,Fecha,Costo.CSV'
df = pd.read_csv(file_path)

# Eliminar duplicados
df_cleaned = df.drop_duplicates()

# Eliminar caracteres no numéricos en la columna 'Costo' y convertir a numérico
df_cleaned['Costo'] = pd.to_numeric(df_cleaned['Costo'], errors='coerce')

# Eliminar filas donde el costo sea NaN 
df_cleaned = df_cleaned.dropna(subset=['Costo'])

# Realizar agregaciones básicas 
suma_costo = df_cleaned['Costo'].sum()
promedio_costo = df_cleaned['Costo'].mean()

# Guardar el archivo 
df_cleaned.to_csv('cleaned_file.csv', index=False)

# Mostrar resultados
print(f"Suma total del costo: {suma_costo}")
print(f"Promedio del costo: {promedio_costo}")



