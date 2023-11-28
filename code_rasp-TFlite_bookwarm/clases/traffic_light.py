import RPi.GPIO as GPIO
import time

class TrafficLights:
    def __init__(self, red_pin, amber_pin, green_pin):
        self.red_pin = red_pin # led rojo
        self.amber_pin = amber_pin # Led ambar
        self.green_pin = green_pin # Led verde
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup([self.red_pin, self.amber_pin, self.green_pin], GPIO.OUT) 

    def set_lights(self, state):
        GPIO.output(self.red_pin, state[0])
        GPIO.output(self.amber_pin, state[1])
        GPIO.output(self.green_pin, state[2])

    def traffic_light_pattern(self, num_vehicles, senal_inicio):
        if num_vehicles > 5:
            green_time = 45  
            amber_time = 5
            red_time = 50  
        else:
            green_time = 25
            amber_time = 5
            red_time = 30
        
        if senal_inicio == "rojo":
            self.set_lights([1, 0, 0])  # Red
            time.sleep(red_time)
            self.set_lights([0, 0, 1])  # Green
            time.sleep(green_time)
            self.set_lights([0, 1, 0])  # Amber
            time.sleep(amber_time)
        if senal_inicio == "green":
            self.set_lights([0, 0, 1])  # Green
            time.sleep(green_time)
            self.set_lights([0, 1, 0])  # Amber
            time.sleep(amber_time)
            self.set_lights([1, 0, 0])  # Red
            time.sleep(red_time)
        if senal_inicio == "yellow":
            self.set_lights([0, 1, 0])  # Amber
            time.sleep(amber_time)
            self.set_lights([1, 0, 0])  # Red
            time.sleep(red_time)
            self.set_lights([0, 0, 1])  # Green
            time.sleep(green_time)

    def cleanup(self):
        GPIO.cleanup()
