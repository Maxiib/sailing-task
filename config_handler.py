import json
from datetime import datetime
from configparser import ConfigParser

# Abrir y guardar los cambios en .jsons de users y portfolios.-

def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)

def save_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

#Configuración de usuario/sesion activa .ini
active_user_file = "users/reserved/active_user.ini"
config = ConfigParser()

#Datos json - rutas portfolio y pseudo db usuarios.-
portfolios_filename = "portfolios/portfolios.json"
users_filename = "users/users.json"

#Datetime
today_date = datetime.today().strftime("%d/%m/%Y")