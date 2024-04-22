import paho.mqtt.client as mqtt
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("mosquitto")
client.publish("house/main-ligth", "OFF")
