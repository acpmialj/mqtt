# mqtt
Pruebas de MQTT con Mosquitto. Necesitamos una red "mqttnet":
```
docker network create mqttnet
```
Usaremos varias imágenes Docker
* Una que trae preinstalado un servidor mosquitto: eclipse-mosquitto
* Otra que trae preinstalados un programa cliente-emisor MQTT (mosquitto_pub) y un programa cliente-suscriptor (mosquitto_pub): efrecon/mqtt-client
* Otra de Alpine con Python preinstalado: python:alpine3.19

## Puesta en marcha del servidor
Clonamos este repositorio y pasamos al directorio mqtt: "cd mqtt". 

En la carpeta "config" tenemos la configuración mínima para el broker. Esta carpeta estará disponible para el contenedor que ejecuta el broker. 

```shell
allow_anonymous true
listener 1883 
```
En un terminal lanzamos un contenedor basado en la imagen eclipse-mosquitto, que implementa el broker MQTT. El terminal queda asociado al servidor. 
```shell
docker run -it --rm --name mosquitto --network mqttnet -v ./config:/mosquitto/config eclipse-mosquitto

1713799126: mosquitto version 2.0.18 starting
1713799126: Config loaded from /mosquitto/config/mosquitto.conf.
1713799126: Opening ipv4 listen socket on port 1883.
1713799126: Opening ipv6 listen socket on port 1883.
1713799126: mosquitto version 2.0.18 running
```
## Lanzamos un suscriptor "universal"
En este caso usamos un contenedor con un cliente MQTT que se suscribe a *todos* los temas. Se conectará al broker usando el nombre del contenedor servidor
(mosquitto). No hace falta indicar el puerto, puesto que se usa el puerto por omisión (1883). El terminal quedará bloqueado, pero se irán volcando resultados 
correspondientes a los mensajes recibidos. 

```shell
docker run -it --rm --network mqttnet efrecon/mqtt-client mosquitto_sub -h mosquitto -p 1883 -t "#" -v
```
En la ventana del servidor, veremos "logs" de la nueva conexión:
```
1713799264: New connection from 172.21.0.3:40146 on port 1883.
1713799264: New client connected from 172.21.0.3:40146 as auto-9B619FE9-5D6D-3BBC-20CE-1BD66BD76C60 (p2, c1, k60).
```

## Lanzamos un emisor usando "mosquitto_pub" 
Lanzamos en un tercer terminal un cliente que emite un mensaje. Se conecta al puerto por omisión (1883) del broker mosquitto.

```shell
docker run -it --rm --network mqttnet efrecon/mqtt-client mosquitto_pub \
        -h mosquitto \
        -t "test/testdevice" \
        -m '[{"json":"validated","data":42},{"to":2,"test":"with"}]'
```

Y en el terminal del cliente suscriptor aparece 

```shell
test/testdevice [{"json":"validated","data":42},{"to":2,"test":"with"}]”
```

En el terminal del servidor veremos:

```shell
1713799484: New connection from 172.21.0.4:42708 on port 1883.
1713799484: New client connected from 172.21.0.4:42708 as auto-043DD009-8EE2-2C03-BD69-4CD10C89E36B (p2, c1, k60).
1713799484: Client auto-043DD009-8EE2-2C03-BD69-4CD10C89E36B disconnected.
```

Indican la conexión del emisor (líneas 1 y 2), y su posterior desconexión. 

## Enviamos mensajes usando Python
Vamos a ver un código Python que, usando la librería paho-mqtt, se conecte al servidor mosquitto y envíe un mensaje -- en este caso, un
simple string "OFF". 

Primero conseguimos un entorno de ejecución Python, en la misma red que el servidor mosquitto:

```
docker run -it --rm --network mqttnet python:alpine3.19 sh
```
El resultado del comando anterior es un contenedor basado en Alpine con Python 3.19 instalado. En dicho contenedor hemos lanzado
un shell interactivo. Desde el mismo, instalamos la librería paho:
```
/ # pip install paho-mqtt
Collecting paho-mqtt
  Downloading paho_mqtt-2.0.0-py3-none-any.whl.metadata (23 kB)
Downloading paho_mqtt-2.0.0-py3-none-any.whl (66 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 66.9/66.9 kB 2.5 MB/s eta 0:00:00
Installing collected packages: paho-mqtt
Successfully installed paho-mqtt-2.0.0
```
Hecho esto, abrimos un shell Python interactivo, que ejecutará el siguiente código:
```
import paho.mqtt.client as mqtt
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("mosquitto")
client.publish("house/main-ligth", "OFF")
```
Este es el resultado:
```
/ # python
Python 3.12.3 (main, Apr 10 2024, 04:12:22) [GCC 13.2.1 20231014] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import paho.mqtt.client as mqtt
>>> client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
>>> client.connect("mosquitto")
<MQTTErrorCode.MQTT_ERR_SUCCESS: 0>
>>> client.publish("house/main-ligth", "OFF")
<paho.mqtt.client.MQTTMessageInfo object at 0x7cd7947a9710>
>>> 
```
Nuestro contenedor-suscriptor universal indicará que ha recibido este mensaje:
```
house/main-ligth OFF
```
En vez de un string, nuestro cliente podría haber enviado un documento JSON completo. 
