import os
import time

# Definir el nombre de la variable de entorno
nivel_env_variable = "NIVEL_SEMAFORO"

# Establecer un valor inicial para la variable de entorno
os.environ[nivel_env_variable] = "bajo"

while True:
    new_nivel = input("Inserte nuevo nivel: ")

    # Actualizar la variable de entorno con el nuevo nivel
    os.environ[nivel_env_variable] = new_nivel

    # Puedes agregar algún tiempo de espera opcional para evitar que se lea el nivel demasiado rápido
    time.sleep(1)
