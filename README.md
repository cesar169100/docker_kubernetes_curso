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

### Dockerfile

En nuestro primer dockerfile:
FROM: Especifica la imagen base que se descargara desde el registro, docker hub.
RUN: Comandos a ejecutar una vez descargue la imagen.
CMD: Comando a ejecutar por defecto cuando lancemos un container basado en esta imagen
A diferencia del comando RUN, los comandos que se pasen por medio de este método se ejecutan una vez que el contenedor se ha inicializado, mientras que RUN se utiliza para crear la imagen de un contenedor.

Comandos:
docker build ruta: Ejemplo es "docker build ." este comando construye una imagen y el punto indica el directorio donde esta el dockerfile, en este caso buscara en el directorio actual. Podria ser necesario usar "sudo" antes del comando (error raro a solucionar).
docker images : Vemos las imagenes.
docker image rm IDS: Removemos las imagenes con esos id. Tambien se pueden usar los nombres.
docker image rm IDs -f : Forza la destruccion por si alguna esta en uso.
docker build -t helloworld:1.0 . : Reetiquetar una imagen. helloworld es es nuevo tag y 1.0 el actual.

Notas:
1) Al ejecutar el build, la imagen base no aparece en la lista del comando "docker images" por alguna razon. Es por la version de docker. Para solucionar 
2) Despues de la instalacion de docker revisar la seccion "Linux post-installation steps for Docker Engine" para ejecutar los comandos docker sin sudo.