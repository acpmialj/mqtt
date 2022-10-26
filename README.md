# mqtt
MQTT testing with mosquitto

A configuration file is required in ~/mqtt/config
allow_anonymous true
port 1883 

## Run the server with:
docker run -it --rm -p 1883:1883 -v $HOME/mqtt/config:/mosquitto/config --ip 172.17.0.2 eclipse-mosquitto 
1666781743: The 'port' option is now deprecated and will be removed in a future version. Please use 'listener' instead. 
1666781743: mosquitto version 2.0.15 starting 1666781743: Config loaded from /mosquitto/config/mosquitto.conf. 
1666781743: Opening ipv4 listen socket on port 1883. 
1666781743: Opening ipv6 listen socket on port 1883. 
1666781743: mosquitto version 2.0.15 running 
1666781757: New connection from 172.17.0.1:32814 on port 1883. 
1666781757: Client <unknown> closed its connection. 

En otra ventana se comprueba que funciona 
ubuntu@ubuntu-2204:~/mqtt$ nc -zv 172.17.0.2 1883 Connection to 172.17.0.2 1883 port [tcp/*] succeeded! 


## Lanzamos un suscriptor:
docker run -it --rm efrecon/mqtt-client sub \
        -h 172.17.0.2 \
        -t "#" \
        -v
## Lanzamos un cliente que emite un mensaje:
docker run -it --rm efrecon/mqtt-client pub \
        -h 172.17.0.2 \
        -p 1883 \
        -t "test/testdevice" \
        -m '[{"json":"validated","data":42},{"to":2,"test":"with"}]'

Y en el terminal del cliente suscrito aparece 
“test/testdevice [{"json":"validated","data":42},{"to":2,"test":"with"}]”

En el terminal del servidor veremos:
1666781985: New connection from 172.17.0.3:56512 on port 1883.
1666781985: New client connected from 172.17.0.3:56512 as auto-870A7ED8-9A87-EBD5-99B5-2B70F942767E (p2, c1, k60).
1666782072: New connection from 172.17.0.4:43678 on port 1883.
1666782072: New client connected from 172.17.0.4:43678 as auto-D0226ACE-0F62-1271-DD9F-9FE11AB37186 (p2, c1, k60).
1666782072: Client auto-D0226ACE-0F62-1271-DD9F-9FE11AB37186 disconnected.

Líneas 1 y 2: conexión del oyente
Líneas 3, 4 y 5: conexión del emisor, y desconexión inmediata




