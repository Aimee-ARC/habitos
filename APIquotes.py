import requests

category = 'happiness'
api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
response = requests.get(api_url, headers={'X-Api-Key': 'UfzmMDWqiU962nYZGZurIw==nLlSvls0UwwXfycs'})
if response.status_code == requests.codes.ok:
    quotes = response.json()  # Convierte la respuesta JSON en un objeto Python
    if quotes:  # Verifica que la lista de citas no esté vacía
        quote = quotes[0]['quote']  # Accede a la primera cita
        print(quote)  # Imprime solo la cita
    else:
        print("No se encontraron citas.")
else:
    print("Error:", response.status_code, response.text)