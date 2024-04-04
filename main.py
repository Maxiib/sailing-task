from user_handler import user_login, create_user, clear_user
from daily_updates import update_prices, update_user_balances
from portfolio_handler import get_portfolios, create_portfolio
from operations_handler import invest_in_portfolio, cash_out

# main - ui
def main():
    # Actualiza los precios de los activos y los balances de los usuarios.-
    variations = update_prices()
    update_user_balances(variations)
    
    #Iniciamos nuestro ui
    while True:
        print("\n Bienvenido al sistema de gestión de inversiones.")
        print("1. Iniciar sesión")
        print("2. Crear usuario")
        print("3. Salir")

        choice = input("Seleccione una opción escribiendo uno de los números: ")
        
        # Opción para iniciar sesión
        if choice == "1": 
            username = user_login()
            if username:
                while True:
                    print("\nMenú principal:")
                    print("1. Ver portafolios")
                    print("2. Invertir en un portafolio")
                    print("3. Realizar cash out")
                    print("4. Crear portafolio")
                    print("5. Cerrar sesión")

                    option = input("Seleccione una opción: ")

                    if option == "1":  # Ver portafolios
                        get_portfolios()
                    elif option == "2":  # Invertir en un portafolio
                        invest_in_portfolio()
                    elif option == "3":  # Realizar cash out
                        cash_out()
                    elif option == "4":  # Crear portafolio
                        create_portfolio()
                    elif option == "5":  # Cerrar sesión
                        print("Cerrar sesión.")
                        clear_user()
                        break
                    else:
                        print("Opción no válida. Por favor, seleccione nuevamente.")
        
        # Opción para crear un nuevo usuario
        elif choice == "2":  
            create_user()
        
        # Opción para salir del programa
        elif choice == "3":
            print("¡Hasta luego!")
            break        
        else:
            print("Opción no válida. Por favor, seleccione nuevamente.")

if __name__ == "__main__":
    # Limpia la "sesion" del usuario al inicio del programa
    clear_user()
    # Ejecuta la función principal main, que sera en este caso nuestra UI
    main()
