import sqlite3
from Doctor import Doctor
from Nurse import Nurse
from Encounter import Encounter


# Función para autenticar medico o enfermera (Se asume que los medicos y/o enfermeros ya han sido registrados en una base de datos de un modulo anteriormente)
# Por lo que para visualizar la implementacion de este modulo se creo una db para medico y una para enfermero, y se registraron usuarios manualmente
def authenticate_user(user_type):
    conn = sqlite3.connect(f'BDs/{user_type}.db')
    cursor = conn.cursor()

    name = input("Ingrese su nombre: ")
    password = input("Ingrese su contraseña: ")

    cursor.execute('SELECT * FROM Lista_{}s WHERE name=? AND password=?'.format(user_type.capitalize()), (name, password))
    user = cursor.fetchone()

    conn.close()
    return user

# Funcion para iniciar el programa
def start_program():
    print("Bienvenido al sistema de la clínica.")
    while True:
        print("Por favor, seleccione el tipo de usuario:")
        print("1. Médico")
        print("2. Enfermero")
        print("3. Salir")
        user_type_option = input("Seleccione una opción: ")

        if user_type_option == '1':
            user_type = 'Medico'
        elif user_type_option == '2':
            user_type = 'Enfermero'
        elif user_type_option == '3':
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

        if user_type in ['Medico', 'Enfermero']:
            user = authenticate_user(user_type)
            if user:
                if user_type == 'Medico':
                    Medico = Doctor(1, "A")
                    Medico.doctor_menu()
                else:
                    Enfermero = Nurse(2, "B")
                    Enfermero.nurse_menu()
            else:
                print("Credenciales incorrectas. Por favor, inténtelo de nuevo.")

start_program()
