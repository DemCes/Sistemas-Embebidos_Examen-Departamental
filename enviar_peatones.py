import json
import requests
import os

def enviar_eventos_al_servidor(ruta_json, url_servidor):
    if not os.path.exists(ruta_json):
        print(f"No se encontró el archivo {ruta_json}")
        return

    with open(ruta_json, 'r') as f:
        eventos = json.load(f)

    if not eventos:
        print("No hay eventos para enviar.")
        return

    for evento in eventos:
        try:
            response = requests.post(url_servidor, json=evento)
            if response.status_code == 200:
                print(f"Evento enviado correctamente: {evento}")
            else:
                print(f"Error al enviar evento {evento}: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Excepción enviando evento {evento}: {e}")

if __name__ == "__main__":
    ruta_json = "datos/peatones.json"
    url_servidor = "http://localhost:3000/api/peaton" # Cambia esto a la URL de tu API

    enviar_eventos_al_servidor(ruta_json, url_servidor)
