import time
import paho.mqtt.client as mqtt
import random

hostname ="localhost"
broker_port = 1883
topic = "mqtt/rpi"


client = mqtt.Client() 
#generate a random number as message payload
message = str(random.randint(1, 100))
client.publish(topic, message)
client.connect(hostname, broker_port, 60)
