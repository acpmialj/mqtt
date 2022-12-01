# mqtt
Pruebas de MQTT con Mosquitto

En la carpeta "config" tenemos la configuración mínima para el broker. Esta carpeta estará disponible para el contenedor que ejecuta el broker. 

```shell
allow_anonymous true
port 1883 
```

## Ejecución

En un terminal lanzamos un contenedor basado en la imagen eclipse-mosquitto, que implementa el broker MQTT. El terminal queda asociado al servidor. 
```shell
docker run -it --rm -p 1883:1883 -v $HOME/mqtt/config:/mosquitto/config --ip 172.17.0.2 eclipse-mosquitto 
1666781743: The 'port' option is now deprecated and will be removed in a future version. Please use 'listener' instead. 
1666781743: mosquitto version 2.0.15 starting 1666781743: Config loaded from /mosquitto/config/mosquitto.conf. 
1666781743: Opening ipv4 listen socket on port 1883. 
1666781743: Opening ipv6 listen socket on port 1883. 
1666781743: mosquitto version 2.0.15 running 
1666781757: New connection from 172.17.0.1:32814 on port 1883. 
1666781757: Client <unknown> closed its connection. 
```

En otro terminal comprobamos (desde el host) que el servidor está operativo: 

```shell
nc -zv 172.17.0.2 1883 Connection to 172.17.0.2 1883 port [tcp/*] succeeded! 
```

## Lanzamos un suscriptor

En este caso usamos un contenedor con un cliente MQTT que se suscribe a *todos* los temas. El terminal quedará bloqueado

```shell
docker run -it --rm efrecon/mqtt-client sub \
        -h 172.17.0.2 \
        -t "#" \
        -v
```

## Lanzamos en otro terminal un cliente que emite un mensaje

```shell
docker run -it --rm efrecon/mqtt-client pub \
        -h 172.17.0.2 \
        -p 1883 \
        -t "test/testdevice" \
        -m '[{"json":"validated","data":42},{"to":2,"test":"with"}]'
```

Y en el terminal del cliente suscrito aparece 

```shell
test/testdevice [{"json":"validated","data":42},{"to":2,"test":"with"}]”
```

En el terminal del servidor veremos:

```shell
1666781985: New connection from 172.17.0.3:56512 on port 1883.
1666781985: New client connected from 172.17.0.3:56512 as auto-870A7ED8-9A87-EBD5-99B5-2B70F942767E (p2, c1, k60).
1666782072: New connection from 172.17.0.4:43678 on port 1883.
1666782072: New client connected from 172.17.0.4:43678 as auto-D0226ACE-0F62-1271-DD9F-9FE11AB37186 (p2, c1, k60).
1666782072: Client auto-D0226ACE-0F62-1271-DD9F-9FE11AB37186 disconnected.
```

1. Líneas 1 y 2: conexión del oyente
2. Líneas 3, 4 y 5: conexión del emisor, y desconexión inmediata

## Extras

También se puede instalar en el host "sudo apt-get install mosquitto-clients", mosquitto clients. Su uso para publicar (enviar) es sencillo

```shell
mosquitto_pub -d -q 1 -h "localhost" -p "1883" -t "v1/devices/me/telemetry" -u "ABC123" -m {"temperature":25}
```

Donde "-h localhost" es la dirección o nombre del broker, "-p 1883" es su puerto, "-t xxx" es el tema, "-u xxx" es el usuario y "-m xxx" es el mensaje, en esta caso un texto JSON. El contenedor publicador de arriba tiene simplemente un alias de "mosquitto_pub" a "pub".  

