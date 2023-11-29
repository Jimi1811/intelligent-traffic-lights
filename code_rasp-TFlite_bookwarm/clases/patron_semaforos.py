import RPi.GPIO as GPIO
import time
from traffic_light import TrafficLights
from camera import Num_vehiculos

if __name__ == "__main__":
    traffic_lights_1 = TrafficLights(red_pin=17, amber_pin=27, green_pin=22)  # Definir los pines para el primer semáforo
    traffic_lights_2 = TrafficLights(red_pin=23, amber_pin=24, green_pin=25)  # Definir los pines para el segundo semáforo

    while True:
        try:
            transition_time = traffic_lights_1.traffic_light_pattern(Num_vehiculos)
            traffic_lights_1.set_lights([1, 0, 0])  # Red
            traffic_lights_2.set_lights([0, 0, 1])  # Green
            time.sleep(transition_time)
            traffic_lights_1.set_lights([1, 0, 0])  # Red
            traffic_lights_2.set_lights([0, 1, 0])  # Ambar
            time.sleep(5)
            traffic_lights_1.set_lights([0, 0, 1])  # Grenn
            traffic_lights_2.set_lights([1, 0, 0])  # Red
            time.sleep(transition_time)
            traffic_lights_1.set_lights([0, 1, 0])  # Ambar
            traffic_lights_2.set_lights([1, 0, 0])  # Red
            time.sleep(5)
        
        except:
            break

        finally:
            traffic_lights_1.cleanup()
            traffic_lights_2.cleanup()