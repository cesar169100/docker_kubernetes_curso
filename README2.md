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
- Mismo codigo (pod.yaml) que el video anterior.
- Los selectors nos permiten hacer referencia a un objeto de kubernetes usando etiquetas en vez de su nombre.
- kubectl get pods --selector project=pagina_web : Busca los pods donde exista una etiqueta project con el vlor pagina_web y asi en vez de project se puede usar cualquier etiqueta que le hayamos definido
- kubectl get pods --selector 'project in (pagina_web, otra_cosa)' : uno mas complejo, estos querys tambien aplican si es un get all.
# Video 29: Reinicio de un Pod y Exec
- Si lanzamos un pod con su contenedor y el proceso principal del contenedor muere o termina lo que iba a hacer, kubernetes podria intentar arrancarlo otra vez. Se recomienda crear un objeto que compruebe esas replicas, compruebe si esta vivo, elimine el pod y lo vuelva a crear si no esta "sano" y esos objetos se veran mas adelante. 
- Supon que arrancas un pod con su manifest (kubectl apply -f pod.yaml), entonces como nos conectamos o ejecutamos un comando dentro de este pod? :
kubectl exec nombre_pod comando : kubectl exec nginx ls (muestra los archivos)
kubectl exec nombre_pod -c container_name comando : En caso de q nuestro pod tenga mas de un container.
- kubectl -it exec pod_name bash : Abre la terminal del container. kubectl -it exec nginx bash
- Recuerda que aqui aun no hay persistencia. Si creas un pod con un container(o mas), e instalas cosas y borras el pod tons todo se pierde.
- Cada vez que kubernetes mediante el sheduler intenta levantar un pod de nuevo lo crea desde cero pero tiene criterios de tiempo para tardarse mas a cada intento.
# Video 30: Replication Controller
- Controlar el numero de replicas que van a correr de un pod. Se asegura que un pod o un grupo homogeneo de estos este siempre corriendo y disponible. Componente de Kubernetes que asegura que un número específico de réplicas de un pod esté ejecutándose en todo momento. Monitorea los pods y, si alguno falla o es eliminado, crea nuevos pods para mantener el número deseado de réplicas. Ayuda a gestionar la escalabilidad y disponibilidad de las aplicaciones en un clúster de Kubernetes.
- El codigo de este video esta en /manifest_examples/replication_controller.yaml
- kubectl get rc : Vemos nuestros objetos tipo replication controller (rc)
- kubectl describe rc nombre_rc : Describe el rc
# Video 31: Replicaset
Es lo mismo que el replication controller solo que Utiliza un selector de etiquetas más flexible que soporta expresiones de igualdad e inigualdad y ReplicaSet ofrece mayor flexibilidad y es la opción recomendada en versiones actuales de Kubernetes.
- El codigo del video es /manifest_examples/replicaset.yaml
- kubectl get rs : Lista de los replicaset
# Video 32: Namespaces
- Un namespace en Kubernetes es una forma de dividir un único clúster Kubernetes en varios entornos virtuales. Cada namespace proporciona un espacio de nombres aislado para recursos. Uso: Gestiona recursos dentro de un clúster compartido, proporcionando aislamiento y organización para diferentes equipos o proyectos.
- kubectl get ns : lista los namespaces
- kubectl create ns nombre_espacio : Crea un namespace
- kubectl get all -n nombre_espacio : Asi listas los recursos definidos en un ns, recuerda q cada ns es un entorno virtual dentro del mismo cluster.
- En /manifest_examples/namespace.yaml hay un ejemplo de un manifest para crear un namespace.
- Modificamos nuestro pod.yaml para incluir el namespace bajo el cual se creara el pod
- kubectl get pods -A : Todos los pods independientemente de a q ns pertenezca
- kubectl delete ns name_space : Borra ese ns junto con lo que tenga dentro
- kubectl apply -f .  : Aplica todos los manifest del directorio en el que estas y resuelve el orden en el que deben ir. Aun asi mejor hacerlo por separado
- En el codigo ns_pod.yaml viene como crear el namespace y el pod juntos.
# Video 33: Servicios
- Como acceder al servicio que hay corriendo dentro de un pod? Para esos son los servicios. Una forma ya conocida para entrar es con minikube ssh pues nuestro cluster es local. Para hacerlo mediante kubectl podemos acceder a la descripcion del pod (kubectl describe pod pod_name), donde pod_name lo podemos ver mediante kubectl get all, y en esa descripcion aparece la IP. Si accedemos con minikube ssh al pod u hacemos un curl IP entonces accederemos a la pagina del container. Otra forma mas facil de obtener la IP es con kubectl get all -o wide
- Acceder al pod mediante IP no es conveniente. En este caso solo hay un pod con una replica, que tal si hay 100 replicas cada una con IP diferente, en cual se estara ejecutando?
- Un Servicio en Kubernetes es un objeto que define una forma lógica para acceder a un conjunto de pods. Proporciona un punto de acceso estable (una IP y un puerto) para los pods, independientemente de su ciclo de vida. Esto permite la comunicación interna y externa con los pods sin preocuparse por los cambios en sus direcciones IP individuales.
- kubectl expose rs nombre --port puerto : Crea un servicio para un replicaset(rs) y especifica el puerto de exposicion. Ej. kubectl expose rs landingpage --port 80
- Lo anterior genera la IP fija mediante la que debemos acceder al pod. Esta IP es accesible desde dentro del pod (minikube ssh)
- kubectl get svc : Lista los servicios
- kubectl delete svc service_name : Borra el servicio
- El manifest para levantar un servicio como hasta ahora es service_clusterip.yaml
- Cuando levantamos este servicio es de tipo ClusterIP, este solo se accede desde dentro del cluster. El tipo NodePort permite el acceso desde fuera del cluster, el codigo es nodeport.yaml
- Una vez creado el NodePort, si le das kubectl get all -o wide podras ver el mapeo que hace, del puerto del pod al de afuera, tipo 80:31483/TCP. Podemos entonces acceder a los servicios desde fuera a traves del puerto 31483
- Seria a traves de la ip de minikube(minikube ip) y el puerto especificado (curl minikube_ip:31483)
- Tambien existe el servicio tipo LoadBalancer, que en algun momento generaria una IP publica(no solo el puerto) para conectar a nuestro cluster. Se vera a detalle cuando se vea aws y su manifest es loadbalancer.yaml
- El otro tipo es ExternalName, su manifest es externalname.yaml. Sirve para migraciones
# Video 34: Deployments