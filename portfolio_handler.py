import json
from rich.console import Console
from rich.panel import Panel
from configparser import ConfigParser
from datetime import datetime

console = Console()
portfolios_filename = "portfolios/portfolios.json"
users_filename = "users/users.json"
config = ConfigParser()
active_user_file = "users/reserved/active_user.ini"


# Fecha de hoy
today_date = datetime.today().strftime("%d/%m/%Y")

# Assets disponibles para la simulación .-
available_assets = {
    "Crude Oil": "crude_oil",
    "DOW30": "dow_30",
    "Gold": "gold",
    "Nasdaq": "nasdaq",
    "S&P500": "sp500"
}

# Abrir y guardar los cambios en .jsons de users y portfolios.-

def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)

def save_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Voy a utilizar esta función para mostrar los assets disponibles durante la creación de portafolios, a efectos prácticos limitados a este selector.-
def display_assets():
    print("Assets disponibles:")
    for i, asset_name in enumerate(available_assets.keys(), 1):
        print(f"{i}. {asset_name}")

#Creación del portafolio
def create_portfolio():
    config.read(active_user_file)
    portfolio_name = input("Ingrese un nombre para su portafolio: ")
    portfolio_owner = config['USER_INFO']['user_name']

    # Creamos el diccionario de assets, para agregar los inputs del usuario
    portfolio_assets = {}

    # Enseñamos los assets disponibles, y el usuario selecciona los deseados, junto con el porcentaje. 
    display_assets()

    while True:
        selection = input("Con los numeros 1-5, seleccione uno de los assets disponibles. Cuando complete la seleccion, presione enter para continuar: ")
        if not selection:
            break
        try:
            selection_index = int(selection)
            if 1 <= selection_index <= len(available_assets):
                asset_name = list(available_assets.keys())[selection_index - 1]
                asset_key = available_assets[asset_name]
                #una vez seleccionado el asset, solicitaremos el porcentaje asegurando que se trate de un numero del 1 al 100
                while True:
                    try:
                        asset_percentage = float(input("Escriba el porcentaje de participación del asset: %"))
                        if 0 < asset_percentage <= 100:
                            portfolio_assets[asset_key] = asset_percentage
                            break
                        else:
                            print("Debe ser un numero entre 1 y 100.")
                    except ValueError:
                        print("Input no valido, por favor, escriba un numero")
            else:
                print("Input invalido, por favor, escriba un numero entre 1 y 5.")
        except ValueError:
            print("Input no valido, por favor, escriba un numero")
       
    # Hacemos un check de integridad para asegurar que los montos suman 100 correctamente
    total_percentage = sum(portfolio_assets.values())
    if total_percentage != 100:
        print("Error! El total de participación es mayor a 100, por favor, vuelva a intentar.")
        return

    # Inicializamos investing_users para poder cargarlo mas adelante con los usuarios que se agreguen.
    investing_users = []

    # Creamos el portafolio con los datos introducidos para guardarlos en el .json
    new_portfolio = {
        "portfolio_name": portfolio_name,
        "portfolio_owner": portfolio_owner,
        "portfolio_assets": portfolio_assets,
        "investing_users": investing_users
    }

    # Add the new portfolio to the existing list of portfolios
    portfolios = load_json(portfolios_filename)
    portfolios.append(new_portfolio)
    save_json(portfolios, portfolios_filename)

    # Update the user's portfolio lists
    users = load_json(users_filename)
    for user in users:
        if user["user_name"] == portfolio_owner:
            user["portfolios_owned"].append(portfolio_name)
    save_json(users, users_filename)

    print("¡Nuevo portafolio creado con éxito!")


class Portfolio:
    def __init__(self, portfolio_data):
        self.portfolio_name = portfolio_data["portfolio_name"]
        self.portfolio_owner = portfolio_data["portfolio_owner"]
        self.portfolio_assets = portfolio_data["portfolio_assets"]
        self.investing_users = portfolio_data["investing_users"]

    def __str__(self):
        assets_str = "\n".join([f"{asset}: {percentage}%" for asset, percentage in self.portfolio_assets.items()])
        return f"Portfolio Name: {self.portfolio_name},\nOwner: {self.portfolio_owner}, \nAssets:\n{assets_str}."

def get_portfolios():
    with open(portfolios_filename) as f:
        portfolios_data = json.load(f)
        for portfolio_data in portfolios_data:
            portfolio = Portfolio(portfolio_data)
            console.print(Panel(str(portfolio), expand=True))


