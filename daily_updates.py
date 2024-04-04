import pandas as pd
from random import randint
from config_handler import load_json, save_json, portfolios_filename

portfolio_file = "portfolios/portfolios.json"

asset_list_routes = {
    'nasdaq': 'assets/nasdaq.CSV',
    'sp500': 'assets/sp500.CSV',
    'dow_30': 'assets/dow_30.CSV',
    'crude_oil': 'assets/crude_oil.CSV',
    'gold': 'assets/gold.CSV'
}


#Primero, actualizaremos los precios con una variacion al azar con una amplitud de 10%

def update_prices():
    #Vamos a crear un diccionario con las variaciones de cada asset, para poder portarlas a los balances de los inversores.
    #En una aplicación real, en realidad el proceso sería inverso, donde se devería calcular, scrapear o req. la variacion para poder 
    #Actualizar los balances. Cómo está simulación genera los valores, reutilizaremos esa fracción para no redundar el cálculo.
    variations = {}
    for asset_name, file_path in asset_list_routes.items():
        variation = randint(-5, 5)
        variations[asset_name] = variation
        #Con la variación generada, aplicamos el cambio a los precios de los assets, agregando un dia con el mismo formato que tiene el codigo.
        asset = pd.read_csv(file_path)
        last_date = pd.to_datetime(asset['Date'].iloc[-1], format="%d/%m/%Y")
        new_date = pd.to_datetime(last_date + pd.DateOffset(days=1)).strftime("%d/%m/%Y")
        last_value = asset['Price'].iloc[-1]
        new_value = round(last_value + (variation / 100 * last_value), 2)
        asset.loc[len(asset.index)] = [new_date, new_value]
        asset.to_csv(file_path, index=False)
        print(f'Asset: {asset_name}, Variacion: {variation}%, el nuevo precio es {new_value} (era {last_value})')

    #Devolvemos las variaciones para portar a los balances
    return variations

# Esta función utiliza las variaciones para poder actualzar el balance de cara usuario inversor en el json.
def update_user_balances(variations):
    portfolios = load_json(portfolios_filename)
    
    #recorremos el json, para tomar los portfolios
    for portfolio in portfolios:
        #recorremos el portfolio para encontrar los usuarios inversores
        for user in portfolio["investing_users"]:
            #recorremos los assets y porcentajes del portafolio, para aplicar la variacion correspondiente (,0 para "ignorar/dafaultear" donde no haya cambios)
            for asset_name, percentage in portfolio["portfolio_assets"].items():
                variation = variations.get(asset_name, 0)  
                #calculamos la fraccion representada segun el porcentaje del portafolio del balance actual del user
                represented_fraction = (user["current_balance"] / 100) * percentage
                #calculamos el cambio de la fraccion en funcion a la variacion
                fraction_chage = (represented_fraction / 100 * variation)  
                #agregamos la variación
                user["current_balance"] += fraction_chage
                #(debuging)print(f'for {user}, asset {asset_name} balance_change is {fraction_chage}, for a variation {variation} in percenteage {percentage}')
    
    # Actualizamos en la cadena los balances de cada user
    save_json(portfolios, portfolios_filename)

if __name__ == "__main__":
    #genera las variaciones al azar
    variations = update_prices()
    #actualiza los balances
    update_user_balances(variations)
