from portfolio_handler import load_json,save_json
from config_handler import config, active_user_file, portfolios_filename, users_filename, today_date

#Para la sesion - datos de usuario.-
config.read(active_user_file)

#Con esta funcion vamos a invertir en cada portafolio.-
def invest_in_portfolio():
    
    #recuperamos y mostramos los portfolios.-
    load_json(portfolios_filename)

    #Solicitamos el nombre del portfolio (podria haber sido un indice.)
    #A lo largo del código Utilizo ambas aproximamos para una revisión a/b de la aproximacion.-
    portfolio_name = input("Escriba el nombre del portfolio en el que desea invertir: ")
    investment = input("Por favor,  indique el monto que desea invertir: ")
    
    #Creamos un dic con los valores que serán guardados.-
    new_investment = {
        "user_name": config['USER_INFO']['user_name'],
        "initial_amount": float(investment),
        "investment_date": today_date,
        "current_balance": float(investment)
    }
    
    #Cargamos y recorremos los portfolios. Al encontrar el portfolio con el nombre, se agrega a
    #los inversores esta nueva inversion y se guarda.-
    portfolios = load_json(portfolios_filename)
    for portfolio in portfolios:
        if portfolio["portfolio_name"] == portfolio_name:
            portfolio["investing_users"].append(new_investment)
            break
    save_json(portfolios, portfolios_filename)

    #Cargamos los usuarios y agregamos esta inversion al respectivo.-
    users = load_json(users_filename)
    for user in users:
        if user["user_name"] == config['USER_INFO']['user_name']:
            user["portfolios_invested"].append(portfolio_name)
    save_json(users, users_filename)
    print(f'Se han invertido {investment} en {portfolio_name} con éxito!')

#Esta función permitira el cash out del balance del usuario.-
def cash_out():
    user_name = config['USER_INFO']['user_name']
    
    portfolios = load_json(portfolios_filename)
    users = load_json(users_filename)
    
    # Recuperaremos primero los portfolios (si existen) del usuario 
    user_portfolios = [portfolio["portfolio_name"] for portfolio in portfolios if any(user["user_name"] == user_name for user in portfolio["investing_users"])]
    
    #Desplegamos solamente estos portfolios en los que invirtió el usuario, junto con la infromación de la inversión y esta vez el indice.-
    print("Portafolios en los que se ha invertido: ")
    for index, portfolio in enumerate(portfolios, 1):
        for user in portfolio["investing_users"]:
            if user["user_name"] == user_name:
                user_portfolios.append(portfolio)
                initial_amount = user["initial_amount"]
                initial_date = user["investment_date"]
                current_balance = user["current_balance"]
                print(f"{index}. {portfolio['portfolio_name']} - Initial Date: {initial_date}, Initial Balance: {initial_amount}, Current Balance: {current_balance}")
    
    # Solicitamos el indice.-
    selected_index = int(input("Escribe el indice del portafolio del que deseas retirar tus fondos: ")) - 1
    selected_portfolio_name = user_portfolios[selected_index]
    
    #Recorremos los portafolios, buscando coincidencia en el que selecciono el usuario
    for portfolio in portfolios:
        if portfolio["portfolio_name"] == selected_portfolio_name:
            for user in portfolio["investing_users"]:
                if user["user_name"] == user_name:
                    
                    # Con la coincidencia, buscamos el usuario dentro del json de usuarios
                    for u in users:
                        if u["user_name"] == user_name:
                            
                            #Agregamos el balance actual
                            u["cash_out"] += user["current_balance"]
                            
                            #Quitamos al usuario de los inversores
                            portfolio["investing_users"].remove(user)
                            
                            #Quitamos la inversion del usuario en users.json
                            if portfolio["portfolio_name"] in u["portfolios_invested"]:
                                u["portfolios_invested"].remove(portfolio["portfolio_name"])
                            break
                
                    # Borrando el dicc del user de investing_users en portfolios.json
                    portfolio["investing_users"] = [u for u in portfolio["investing_users"] if u["user_name"] != user_name]
                    
                    break
    
    #Guardamos ambos archivos
    save_json(portfolios, portfolios_filename)
    save_json(users, users_filename)