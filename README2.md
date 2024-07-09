# Docker compose
docs.docker.com/compose
En la anterior ver los dos comandos de instalacion en standalone. El segundo comando es para permisos de ejecucion y en el momento de este tutorial, no estaba en los docs:
sudo chmod +x /usr/local/bin/docker-compose
# Notas
1) docker-compose ya crea una red interna de docker, por lo que los containers de ahi estaran comunicados.
2) docker-compose down : Para y elimina containers existentes
3) Los comandos como el de arriba solo funcionan si estas parado en el directorio donde esta tu docker-compose.yml
4) docker-compose up -d nos permite seguir usando la terminal y con docker-compose logs pues vemos los logs
5) Revisar los compose de ejemplo en la carpeta docker_compose_examples
6) NOTA IMPORTANTE: Cuando construimos una imagen esta se construye segun la arquitectura del equipo en el que la hicimos. En este caso mi equipo tiene arquitectura amd64 de Intel con linux (tipear uname -a en la terminal para ver), pero tambien hay otras arquitecturas como la arch64. Si subimos una imagen a dockerhub esta se guardara con su arquitectura, supongamos amd64, si despues queremos descargar esta imagen desde dockerhub a un equipo o instancia con arquitetura arch64 entonces no correra en este equipo. Consejo: crea una version de tu imagen para cada arquitectura en la que creas que puede correr. Las MAC y Raspberrypy suelen tener arquitecturas arch/arm (lo mismo)

### Kubernetes con Minikube
# Video 22: Presentacion
Configurar cluster de kubernetes de manera local, en vez e la nube pues eso acarrea costos y es lento.
# Video 23: Cluster local en minikube
Un clúster de Kubernetes es un conjunto de máquinas (físicas o virtuales) que trabajan juntas para ejecutar aplicaciones en contenedores. Está compuesto por:
- Nodo Maestro: Gestiona el clúster, maneja la programación de contenedores, la administración  de estado y la coordinación de nodos.
- Nodos de Trabajo: Ejecutan las aplicaciones en contenedores. Cada nodo contiene el runtime de contenedores y componentes de Kubernetes que permiten ejecutar y gestionar contenedores.

Juntos, estos nodos proporcionan una plataforma escalable y flexible para ejecutar, gestionar y automatizar el despliegue de aplicaciones en contenedores.
1) Tipear minikube start --help Aqui apareceran muchas cosas entre ellas --kubernetes-version, aqui se especifica las versiones disponibles de kubernetes. La ultima podria no tener soporte en aws o en la nube que uses, por lo tanto debemos elegir una que tenga soporte. Actualmente cuentan con soporte de la 1.26 a la 1.30, y con soporte extendido de la 1.23 a 1.25. Elegimos la 1.22.6: minikube start --kubernetes-version=v1.22.6 pues es la del curso
2) minikube start --kubernetes-version=v1.22.6 Descarga la imagen de kubernetes y crea el cluster local con el tamano estandar
3) Despues de que se descargo kubernetes debe existir en /home/cesar una carpeta llamada ./kube con un archivo config. Si das cat config veras el archivo que es el archivo de configuracion que define como conectarse al cluster
4) Tenemos ahora dos comandos: minikube que permite gestionar este cluster local y kubectl que nos permite conectarnos al cluster, es la linea de comandos de kubernetes. 
- minikube status: status del cluster
- minikube ip: ip de acceso a nuestro cluster local
- minikube stop: Para los containers ligados a este cluster. Si damos docker ps -a veremos el container de minikube en status stopped. (No le muevas a este container)
- minikube start: Echarlo andar de nuevo
- minikube delete: Elimina el cluster pero no la imagen. Al dar docker start de nuevo no descargara la iamgen otra vez.
- minikube addons list: Lista de los addons de minikube. Funcionalidades que en otro tipo de cluster(no local como este) tendriamos que instalar a mano o usando otras herramientas. Como herramientas de monitoreo, gestión de contenedores, dashboards, entre otros. 
- minikube addons enable nombre_addon: Por ejemplo, minikube addons enable dashboard, instala ese addon. 
- minikube dashboard: Abres la interfaz de kubernetes
- minikube ssh: Se conecta via ssh al container, maquina virtual, etc
- kubectl get nodes: Comando de kubernetes. Lista de los nodos del cluster
# Video 24: Configurar el cluster

Unable to load cached images: loading cached images: stat /home/cesar/.minikube/cache/images/amd64/registry.k8s.io/kube-proxy_v1.22.6: no such file or directory