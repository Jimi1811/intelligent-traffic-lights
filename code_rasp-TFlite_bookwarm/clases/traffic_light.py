import RPi.GPIO as GPIO
import time

def seteo_pines():
    global red_led_pin_1, red_led_pin_2
    global yellow_led_pin_1, yellow_led_pin_2
    global green_led_pin_1, green_led_pin_2
	
    # Definir pines del rasp (SEMAFORO 1)
    red_led_pin_1 = 18 # semaforo rojo
    yellow_led_pin_1 = 23 # semaforo ambar
    green_led_pin_1 = 24 # semaforo verde
	# Definir pines del rasp (SEMAFORO 2)
    red_led_pin_2 = 17 # semaforo rojo
    yellow_led_pin_2 = 27 # semaforo ambar
    green_led_pin_2 = 22 # semaforo verde
	
    # Configurar pines
    GPIO.setmode(GPIO.BCM) 
	### semaforo 1
    GPIO.setup(red_led_pin_1, GPIO.OUT) # seteo rojo
    GPIO.setup(yellow_led_pin_1, GPIO.OUT) # seteo ambar
    GPIO.setup(green_led_pin_1, GPIO.OUT) # seteo verde
	### semaforo 2
    GPIO.setup(red_led_pin_2, GPIO.OUT) # seteo rojo
    GPIO.setup(yellow_led_pin_2, GPIO.OUT) # seteo ambar
    GPIO.setup(green_led_pin_2, GPIO.OUT) # seteo verde

def sincronizar_trafico(temp):
    ## semaforo 1 (VERDE) --- semaforo 2 (RED)
    GPIO.output(green_led_pin_1, GPIO.HIGH)
    GPIO.output(yellow_led_pin_1, GPIO.LOW)
    GPIO.output(red_led_pin_1, GPIO.LOW)
    GPIO.output(green_led_pin_2, GPIO.LOW)
    GPIO.output(yellow_led_pin_2, GPIO.LOW)
    GPIO.output(red_led_pin_2, GPIO.HIGH)
    time.sleep(temp) 
    ## semaforo 1 (AMBAR) --- semaforo 2 (RED)
    GPIO.output(green_led_pin_1, GPIO.LOW)
    GPIO.output(yellow_led_pin_1, GPIO.HIGH)
    GPIO.output(red_led_pin_1, GPIO.LOW)
    GPIO.output(green_led_pin_2, GPIO.LOW)
    GPIO.output(yellow_led_pin_2, GPIO.LOW)
    GPIO.output(red_led_pin_2, GPIO.HIGH)
    time.sleep(5) 
    ## semaforo 1 (RED) --- semaforo 2 (GREEN)
    GPIO.output(green_led_pin_1, GPIO.LOW)
    GPIO.output(yellow_led_pin_1, GPIO.LOW)
    GPIO.output(red_led_pin_1, GPIO.HIGH)
    GPIO.output(green_led_pin_2, GPIO.HIGH)
    GPIO.output(yellow_led_pin_2, GPIO.LOW)
    GPIO.output(red_led_pin_2, GPIO.LOW)
    time.sleep(temp) 
    ## semaforo 1 (RED) --- semaforo 2 (AMBAR)
    GPIO.output(green_led_pin_1, GPIO.LOW)
    GPIO.output(yellow_led_pin_1, GPIO.LOW)
    GPIO.output(red_led_pin_1, GPIO.HIGH)
    GPIO.output(green_led_pin_2, GPIO.LOW)
    GPIO.output(yellow_led_pin_2, GPIO.HIGH)
    GPIO.output(red_led_pin_2, GPIO.LOW)
    time.sleep(5) 
		

def sincronizar_LEDs(Num_vehiculos):
    if Num_vehiculos > 5:
        temp = 25
    else:
        temp = 45
    sincronizar_trafico(temp)