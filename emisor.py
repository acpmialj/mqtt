$ python3
Python 3.10.6 (main, Aug 10 2022, 11:40:04) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import paho.mqtt.client as mqtt
>>> broker_address="172.17.0.2"
>>> client.connect(broker_address)
0
>>> client.publish("house/main-ligth", "OFF")
<paho.mqtt.client.MQTTMessageInfo object at 0x7f435d60af20>
>>> 
