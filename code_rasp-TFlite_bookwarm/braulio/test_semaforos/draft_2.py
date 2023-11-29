import RPi.GPIO as GPIO
import time
from traffic_light import TrafficLights

global nivel

if __name__ == "__main__":
    traffic_lights_1 = TrafficLights(red_pin=17, amber_pin=27, green_pin=22)  # Definir los pines para el primer semáforo
    traffic_lights_2 = TrafficLights(red_pin=23, amber_pin=24, green_pin=25)  # Definir los pines para el segundo semáforo

    semaforo_1 = "rojo"
    semaforo_2 = "verde"

    while True:
        try:
            if nivel == "bajo":
                trans_time_1 = 30
                trans_time_2 = 30
            elif nivel == "medio":
                trans_time_1 = 40
                trans_time_2 = 20
            elif nivel == "alto":
                trans_time_1 = 50
                trans_time_2 = 10

            print(nivel)
            print(trans_time_1)
            print(trans_time_2)

            traffic_lights_1.set_lights([1, 0, 0])  # Red
            semaforo_1 = "rojo"
            traffic_lights_2.set_lights([0, 0, 1])  # Green
            semaforo_2 = "verde"
            time.sleep(trans_time_1)
            traffic_lights_1.set_lights([1, 0, 0])  # Red
            semaforo_1 = "rojo"
            traffic_lights_2.set_lights([0, 1, 0])  # Ambar
            semaforo_2 = "ambar"
            time.sleep(3000)
            traffic_lights_1.set_lights([0, 0, 1])  # Green
            semaforo_1 = "verde"
            traffic_lights_2.set_lights([1, 0, 0])  # Red
            semaforo_2 = "rojo"
            time.sleep(trans_time_2)
            traffic_lights_1.set_lights([0, 1, 0])  # Ambar
            semaforo_1 = "ambar"
            traffic_lights_2.set_lights([1, 0, 0])  # Red
            semaforo_2 = "rojo"
            time.sleep(3000)
        
        except:
            break

        finally:
            traffic_lights_1.cleanup()
            traffic_lights_2.cleanup()
