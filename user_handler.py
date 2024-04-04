import json
from configparser import ConfigParser
from config_handler import load_json, save_json,active_user_file, users_filename, config
    
#El usuario activo (la sesión) se maneja desde un archivo .ini, podría haber sido local, env, etc. La "db" es un .json

#La función clear user restablece el .ini, cerando la sesión de facto.
def clear_user():
    active_user = ConfigParser()
    active_user['USER_INFO'] = {
        'user_type' : 'unreg_user',
        'user_name' : 'none'}
    with open('users/reserved/active_user.ini', 'w') as configfile:
        active_user.write(configfile)

#Para creacion de usuarios. Primero controlamos estar deslogeados. Failsafe, porque el script restablece sesiones al ejecutarse.
def create_user():
    config.read(active_user_file)
    user_type = config.get("USER_INFO", "user_type", fallback="unreg_user")

    if user_type != "unreg_user":
        close_session = input("Sesión activa. Debe cerrar sesión para crear un usuario nuevo. Desea cerrar la sesion activa? (y/n): ")
        if close_session.lower() == "y":
            clear_user() 
        else:
            print("Se mantendra la sesion abierta. Cancelando registro de usuario.")
            return

    #Creación de usuario
    print("Registre un usuario nuevo.")
    while True:
        try:
            username = input("Ingrese su nombre de usuario. Utilice minusculas y solo caracteres alfabeticos: ")
            
            # Comparamos con la base de datos, para evitar redundancias
            users = load_json(users_filename)
            for user in users:
                if user["user_name"] == username:
                    raise ValueError("Error en la creación de usuario. Nombre ya utilizado")
            break        
        except ValueError as e:
            print(e)

    password = input("Ingrese una contraseña: ")

    # Creamos un diccionario con las credenciales nuevas y operaciones en blanco para poder agregarlo al json
    new_user = {
        "user_name": username,
        "user_pass": password,
        "portafolios_owned": [],
        "portfolios_invested": [],
        "cash_in": 0,
        "cash_out": 0
    }
    users.append(new_user)

    # Guardamos el user en nuestra """"""""""db"""""""""""
    save_json(users, users_filename)

    print("Usuario creado con éxito!")

#login
def user_login():
    # Leemos la infomación del ini, para saber si hay una sesion activa. Sino, se indica el login
    config.read(active_user_file)
    user_type = config['USER_INFO']['user_type']
    user_name = config['USER_INFO']['user_name']
    if user_type != 'unreg_user':
        print(f"Bienvenido de nuevo {user_name}")
        return user_name
    else:
        print("Por favor, inicie sesion.")
    username = input("Ingrese su nuevo nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    #Comparamos los datos con los del .json para saber si existe el user.
    users = load_json(users_filename)
    for user in users:
        if user["user_name"] == username and user.get("user_pass") == password:
            print(f"Bienvenido {username}.")

            #Actualizamos la sesion. Esto lol utilizamos para hacer las operaciones tambien.
            config["USER_INFO"]["user_type"] = "reg_user"
            config["USER_INFO"]["user_name"] = username
            with open(active_user_file, "w") as configfile:
                config.write(configfile)

            return username

    print("Credenciales incorrectas. Vuelva a intenarlo.")
    return None
