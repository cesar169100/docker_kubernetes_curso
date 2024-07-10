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
- Nodos de Trabajo(workers): Ejecutan las aplicaciones en contenedores. Cada nodo contiene el runtime de contenedores y componentes de Kubernetes que permiten ejecutar y gestionar contenedores.

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
Unable to load cached images: loading cached images: stat /home/cesar/.minikube/cache/images/amd64/registry.k8s.io/kube-proxy_v1.22.6: no such file or directory

# Video 24: Configurar el cluster
- minikube config: Subcomandos para la configuracion
- minikube config view: Muestra los cambios al archivo de configuracion de minikube
- minikube config set campo_configurable valor: Por ejemplo minikube config set kubernetes-version v1.22.6, establece un valor
- Ahora si das minikube start hara la descarga con las configuraciones especificadas
# Video 25: Multiples clusters usando perfiles y minikube kubectl
- Un perfil es una configuración aislada de un clúster de Minikube que permite tener múltiples clústeres con diferentes configuraciones en una misma máquina. Cada perfil puede tener su propio conjunto de recursos y configuraciones, facilitando la gestión y pruebas de diferentes entornos de clúster.
- rm -rf .minikube/ : Correr desde /home/cesar para eliminar este directorio y empezar de nuevo el proceso de descarga de imagenes. Tambien se borran los cambios en el config
- minikube profile list: Lista de los perfiles que hay, debe existir al menos un cluster para que exista un perfil.
- minikube start -p nombre_perfil: Nos levantaria otro cluster con las mismas caracteristicas de nuestro config pero bajo otro perfil. Ej. minikube start -p perfil-1
- minikube start -p nombre_perfil --kubernetes-version=v1.24.0 : Se pueden especificar otros parametros.
- minikube delete -p nombre_perfil : Borra los clusters asociados a ese perfil
- minikube -p nombre_perfil kubectl get nodes: Baja la version que corresponda de kubectl a ese entorno en especifico de nuestro perfil. Las versiones de kubectl tambien cambian dependiendo de que version de kubernetes tengas.
- minikube profile profile_name : Cambiar de perfil/cluster
# Video 26: Manifest vs comandos - Configuracion declarativa vs imperativa
- En un clúster de Kubernetes siempre hay una API server en funcionamiento. Esta API server es responsable de recibir y procesar todas las solicitudes de administración del clúster. Las herramientas como kubectl envían comandos y consultas a esta API server para gestionar y operar el clúster, como desplegar aplicaciones, escalar nodos y monitorear el estado de los recursos.
- Configurar recursos de manera declarativa: Hacer un fichero(un yml) de configuracion al que vamos a llamar manifest.
- kubectl get all: Lista los objetos que existan en el espacio de nombres en el que estamos trabajando. Mas adelante se definira lo que es un espacio de nombres, pero sirven para aislar recursos. Hay un espacio deafult que existe si no se crea ninguno adicional. Si ejecutas este comando aparecera un objeto de tipo servicio que se llama kubernetes, con una IP y sirve para que cualquier cosa que este desplegada en este cluster pudiera atacar(recibir y procesar solicitudes) a la appi de kubernetes desde dentro del propio cluster.
- kubectl get namespaces: Lista los espacios de nombres
- kubectl apply -f archivo.yml : Aplica las configuraciones, crea cosas, levanta containers segun el archivo yml. Mas adelante se veran ejemplos de este archivo.
- kubectl delete archivo.yml :Se elimina lo desplegado o creado a traves del manifest. Lo que existia antes no.
- Manera imperativa: A traves de comando directo.
- kubectl create deployment --image=nginx:latest --replicas=2 pruebas Crea un deploy que se llama pruebas con esas caracteristicas.
- kubectl delete deployment pruebas : Se elimina un objeto deployment llamado pruebas
# Video 27: Pods
- Un pod es una abstraccion de kubernetes para indicar uno o varios contenedores que se van a ejecutar juntos/agrupados compartiendo almacenamiento, red y especificaciones de como se van a ejecutar. Un pod es la unidad básica de ejecución en Kubernetes. Es el contenedor más pequeño y simple en el que Kubernetes despliega aplicaciones. Cada pod puede contener uno o más contenedores que comparten la misma red y almacenamiento, y están diseñados para ser ejecutados juntos como una única aplicación. Los pods encapsulan los recursos de la aplicación y la configuración necesaria para su ejecución.
- Kubernetes tiene un scheduler que es uno de los componentes que se va a encargar de encontrar el nodo de tipo worker donde va a lanzar este pod y asignarselo para que ejecute ahi el pod. Optimiza el uso de los recursos
- El codigo pod.yaml se desarrolla en este video
- kubectl get all -o wide :  Nos da info adicional al comando sencillo. Nos da la Ip que internamente se asigna para acceder a este servicio, en que nodo se ejecuta (parece ser igual al nombre del perfil)
- kubectl get pod : Solo los pods
- kubectl describe pod pod_name : Describe el pod.
- NOTA: Un namespace en Kubernetes es una forma de dividir un único clúster Kubernetes en varios entornos virtuales. Cada namespace proporciona un espacio de nombres aislado para recursos. Uso: Gestiona recursos dentro de un clúster compartido, proporcionando aislamiento y organización para diferentes equipos o proyectos. En resumen, un perfil es para gestionar múltiples clústeres en Minikube, mientras que un namespace es para organizar recursos dentro de un solo clúster Kubernetes.
# Video 28: Metadata, Labels y Selectors