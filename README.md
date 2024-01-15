### ENTORNO
## Docker engine
1) Version de ubuntu recomendada 20.04
2) Instalar docker ce ubuntu (community edition). Poner asi en navegador y abrir la primera opcion de docker docs.
3) Hacer la purga de lo existente(todo) e instalar como viene en la guia. Para cuando se hizo este curso la version mas reciente del docker engine parecia tener problemas al descargar la imagen base del dockerfile (FROM nombre_imagen) pues al ejecutar el build a partir del dockerfile corre pero despues, al ejecutar docker images, la imagen base no aparece. No se si sea error en si, pero se quita instalando una version anterior de docker; en la misma guia dice como, definiendo un VERSION_STRING y usandolo en el comando siguiente. En este caso jalo con VERSION_STRING=5:20.10.14~3-0~ubuntu-focal
4) Podria ser necesario tambien correr el comando "systemctl start docker" pa que arranque y jalen los comandos docker.
5) En la misma guia viene que hacer si salen errores al ejecutar comandos docker sin sudo. Similar es ejecutar el comando "sudo usermod -a -G docker nombre_usuario", en mi caso, en esta lap, nombre_usuario=cesar.
## kubectl
1) Herramienta de linea de comandos para kubernetes.
2) Tipear kubectl en el navegador y elegir la primera opcion de sus docs. Elegir el sistema operativo(linux en este caso) y la opcion de instalado "using native package management".
3) Seguir el resto de la guia.
## minikube
1) Herramienta para desplegar clusters de manera local.
2) Tipear minikube y elegir minikube start de la pag oficial.
3) Opciones default. Linux, arqu de 64, version estable y con descarga de binarios.
4) A la hora de ejecutar el comando "sudo install minikube ..." la carpeta bin de la ruta /usr/local/bin podria no existir. Creala y vuelve a instalar. "sudo mkdir /usr/local/bin"
5) Podria salir una especie de warning al ejecutar comandos minikube, en este caso, Docker CLI context "default" no encontrado. Ejecuta "docker context use default"

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

Comandos:
1) docker build ruta: Ejemplo es "docker build ." este comando construye una imagen y el punto indica el directorio donde esta el dockerfile, en este caso buscara en el directorio actual.
2) docker images : Vemos las imagenes.
3) docker image rm IDS: Removemos las imagenes con esos id. Tambien se pueden usar los nombres.
4) docker image rm IDs -f : Forza la destruccion por si alguna esta en uso.
5) docker build -t helloworld:1.0 . : Reetiquetar una imagen. helloworld es es nuevo tag y 1.0 el actual.
6) docker ps :Containers activos
7) docker ps -a :Cualquier container activo o detenido.
8) docker create imagen:TAG  :Crea el container con el nombre que tiene la imagen y su tag. Solo se crea pero no se arranca.
9) docker start container_id,nombre :Arranca el container. Pasa a status Up.
10) docker stop container_id  :Se detiene. Pasa a estatus exit.
11) docker rm container_id -f :Elimina el container. La f es igual para el forzado.
12) docker inspect image_id, container_id :Nos da info sobre la imagen o container.
13) docker create -p 8080:80 --name "nombre" image_id :Este comando crea nuestro container a partir de la imagen indicada, con el nombre que queramos y mapeando el puerto 80(en el que respnde nginx y es el puerto del container) al 8080 de nuestra maquina.
14) docker create -P --name "nombre" image_id :En este comando ya no fue necesario poner el puerto de el container(80) pues se especifico con el expose del dockerfile. Tambien mapea ese puerto en uno local, que es parte de un conjunto de puertos que se conocen como efimeros y estan definidos en algun lugar, el punto es que se elijen al azar de un rango y no es necesario preocuparse por saber cuales de nuestros puertos locales ya estan ocupados pues lo va a mandar automaticamente a uno libre de ese rango.

Notas:
1) Con docker inspect, en el bloque de NetworkSettings hay un campo que se llama IPAddress. Esta IP es la asociada a nuestro container. Si la pones en el navegador entras a tu container.
Hacer peticiones a esta IP es incorrecto pues si vuelves a levantar el container la IP puede cambiar, es decir, esta IP es efimera.
2) Para poder acceder correctamente a los puertos de un container podemos "mapear" los puertos, por ejemplo, el puerto 80 en el que responde nginx este mapeado a un puerto fijo de nuetra maquina. Revisar comando docker create. Asi, ya no importa cuantas veces levantemos el container, si especificamos el mapeo en el comando podremos acceder.