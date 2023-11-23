import sqlite3
from Encounter import Encounter

class Doctor:
    def __init__(self, doctor_id, name):
        self.doctor_id = doctor_id
        self.name = name

    # Llamado al metodo para crear encuentro de medico
    def add_encounter(self, patient_id, date, subjective, objective, diagnosis, observations):
        encounter = Encounter(patient_id, date, subjective, objective, diagnosis, observations)
        encounter.save_to_database()
    
    # Funcion para añadir nota aclaratoria a un encuentro especifico cerrado anteriormente
    def add_clarify(self, buscar_id):
        conn = sqlite3.connect('BDs/encuentros.db')
        cursor = conn.cursor()

        nota_aclaratoria = input("Ingrese la nota aclaratoria: ")
        cursor.execute('UPDATE Encuentros SET Nota_aclaratoria = ? WHERE ID = ?', (nota_aclaratoria, buscar_id))
        conn.commit()
        conn.close()

    def create_patient(self, patient_id):
        conn = sqlite3.connect('BDs/encuentros.db')
        cursor = conn.cursor()
       
        name = input("Ingrese nombre completo: ")
        birthday = input("Ingrese la fecha de nacimiento (YYYY-MM-DD): ")
        height = input("Ingrese la estatura (mts): ")
        weight = input("Ingrese el peso (kgs): ")
        bloodtype = input("Ingrese el grupo sanguineo: ")
        address = input("Ingrese la direccion de residencia: ")
        contact = input("Ingrese un telefono de contacto: ")

        # Verificar si el paciente ya existe
        cursor.execute('SELECT * FROM Paciente WHERE id = ?', (patient_id,))
        existing_patient = cursor.fetchone()

        if existing_patient is None:
            # Insertar el paciente solo si no existe
            cursor.execute('INSERT INTO Paciente (id, name, birthday, height, weight, bloodtype, address, contact) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (patient_id, name, birthday, height, weight, bloodtype, address, contact))
    
        else:
            print(f"El paciente con ID {patient_id} ya existe en la base de datos.")

        conn.commit()
        conn.close()
    
    # Funcion para ver los demograficos de un paciente
    def see_demographics(self, buscar_id):
        conn = sqlite3.connect('BDs/encuentros.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Paciente WHERE id = ?', (buscar_id,))
        data = cursor.fetchall()

        for enc in data:
            print("\n")
            print(f"Nombre: {enc[1]}")
            print(f"Fecha de nacimiento: {enc[2]}")
            print(f"Estatura: {enc[3]}")
            print(f"Peso: {enc[4]}")
            print(f"Grupo sanguineo: {enc[5]}")
            print(f"Direccion de residencia: {enc[6]}")
            print(f"Teléfono de contacto: {enc[7]}")
        
        conn.commit()
        conn.close()
        
    # Funcion para acceder al reporte de todos los encuentros de un paciente
    def user_reports(self, buscar_id):
        conn = sqlite3.connect('BDs/encuentros.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Encuentros WHERE Patient_id = ?', (buscar_id,))
        encounters = cursor.fetchall()

        # Mostrar la información de los encuentros encontrados
        for idx, enc in enumerate(encounters, start=1):
            print("\n")
            print(f"Encuentro {idx}:")
            print(f"ID del paciente: {enc[1]}")
            print(f"Fecha: {enc[2]}")
            print(f"Subjetivo: {enc[3]}")
            print(f"Objetivo: {enc[4]}")
            print(f"Diagnóstico: {enc[5]}")
            print(f"Observaciones: {enc[6]}")
            print(f"Notas aclaratorias: {enc[7]}")
        
        conn.commit()
        conn.close()

    # Funcion para desplegar el menú de medico
    def doctor_menu(self):
        while True:
            print("\nMenú de Médico")
            print("1. Crear nuevo paciente")
            print("2. Agregar encuentro")
            print("3. Ver reporte de encuentros de paciente")
            print("4. Añadir nota aclaratoria a un encuentro creado")
            print("5. Ver datos demograficos de un paciente")
            print("6. Salir")
            option = input("Seleccione una opción: ")

            if option == '1':
                patient_id = int(input("Ingrese el ID del paciente: "))
                self.create_patient(patient_id)

            elif option == '2':
                patient_id = int(input("Ingrese el ID del paciente: "))
                date = input("Ingrese la fecha del encuentro (YYYY-MM-DD): ")
                subjective = input("Ingrese la información subjetiva: ")
                objective = input("Ingrese la información objetiva: ")
                diagnosis = input("Ingrese el diagnóstico: ")
                observations = input("Ingrese las observaciones: ")
                self.add_encounter(patient_id, date, subjective, objective, diagnosis, observations)

            elif option == '3':
                buscar_id = int(input("Ingrese el ID del paciente: "))
                self.user_reports(buscar_id)

            elif option == '4':
                buscar_id = int(input("Ingrese el ID del encuentro: "))
                self.add_clarify(buscar_id)
            
            elif option == '5':
                buscar_id = int(input("Ingrese el ID del paciente: "))
                self.see_demographics(buscar_id)

            elif option == '6':
                break

            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")