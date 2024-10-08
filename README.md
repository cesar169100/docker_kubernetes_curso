### ENTORNO
## Docker engine
1) Version de ubuntu recomendada 20.04
2) Instalar docker ce ubuntu (community edition). Poner asi en navegador y abrir la primera opcion de docker docs.
3) Hacer la purga de lo existente(todo) e instalar como viene en la guia. Para cuando se hizo este curso la version mas reciente del docker engine parecia tener problemas al descargar la imagen base del dockerfile (FROM nombre_imagen) pues al ejecutar el build a partir del dockerfile corre pero despues, al ejecutar docker images, la imagen base no aparece. No se si sea error en si, pero se quita instalando una version anterior de docker; en la misma guia dice como, definiendo un VERSION_STRING y usandolo en el comando siguiente. En este caso jalo con VERSION_STRING=5:20.10.14~3-0~ubuntu-focal
4) Podria ser necesario tambien correr el comando "systemctl start docker" pa que arranque y jalen los comandos docker.
5) En la misma guia viene que hacer si salen errores al ejecutar comandos docker sin sudo. Similar es ejecutar el comando "sudo usermod -a -G docker nombre_usuario", en mi caso, en esta lap, nombre_usuario=cesar.
6) Otros comandos que no esta de mas correr:
sudo chmod 666 /var/run/docker.sock
## kubectl
1) Herramienta de linea de comandos para kubernetes.
2) Tipear kubectl en el navegador y elegir la primera opcion de sus docs. Elegir el sistema operativo(linux en este caso), elige la version que desees (parte de arriba, versions) y la opcion de instalado "using native package management".
3) Seguir el resto de la guia.
## minikube
1) Herramienta para desplegar clusters de kubernetes de manera local.
2) Tipear minikube y elegir minikube start de la pag oficial.
3) Opciones default. Linux, arqu de 64, version estable y con descarga de binarios.
4) A la hora de ejecutar el comando "sudo install minikube ..." la carpeta bin de la ruta /usr/local/bin podria no existir. Creala y vuelve a instalar. "sudo mkdir /usr/local/bin"
5) Verifica con el comando "minikube version", podria salir una especie de warning al ejecutarlo, en este caso, Docker CLI context "default" no encontrado. Ejecuta "docker context use default"

Notas:
1) Al ejecutar el build, la imagen base no aparece en la lista del comando "docker images" por alguna razon. Es por la version de docker. Esto ya se soluciono.
2) Despues de la instalacion de docker revisar la seccion "Linux post-installation steps for Docker Engine" para ejecutar los comandos docker sin sudo.

### Dockerfile

En nuestro primer dockerfile:
FROM: Especifica la imagen base que se descargara desde el registro, docker hub.
RUN: Comandos a ejecutar una vez descargue la imagen. Pueden ser muchos.
EXPOSE:El puerto que pongas aqui sera el puerto principal del container y se guardara en los metadatos de la imagen (docker inspect). En los comandos posteriores ya no es necesario especificarlo, esa es la ventaja de ponerlo aqui.
CMD: Comando a ejecutar por defecto cuando lancemos un container basado en esta imagen
A diferencia del comando RUN, los comandos que se pasen por medio de este método se ejecutan una vez que el contenedor se ha inicializado, mientras que RUN se utiliza para crear la imagen de un contenedor.

### Primeros comandos

Comandos:
1) docker build ruta: Ejemplo es "docker build ." este comando construye una imagen y el punto indica el directorio donde esta el dockerfile, en este caso buscara en el directorio actual.
2) docker images : Vemos las imagenes.
3) docker image rm IDS: Removemos las imagenes con esos id. Tambien se pueden usar los nombres.
4) docker image rm IDs -f : Forza la destruccion por si alguna esta en uso.
4) docker image remove -f $(docker images -a -q): borra todas las imagenes.
5) docker build -t helloworld:1.0 . : Reetiquetar una imagen. helloworld es es nuevo tag y 1.0 el actual.
6) docker ps :Containers activos
7) docker ps -a :Cualquier container activo o detenido.
8) docker create imagen:TAG  :Crea el container con el nombre que tiene la imagen y su tag. Solo se crea pero no se arranca.
9) docker start container_id,nombre :Arranca el container. Pasa a status Up.
10) docker stop container_id  :Se detiene. Pasa a estatus exit.
11) docker rm container_id -f :Elimina el container. La f es igual para el forzado.
12) docker rm -v -f $(doker ps -qa) : Borra todos los containers detenidos o no.
12) docker inspect image_id, container_id :Nos da info sobre la imagen o container.
13) docker create -p 8080:80 --name "nombre" image_id :Este comando crea nuestro container a partir de la imagen indicada, con el nombre que queramos y mapeando el puerto 80(en el que respnde nginx y es el puerto del container) al 8080 de nuestra maquina.
14) docker create -P --name "nombre" image_id :En este comando ya no fue necesario poner el puerto de el container(80) pues se especifico con el expose del dockerfile. Tambien mapea ese puerto en uno local, que es parte de un conjunto de puertos que se conocen como efimeros y estan definidos en algun lugar, el punto es que se elijen al azar de un rango y no es necesario preocuparse por saber cuales de nuestros puertos locales ya estan ocupados pues lo va a mandar automaticamente a uno libre de ese rango.
15) docker exec -it container_id,nombre bash :Con este comando entramos a la consola bash del container. En esta consola se pueden ejecutar comandos normales por ejemplo de instalacion apt update etc. Si paras y reinicias el container los datos seguiran ahi pero si lo eliminas pues no.
16) docker exec container_id,nombre bash -c "comando a ejecutar" :Con este comando puedes ejecutar el "comando a ejecutar" en la consola del container en idioma bash sin tener que entrar a su consola con el comando anterior.
17) Existen contenedores basados en ciertas imagenes como python o python slim que no pueden mntenerse en ejecucion, por lo cual no podras entrar a la consola bash de este container. Entonces para estos casos no descargues la imagen ni nada y directamente ejecuta: 
docker exec -it --name "nombre_del_container" "imagen" /bin/bash donde imagen puede ser pyhon:3.9 por ejemplo

Notas:
1) Con docker inspect, en el bloque de NetworkSettings hay un campo que se llama IPAddress. Esta IP es la asociada a nuestro container. Si la pones en el navegador entras a tu container.
Hacer peticiones a esta IP es incorrecto pues si vuelves a levantar el container la IP puede cambiar, es decir, esta IP es efimera.
2) Para poder acceder correctamente a los puertos de un container podemos "mapear" los puertos, por ejemplo, el puerto 80 en el que responde nginx este mapeado a un puerto fijo de nuetra maquina. Revisar comando docker create. Asi, ya no importa cuantas veces levantemos el container, si especificamos el mapeo en el comando podremos acceder.

### Volumenes

Recordemos que cualquier cosa que hayamos creado en un container solo estara ahi mientras el container viva. Si creamos una carpeta, instalamos algo, etc, esto desaparece si matamos al container. Para dar persistencia (no se pierdan los datos), podemos hacer uso de un sistema de volumenes en docker.

1) Sistema bind mount: Ya no se usa. Consiste en crear un container cuyo volumen(lo que tiene dentro) o dirctorio en especifico venga ligado a un directorio de la maquina donde estemos corriendo este container. Para entornos prod no se recomienda, es mejor el sistema de volumenes.
2) Sistema de volumenes: Son mas faciles de migrar pues no estan ligados a ruta local. Se pueden manejar con comandos docker. Funcionan en containers de linux y windows. Son mas seguros de compartir entre containers. Mejor rendimiento.
3) No se elimina un volumen que este siendo usado por un container. Primero elimina el container.
4) Kubernetes tiene un mejor sistema de volumenes.

Comandos:
1) docker create --name "nombre_container" --mount type=bind,source="$(pwd)/src",target=/src image_id  :Crea el container con el nombre y toma lo que exista en nuestra ruta local pwd(directorio actual)/src y lo monta  en la carpeta /src del container. Ahora, si creamos un nuevo archivo dentro de la carpeta /src del container y luego lo matamos, este nuevo archivo existira en nuestra carpeta local tambien,de manera que si levantamos de nuevo el container tendrmos nuestro nuevo archivo ahi.
2) docker volume ls :Lista de volumenes.
3) docker volume create "nombre_volumen" :Creas un volumen.
4) docker volume inspect "volume_name" :Datos del volumen. Entre ellos, viene la ruta local donde se almacenan los volumenes. A esta ruta solo podemos acceder como root (escribir sudo su y entraremos a nuestra consola como root). Damos cd para ponernos al inicio y luego cd y la ruta que aparece en el inspect y ahi veremos nuestro volumen.
5) docker volume rm "nombre_volumen" :Lo elimina
6) docker volume prune :Los elimina todos.
7) docker create --name "nombre_container" --mount source="mivolumen",target=/app image_id :Similar al primer comando.
8) docker create --name "nombre_container" -v "mivolumen":/app image_id :Aun mas simple. Solo se especifica el nombre de nuestro volumen y la carpeta destino del container

### Configuracion de red con Docker Network

Existen drivers de red que nos proporcionan funcionalidades basicas. Al igual que el caso anterior, kubernetes tiene mejores opciones.
Driver: Basicamente provee de las insturcciones necesarias al sistema operativo para saber cómo comunicarse con este nuevo dispositivo.
Estos son los drivers de red para funcionalidades de nuestros contenedores:
1) bridge :Permiten a los containers tener subred dedicada y obtendran IPs de esa red para comunicarse entre ellos. Estaran aislados del host (nuestra compu)
2) host: Ya no se aislan del host, obtienen una IP directa de la red del host.
3) overlay : Para clusters.

Comandos:
1) docker network ls :Las redes por defecto (bridge, host)
2) docker network create --driver "tipo_driver" "nombre" :Crea una network con el driver especificado (bridge, host, etc) y su nombre que le queramos dar.
3) docker inspect "network_name" :Datos de la network. En particular se ve el driver y su subnet. Cualquier container que lanzaramos dentro de este network se lanzara con una de esas IPs del subnet.
4) docker create --name "container_name" --network "network_name" image_id :Crea el container en esa network y tendra la ip correspondiente a la subnet de la network.
5) docker network rm "net1","net2",...  :Elimina las networks.

### Docker Hub
1) docker login / sudo docker login :Para acceder a nuestra cuenta de DockerHub, subir nuestras imagenes locales, etc.
2) docker tag imagename:TAG newname:newTAG :Crea una copia de una imagen con un nuevo nombre y tag.
3) sudo docker push cesar169/helloworld:tagname :Sube una imagen a nuestro repo de docherhub. Debe tener el nombre de nuestro usuario/repo/tag
4) docker pull cesar169/helloworld:tagname :Jala esta imagen del repo.

### Variables de entorno
Comandos:
1) docker create -e variable1=db.midominio -e variable2=miusuario -e variable3=mipass --name c1 image_id :En este comando especificas con e las variables de entorno. Al iniciar el container y acceder a su terminal, con el comando env en este caso pues el container es ubuntu, podremos ver las variables. Puedes especificar tantas variables como desees.

### Supervisor
Sistema de monitorizacion y control de procesos en linux. Revisar despues, no le entiendo.

### Ciclo vida container
1) Creado  :docker create ...
2) running :docker start container_id, name
3) paused  :docker pause ..................
4) stopped : docker stop container_id, name
5) deleted :docker rm .....................

Comandos extra:
1) docker restart container_id, name :Lo para y reinicia.
2) docker unpause .................. :Quita la pausa.
3) El container tambien puede morir si se queda sin memoria o da error, salvo en el caso que no tengamos una condicion de restart.
4) docker run --name nombre -P -e var1=mivar1 .... -d image_id :Crea y corre de una.

### Restart policies
Estas politicas permiten controlar si los contenedores arrancaran de manera automatica o cuando docker reinicie. Aseguran que los containers vinculados se inicien en el orden correcto.

Tipos de reinicio. Se especifican con el comando --restart
1) no :No hay reinicio automatico(default)
2) on-failure[:max-retries] :Reinicia si se detiene por un error que no sea una salida con estado zero. Opcional se puede limtar el numero de reinicios.
3) always :Siempre reinicia si se detiene. Si es manualmente detenido solo reinicia cuando el docker daemon reinicia o cuando el container es manualmente reiniciado.
4) unless-stopped :Como always solo que cuando el container sea detenido manual entonces no reiniciara.

Notas:
1) Si ponemos la opcion --restart always y despues ejecutamos para ver la terminal (docker exec -it container_id bash) y ponemos ps aux veremos nuestro container corriendo. Si damos kill al PID del container (kill 1, kill 2, etc) lo matara y volvera a levantarse de inmediato. Lo anterior se ve al ejecutar docker ps -a de nuevo y dira up to n seconds/minutes, un tiempo mas reciente que el inicial, pues.

Comando ejemplo:
1) docker create --name c1 -p 8080:80 --restart always image_id
2) docker update --restart unless-stopped container_id :Este comando actualiza el metodo de reinicio de un container que ya esta corriendo. Lo actualiza del metodo que tenga al nuevo que es unless-stopped.

### Otros comandos
1) docker commit container_id,nombre imagen:TAG :Este comando crea una nueva imagen a partir de un container existente. Supon que tienes un container en el que hiciste cambios y creaste cosas, entonces puedes replicar esto y hacerlo una nueva imagen para seguir usandola sin tener que estar haciendo los movimientos otra vez. No es la mejor practica, mejor incluye todas las indicaciones en el dockerfile.
2) docker :Muestra todos los comandos disponibles. Si anadimos --help nos dira como usarlo.
3) docker logs container_id,nombre :Los logs de un container.
4) docker rename nombre_container nombre_container2 :Renombra container
5) docker top container_id,nombre :Procesos en el container corriendo. 