import time

global nivel

# asignar nivel
nivel = "bajo"
nivel_file_path = "/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm/braulio/semaforos/nivel.txt"

while True:
    new_nivel = input("Inserte nuevo nivel: ")
    nivel = new_nivel

    # Escribir el nuevo nivel en el archivo
    with open(nivel_file_path, "w") as file:
        file.write(new_nivel)

    # Puedes agregar algún tiempo de espera opcional para evitar 
    # que se lea el nivel demasiado rápido
    time.sleep(3)
