import pandas as pd

# Inicializar variables de agregación
suma_costo = 0.0
total_registros = 0
total_valores_validos = 0

# Leer el archivo CSV en chunks para manejar grandes volúmenes de datos
file_path = 'ID,Nombre,Fecha,Costo.CSV'
chunk_size = 10000 

for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    # Eliminar duplicados en cada chunk
    chunk_cleaned = chunk.drop_duplicates()

    # Convertir la columna 'Costo' a numérica, Eeto fuerza los errores a NaN
    chunk_cleaned['Costo'] = pd.to_numeric(chunk_cleaned['Costo'], errors='coerce')

    # Eliminar filas donde costo sea NaN
    chunk_cleaned = chunk_cleaned.dropna(subset=['Costo'])

    # Sumar los costos validos en este chunk
    suma_costo += chunk_cleaned['Costo'].sum()
    
    # Acumular el total de registros procesdos y los valores validos
    total_registros += len(chunk)
    total_valores_validos += len(chunk_cleaned)

# Calcular el promedio del costo
promedio_costo = suma_costo / total_valores_validos if total_valores_validos > 0 else 0

# Mostrar resultados
print(f"Suma total del costo: {suma_costo}")
print(f"Promedio del costo: {promedio_costo}")
print(f"Total de registros procesados: {total_registros}")
print(f"Total de valores válidos: {total_valores_validos}")
