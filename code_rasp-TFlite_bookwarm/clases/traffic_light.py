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

    def traffic_light_pattern(self, num_vehicles):
        if num_vehicles > 5:
            transition_time = 45
        else:
            transition_time = 25

        return transition_time

    def cleanup(self):
        GPIO.cleanup()
        GPIO.cleanup()