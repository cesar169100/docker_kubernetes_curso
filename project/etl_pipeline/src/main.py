# from fastapi import HTTPException
import boto3
import pandas as pd
from io import StringIO
from botocore.exceptions import ClientError


s3_client = boto3.client('s3')

def s3_read_csv(bucket: str, key: str):
    # try:
    # Descargar el archivo CSV desde S3
    s3_object = s3_client.get_object(Bucket=bucket, Key=key)
    # Leer el contenido del archivo CSV
    csv_content = s3_object['Body'].read().decode('utf-8')
    # Usar pandas para leer el CSV desde el contenido descargado
    df = pd.read_csv(StringIO(csv_content))   
    return df
    # except Exception as e:
    #      raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")
    
def transformacion(df):
    df['costo'] = [200,100,500,1000]
    return df

def s3_upload_df(df, bucket, carpeta, archivo):
    try:
        # Verificar si la carpeta existe listando los objetos con ese prefijo
        # resultado = s3_client.list_objects_v2(Bucket=bucket, Prefix=carpeta)
        # Si no hay contenidos bajo ese prefijo, significa que la carpeta no existe
        # if 'Contents' not in resultado:
        #     print(f"La carpeta '{carpeta}' no existe, creando...")
        # Convertir el DataFrame a un archivo CSV en memoria
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Subir el archivo CSV al bucket S3 bajo el prefijo (carpeta)
        s3_client.put_object(Bucket=bucket, Key=f"{carpeta}/{archivo}", Body=csv_buffer.getvalue())
        print(f"Archivo '{archivo}' subido exitosamente a la carpeta '{carpeta}' en el bucket '{bucket}'.")
        
    except ClientError as e:
        print(f"Error al subir el archivo: {e}")

if __name__=='__main__':
     df = s3_read_csv('mi-bucket-project', 'datos.csv')
     df2 = transformacion(df)
     s3_upload_df(df2, 'mi-bucket-project', 'mi-carpeta', 'datos2.csv')