import os
import RPi.GPIO as GPIO
import time

# Definir el nombre de la variable de entorno
nivel_env_variable = "NIVEL_SEMAFORO"

GPIO.setwarnings(False)  # Desactiva las advertencias de GPIO

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM) 
    ## semaforo 1
    GPIO.setup(25, GPIO.OUT) # semaforo rojo
    GPIO.setup(8, GPIO.OUT) # semaforo ambar 
    GPIO.setup(7, GPIO.OUT) # semaforo verde
    rojo_1 = 25
    ambar_1 = 8
    verde_1 = 7
    ## semaforo 2
    GPIO.setup(20, GPIO.OUT) # semaforo ambar 
    GPIO.setup(16, GPIO.OUT) # semaforo rojo
    GPIO.setup(21, GPIO.OUT) # semaforo verde   
    rojo_2 = 16
    ambar_2 = 20
    verde_2 = 21

    ## inicialzar nivel
    nivel = "bajo"

    ## inicializar tiempos de transicion
    trans_time_1 = 0
    trans_time_2 = 0

    ## inicializar semaforo 1
    GPIO.output(verde_1, False)
    GPIO.output(ambar_1, False)
    GPIO.output(rojo_1, False)
    ## inicializar semaforo 2
    GPIO.output(verde_2, False)
    GPIO.output(ambar_2, False)
    GPIO.output(rojo_2, False)

    time.sleep(5)

    while True:

        # Ahora utilizas el nivel leído para la transición de los LEDs
        nivel = os.environ.get(nivel_env_variable, "bajo")

        ## determinar tiempo de transicion
        if nivel == "bajo":
            trans_time_1 = 30
            trans_time_2 = 30
        elif nivel == "medio":
            trans_time_1 = 40
            trans_time_2 = 20
        elif nivel == "alto":
            trans_time_1 = 50
            trans_time_2 = 10

        ## estado 1
        # semaforo 1 -- verde
        GPIO.output(rojo_1, False)
        GPIO.output(verde_1, True)
        # semaforo 2 -- rojo
        GPIO.output(ambar_2, False)
        GPIO.output(rojo_2, True)
        time.sleep(trans_time_1)
        ## estado 2
        # semaforo 1 -- ambar
        GPIO.output(verde_1, False)
        GPIO.output(ambar_1, True)
        # semaforo 2 -- rojo
        time.sleep(3)
        ## estado 3
        # semaforo 1 -- rojo
        GPIO.output(ambar_1, False)
        GPIO.output(rojo_1, True)
        # semaforo 2 -- verde
        GPIO.output(rojo_2, False)
        GPIO.output(verde_2, True)
        time.sleep(trans_time_2)
        ## estado 4
        # semaforo 1 -- rojo
        # semaforo 2 -- ambar
        GPIO.output(verde_2, False)
        GPIO.output(ambar_2, True)
        time.sleep(3)

    GPIO.cleanup()
