# prueba-data-engineer

# Parte 1: AWS y GCP (Infraestructura en la nube)
## 1. Migración de base de datos
### Migración de MySQL a Cloud SQL:
1. **Pasos detallados para migrar una base de datos MySQL a Google Cloud SQL:**

   - Planificación:
        - Verifica la versión de MySQL de origen para asegurar compatibilidad con Cloud SQL.
        - Define un periodo de migración, especialmente si la base de datos está en uso activo.
        - Identifica las dependencias y realiza un respaldo completo.
2. Exportación de datos:
    - Utiliza mysqldump para exportar los datos.
        ``` bash
        mysqldump -u usuario -p base_de_datos > respaldo.sql
        ```
3. Crear la instancia en Cloud SQL:
    - Desde la consola de GCP, crea una nueva instancia de Cloud SQL seleccionando MySQL como el motor de base de datos.
4. Importación de datos:
    - Sube el archivo de respaldo a Google Cloud Storage.
    - Importa los datos desde Cloud Storage a Cloud SQL:
        ```bash
        gcloud sql import sql nombre_instancia gs://ruta_al_respaldo/respaldo.sql
        ```
5. Verificación de la integridad:
    - Verifica la integridad de los datos comparando registros y realizando pruebas.
### Script para exportar la base de datos de prueba desde MySQL:

```bash
# Exportar la base de datos
mysqldump -u usuario -p --databases nombre_base > base_datos_respaldo.sql

# Instrucciones para importarlo en Cloud SQL
gcloud sql instances create my-instance --database-version=MYSQL_8_0 --tier=db-n1-standard-1

gcloud sql import sql my-instance gs://mi-bucket/base_datos_respaldo.sql
```
- Desafíos:

    - Tamaño de los archivos: Las grandes bases de datos requieren más tiempo y espacio.
    - Tiempo de inactividad: Se debe planificar el downtime de la migración.
    - Otros Problemas comunes: Diferencias de versiones, interrupciones en la conexión durante la exportación o importación.
    - Mitigación: Asegurar la compatibilidad de versiones y mantener conexiones estables.
## 2. Optimización en la nube
## AWS:
1. Recomendaciones para optimizar costos en AWS:

    - EC2: Utilizar instancias reservadas o spot instances para cargas predecibles.
    - S3: Habilitar S3 Intelligent-Tiering para mover datos a almacenamiento de menor costo y habilitar el ciclo de vida para mover datos antiguos a Glacier (almacenamiento más económico).
    - RDS: Escalar la base de datos en función de la carga y habilitar "read replicas" para consultas de solo lectura y optimizar el uso de instancias según las necesidades. Habilitar el auto-scaling y el apagado de instancias en horarios no laborales.
2. Ajuste de recursos para mejorar la eficiencia:

    - Autoescalado de EC2 para adaptarse a cambios de carga.
    - Configurar reglas de retención en S3 y eliminar versiones antiguas de objetos.

GCP:

1. Recomendaciones para optimizar costos en GCP:

    - Compute Engine: Utilizar máquinas preemtibles o autoscalado.
    - Cloud Storage: Habilitar clases de almacenamiento como Nearline o Coldline para archivos de acceso esporádico.
    - Cloud SQL: Ajustar el tamaño de la instancia según el uso.
2. Comparativa con AWS:

    - Costos: En GCP, las máquinas preemtibles son más económicas que las spot instances de AWS.
    - Facilidad de uso: GCP tiene una integración más sencilla para escalar automáticamente las bases de datos con Cloud SQL.
-  Diferencias clave entre IAM en AWS y GCP:
    - IAM en AWS: Es más granular y permite asignar permisos a nivel de servicio específico (S3, EC2).
    - IAM en GCP: Está más enfocado en la gestión de roles a nivel de proyecto o recurso, facilitando una gestión más global.
- Alta disponibilidad:
    - En AWS, se puede utilizar Multi-AZ en RDS para garantizar la alta disponibilidad.
    - En GCP, se pueden usar réplicas en diferentes regiones para Cloud SQL.

    
# Parte 2: Python (Desarrollo y scripting)
1. Procesamiento de datos
Script en Python para limpiar un CSV y realizar agregaciones:

```python
import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('/mnt/data/ID,Nombre,Fecha,Costo.CSV')

# Eliminar duplicados
df = df.drop_duplicates()

# Realizar agregaciones
total_costo = df['Costo'].sum()
promedio_costo = df['Costo'].mean()

print(f"Total Costo: {total_costo}")
print(f"Promedio Costo: {promedio_costo}")

# Guardar el CSV limpio
df.to_csv('limpio.csv', index=False)
```
### Optimización para grandes volúmenes:

- Utilizar chunksize para leer el CSV por partes y procesarlo en fragmentos.
### Script para creación de bucket en S3 y Cloud Storage:

```python
import boto3
from google.cloud import storage

# AWS S3
s3 = boto3.client('s3')
try:
    s3.create_bucket(Bucket='mi-bucket-s3')
    print("Bucket S3 creado exitosamente.")
except Exception as e:
    print(f"Error al crear bucket en S3: {e}")

# GCP Cloud Storage
client = storage.Client()
bucket = client.bucket('mi-bucket-gcp')
try:
    bucket.create(location="US")
    print("Bucket de Cloud Storage creado exitosamente.")
except Exception as e:
    print(f"Error al crear bucket en GCP: {e}")
```
### Optimización de memoria en Python:
- Utilizar generadores para procesar datos grandes sin cargar todo en memoria.
- Uso de librerías como dask, pyspark o pandas con chunksize para manejar grandes volúmenes de datos.
### Interacción con APIs de AWS y GCP:
- AWS SDK (Boto3) y GCP SDK (google-cloud) son las bibliotecas recomendadas. Ambas utilizan autenticación mediante credenciales.
# Parte 3: Migración de Bases de Datos Complejas
1. Estrategia de migración sin downtime:
- Estrategia:
    - Habilitar la replicación en el servidor on-premise.
    - Migrar la base de datos en modo replicación (master-slave).
    - Cuando se alcance la sincronización, cambiar el rol de la nueva base de datos a master.
2. Configuración de replicación MySQL entre AWS y GCP:
    - Se puede utilizar MySQL binlog para configurar la replicación entre instancias.
# Parte 4: Automatización de WhatsApp
### Script en Python para enviar mensajes interactivos:
```python
import requests
import json

# SIMULACION API
API_URL = "https://api.whatsapp.com/send"
TOKEN = 'toke_de_accesso'

# Datos 
mensaje_interactivo = {
    "to": "whatsapp:+123456789",
    "type": "interactive",
    "interactive": {
        "type": "button",
        "body": {
            "text": "Hola, ¿en qué puedo ayudarte?"
        },
        "action": {
            "buttons": [
                {
                    "type": "reply",
                    "reply": {
                        "id": "1",
                        "title": "Ver productos"
                    }
                },
                {
                    "type": "reply",
                    "reply": {
                        "id": "2",
                        "title": "Contactar soporte"
                    }
                }
            ]
        }
    }
}

# Función para enviar mensaje
def enviar_mensaje(mensaje):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(mensaje))
    
    if response.status_code == 200:
        print("Mensaje enviado exitosamente")
        return response.json()
    else:
        print("Error al enviar el mensaje", response.status_code, response.text)
        return None

# Simulación del envío
respuesta = enviar_mensaje(mensaje_interactivo)

# Manejo de la respuesta del usuario
if respuesta:
    user_reply_id = respuesta.get('user_reply_id', None)
    if user_reply_id == '1':
        print("El usuario eligió: Ver productos")
    elif user_reply_id == '2':
        print("El usuario eligió: Contactar soporte")

```
### Requisitos para usar la API de WhatsApp Business:

- Cuenta de WhatsApp Business: Se debe tener cuenta en WhatsApp Business.
- Acceso a la API: Solicitar acceso a la API de WhatsApp Business desde Meta.
- Habilitación de un número de teléfono:  un número de teléfono que esté dedicado exclusivamente a la API.
- Configuración de un servidor: Contar con un servidor que procese las solicitudes entrantes y salientes a través de la API.
- Token de autenticación: Se requiere un token para autenticar las solicitudes a la API.
### Consideraciones de seguridad:
- Encriptación de extremo a extremo: WhatsApp utiliza encriptación de extremo a extremo.
- Autenticación segura: Utilizar autenticación segura para acceder a la API mediante tokens.
- Manejo de datos sensibles: No se deben transmitir datos sensibles sin encriptación adicional.
- Control de acceso
- Prevención de ataques de spam o phishing
