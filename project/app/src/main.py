from fastapi import FastAPI, HTTPException
import uvicorn
import boto3
import pandas as pd
from io import StringIO

# Crear una instancia de la aplicación FastAPI
app = FastAPI()
s3_client = boto3.client('s3')

# Endpoint para la raíz ("/")
@app.get("/")
async def read_root():
    return {"mensaje": "¡Bienvenido a mi API con FastAPI!"}

# Definir un endpoint para saludar al usuario
@app.get("/saludo/{nombre}")
async def saludar(nombre: str):
    return {"mensaje": f"Hola, {nombre}!"}

# Leer un csv
@app.get("/csv/")
async def leer_csv():
    """
    Lee un archivo CSV desde un bucket de S3.
    :param bucket: Nombre del bucket S3.
    :param archivo: Nombre del archivo CSV en el bucket.
    :return: Contenido del CSV en formato JSON.
    """
    try:
        # Descargar el archivo CSV desde S3
        s3_object = s3_client.get_object(Bucket='mi-bucket-project', Key='datos.csv')
        # Leer el contenido del archivo CSV
        csv_content = s3_object['Body'].read().decode('utf-8')
        # Usar pandas para leer el CSV desde el contenido descargado
        df = pd.read_csv(StringIO(csv_content))   
        return print(df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
