import json
import datetime
import boto3
from bs4 import BeautifulSoup
import re

# Configuración de S3
s3_client = boto3.client("s3")
SOURCE_BUCKET = "bucket-parcial1-1"
DESTINATION_BUCKET = "bucket-parcial1-2"

def clean_price(price):
    """Limpia y convierte el precio en un string numérico sin comas ni símbolos."""
    if isinstance(price, (int, float)):
        return str(price)
    if price and isinstance(price, str):
        return "".join(filter(str.isdigit, price))  # Extrae solo los números
    return "N/A"

def extract_number(value):
    """Extrae solo números de un string."""
    if value and isinstance(value, str):
        digits = re.sub(r"\D", "", value)  # Elimina caracteres no numéricos
        return digits if digits else "N/A"
    return "N/A"

def get_rooms_and_bathrooms(card):
    """
    Extrae el número de habitaciones y baños.
    Primero intenta leerlos desde data-rooms y data-bathrooms.
    Si no existen, los busca en etiquetas <span> con clases alternativas.
    """
    # Intentar extraer desde atributos data-rooms y data-bathrooms
    rooms = card.get("data-rooms", None)
    bathrooms = card.get("data-bathrooms", None)

    # Si no se encuentran en los atributos, buscar dentro de etiquetas <span>
    if not rooms:
        for span in card.find_all("span"):
            class_names = span.get("class", [])
            for class_name in class_names:
                if re.search(r"rooms|habitaciones", class_name, re.IGNORECASE):
                    rooms = span.text.strip()
                    break  # Detener búsqueda si se encuentra
    
    if not bathrooms:
        for span in card.find_all("span"):
            class_names = span.get("class", [])
            for class_name in class_names:
                if re.search(r"bathrooms|baños", class_name, re.IGNORECASE):
                    bathrooms = span.text.strip()
                    break  # Detener búsqueda si se encuentra

    # Limpiar los valores extraídos para que solo contengan números
    rooms = extract_number(rooms)
    bathrooms = extract_number(bathrooms)

    return rooms, bathrooms

def extract_data(html_content):
    """Extrae datos de apartaestudios desde las etiquetas <a> en el HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    fecha_descarga = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    registros = []
    
    # Buscar todas las etiquetas <a> con clase "listing listing-card"
    property_cards = soup.find_all("a", class_="listing listing-card")
    for card in property_cards:
        # Extraer ubicación y precio
        location = card.get("data-location", "N/A").strip() if card.get("data-location") else "N/A"
        price = clean_price(card.get("data-price", "N/A"))

        # Extraer número de habitaciones y baños
        rooms, bathrooms = get_rooms_and_bathrooms(card)

        # Extraer área en metros cuadrados
        floor_area_raw = card.get("data-floorarea", "N/A")
        floor_area = extract_number(floor_area_raw)
        
        registros.append([fecha_descarga, location, price, rooms, bathrooms, floor_area])
    
    return registros

def save_to_s3(data, filename):
    """Guarda los datos extraídos en un CSV y lo sube a S3."""
    header = "FechaDescarga,Barrio,Valor,NumHabitaciones,NumBanos,mts2"
    csv_content = header + "\n" + "\n".join([",".join(map(str, row)) for row in data])
    
    s3_client.put_object(
        Bucket=DESTINATION_BUCKET,
        Key=filename,
        Body=csv_content.encode("utf-8"),
        ContentType="text/csv"
    )
    print(f"Archivo {filename} guardado en S3 en el bucket {DESTINATION_BUCKET}.")

def app(event, context):
    """Maneja la ejecución del Lambda cuando se sube un archivo HTML a S3."""
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        
        if bucket == SOURCE_BUCKET:
            response = s3_client.get_object(Bucket=bucket, Key=key)
            html_content = response["Body"].read().decode("utf-8")
            
            data = extract_data(html_content)
            
            if data:
                today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
                csv_filename = f"{today}.csv"
                save_to_s3(data, csv_filename)
                
                return {
                    "statusCode": 200,
                    "body": f"Archivo procesado y guardado en s3://{DESTINATION_BUCKET}/{csv_filename}"
                }
            else:
                return {
                    "statusCode": 400,
                    "body": "No se encontraron datos en el HTML."
                }
