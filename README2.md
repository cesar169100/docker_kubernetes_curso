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
- Un Deployment en Kubernetes es un objeto que gestiona la creación, actualización y escalado de un conjunto de pods. Proporciona un mecanismo para implementar aplicaciones de manera declarativa, asegurando que el estado actual del clúster coincida con el estado deseado especificado en el Deployment. También facilita las actualizaciones controladas y los rollbacks automáticos.
- Objeto que nos permite desplegar un replica set , que a su vez despliega una serie de pods y se puede controlar mediante un comando rollout
- El manifest de un deployment es deployment.yaml
- Si cambiamos, por ejemplo en el deployment.yaml la version de nginx y volvemos a dar apply se detendran los pods y el replicaset de la version anterior, pero no se elimina el replicaset; se genera un segundo replicaset y se levantan los pods, pero el primer replicaset sigue ahi solo que no esta corriendo.
- kubectl rollout history deployment deploy_name : Versiones por las que ha pasado el deployment. Es necesario agregar comentarios para tener buen detalle de que version es y porque cambio, etc. Se vera despues
- Si al comando anterior agregamos --revision=1, porjemlo, obtendremos mas detalles.
- kubectl rollout undo deployment deploy_name --to-revision=2 : Se vuelve a activar la version 2 del deploy, pero cambia el numero de las revisiones y se vuelve confuso. Es necesario agrgar descripciones. Como se activo la 2, esta desaparace y se convierte en la ultima revision
- kubectl rollout status deployment deploy_name : Status del deploy, util cuando son varias cosas las que se deben desplegar y queremos ur viendo como evoluciona el status
- kubectl annotate deployment deploy_name kubernetes.io/change-cause="Version 1.20" : Por ejemplo, cambiamos la etiqueta de la revision para que sea mas claro. Este cambio aplica para la version/revision que esta activa. Con esto ya es mas facil los undo porque el mensaje se mantiene, siempre sabes con que revision/version estas tratando.
# Video 35: Volumenes
- Empezamos con el sistema de volumenes de kubernetes.
- Un PersistentVolume (PV) en Kubernetes es un recurso de almacenamiento abstracto que proporciona una manera de gestionar el almacenamiento persistente para los pods. Es un recurso mas del cluster, al igual que un nodo es un recurso del cluster. A diferencia del almacenamiento temporal que se elimina cuando un pod se reinicia, un PV persiste más allá de la vida útil de cualquier pod, lo que permite que los datos permanezcan disponibles y consistentes entre reinicios y reprogramaciones de pods. Los PVs son gestionados de manera independiente del ciclo de vida de los pods, proporcionando almacenamiento duradero para aplicaciones que lo necesiten.
- Los PersistentVolumes (PVs) pueden ser provisionados de dos maneras:
Static Provisioning: Los administradores crean manualmente los PVs.
Dynamic Provisioning: Kubernetes crea automáticamente los PVs según sea necesario, utilizando StorageClasses para definir cómo se debe aprovisionar el almacenamiento.
- Un PersistentVolumeClaim (PVC) en Kubernetes es una solicitud de almacenamiento persistente realizada por un usuario. Los PVCs permiten a los usuarios solicitar tamaños específicos y características de almacenamiento sin preocuparse por los detalles de aprovisionamiento. Kubernetes vincula automáticamente el PVC a un PersistentVolume (PV) adecuado que cumple con los requisitos de la solicitud.
- "binding" es el proceso de enlazar o asociar un PVC a un PV. Cuando un PVC es creado, Kubernetes busca un PV disponible que cumpla con las especificaciones solicitadas en el PVC (como tamaño y características de almacenamiento) y los enlaza. Este binding asegura que el PVC tenga acceso al almacenamiento persistente proporcionado por el PV. Una vez que un PV está enlazado a un PVC, ese PV no puede ser enlazado a otro PVC hasta que el PVC actual sea liberado.
- El codigo esta en manifest_examples/volumenes/persisten_volume.yaml
- kubectl get pv : Ve los persisten volumes (pv)
- De los AccessModes y ReclaimPolicy se habla en el codigo
- Si el STATUS de un PV es available es que ningun PVC esta ligado (binding) a el, de lo contrario el STATUS sera bound.
- StorageClasses: Es un objeto que proporciona una manera de describir las clases de almacenamiento que están disponibles para los PersistentVolumes (PVs) dinámicos en un clúster. Define cómo deben ser aprovisionados y configurados los PVs solicitados a través de PersistentVolumeClaims (PVCs). Esto permite a los usuarios solicitar almacenamiento con características específicas (como tipo, tamaño, rendimiento) sin necesidad de conocer los detalles de la infraestructura subyacente de almacenamiento.
- Codigo para crear el pvc es persistent_volume_claim.yaml
- Codigo para asociar un PV a un pod en el codigo pod_pv.yaml junto con notas importantes de la clase.
- Lo visto hasta ahora es muy manual, es mejor los sistemas de aprovisionamiento dinamico q se veran mas adelante.
# Video 36: Configmaps
- Un ConfigMap nos da una manera de inyectar datos de configuracion a un pod
- Es un objeto que se utiliza para almacenar datos de configuración en pares clave-valor. Permite separar la configuración del código de la aplicación, facilitando la administración y modificación de configuraciones sin necesidad de recompilar la imagen del contenedor. Los datos almacenados en un ConfigMap pueden ser utilizados por los pods como variables de entorno, archivos de configuración montados en volúmenes, o argumentos de línea de comando.
- kubectl get cm : Obtener nuestros configmaps
- Kubectl create configmap configmap_name --from-literal var1=valor1 --from-literal var2=valor2 ... : Crea el mas sencillo de los configmaps, con nombre configmap_name, solo una relacion clave-valor o en forma mas sencilla, define variables. (No admite '_' en los nombres)
- kubectl describe cm configmap_name : Mas info del cm
- Codigo de un pod que toma una variable de ambiente de un configmap: pod_cm_literal.yaml, junto con notas adicionales de la clase
- Vamos a tener dos archivos de configuracion, default.conf y test.conf. El objetivo es inyectar estos archivos en un pod, es decir, darle la configuracion al container especificada por uno de estos archivos.
- kubectl create cm nginx-config-dir --from-file=manifest_examples/nginx : Crea un ConfigMap en Kubernetes llamado nginx-config-dir. Este ConfigMap se genera a partir de todos los archivos contenidos en el directorio manifest_examples/nginx, y cada archivo en ese directorio se convierte en una clave dentro del ConfigMap, con su contenido como valor correspondiente.
- El pod que se levanta con el configmap anterior es pod_cm_file.yaml y tiene notas importantes de la clase.
# Video 37: Secrets
- Similares a los ConfigMaps pero sirven para guardar passwords, tokens, etc, info sensible. Desacoplan la configuracion de lo que hay dentro de la imagen. A diferencia de los ConfigMaps, los Secrets permiten almacenar datos en formato codificado (Base64) para añadir una capa de protección. Los Secrets pueden ser montados en pods como volúmenes o inyectados como variables de entorno.
- kubectl get secret
- kubectl create secret generic secret_name --from-file=manifest_examples/nginx/username.txt --from-file=manifest_examples/nginx/pass.txt
Lo anterior crea un volumen secret a partir de esos archivos con info sensible.
- El codigo q crea un pod y monta en el container los secrets definidos es pod_secret.yaml
- El codigo que crea un pod y sus variables env las toma de un secret es pod_envars.yaml
- Convertir un string a Base64: echo -n 'tu-password' | base64
- El codigo secret.yaml viene como crear un secret desde manifest. Esto ya no venia en el curso
# Video 38: Request y Limits
- Cuando especificas un Pod, opcionalmente puedes especificar qué cantidad de cada recurso necesita un contenedor. Los recursos más comunes para especificar son CPU y memoria (RAM); hay otros. Cuando especifica la solicitud de recursos para contenedores en un Pod, el kube-scheduler usa esta información para decidir en qué nodo colocar el Pod. Cuando especifica un límite de recursos para un contenedor, kubelet aplica esos límites para que el contenedor en ejecución no pueda usar más de ese recurso que el límite que usted estableció. El kubelet también reserva al menos la cantidad solicitada de ese recurso del sistema específicamente para que lo use ese contenedor. Los límites se pueden implementar de forma reactiva (el sistema interviene una vez que detecta una infracción) o mediante aplicación (el sistema evita que el contenedor exceda el límite).
- Los cgroups (control groups) en Linux son una característica del kernel que permite limitar, contabilizar y aislar el uso de recursos (como CPU, memoria, disco y red) de un grupo de procesos. Esto es útil para administrar recursos en sistemas compartidos y es ampliamente utilizado en contenedores y sistemas de virtualización para garantizar que cada aplicación o contenedor tenga acceso a una cantidad específica de recursos del sistema.
- Cuando kubelet inicia un contenedor como parte de un Pod, kubelet pasa las solicitudes y los límites de memoria y CPU de ese contenedor al tiempo de ejecución del contenedor. En Linux, el tiempo de ejecución del contenedor generalmente configura cgroups del kernel que aplican y hacen cumplir los límites que usted definió.
- El límite de CPU define un límite estricto sobre la cantidad de tiempo de CPU que puede utilizar el contenedor. Durante cada intervalo de programación (intervalo de tiempo), el kernel de Linux verifica si se excede este límite; si es así, el kernel espera antes de permitir que ese cgroup reanude la ejecución.
- La solicitud(request) de CPU normalmente define una ponderación. Si se quieren ejecutar varios contenedores diferentes (cgroups) en un sistema competitivo, a las cargas de trabajo con solicitudes de CPU más grandes se les asigna más tiempo de CPU que a las cargas de trabajo con solicitudes pequeñas.
- El límite de memoria define un límite de memoria para ese cgroup. Si el contenedor intenta asignar más memoria que este límite, el subsistema de falta de memoria del kernel de Linux se activa y, normalmente, interviene deteniendo uno de los procesos en el contenedor que intentó asignar memoria. Si ese proceso es el PID 1 del contenedor y el contenedor está marcado como reiniciable(a traves de un replicaset, etc), Kubernetes reinicia el contenedor.
- apt update y apt install stress : Instala stress que es una herramienta para probar la cpu y memoria de una maquina. El codigo que levanta un pod con request y limits es pod_request.yaml
- apt install htop : Herramienta para ver los recursos que se consumen en tiempo real
# Video 39: Statefulsets
- Gestiona la implementación y el escalado de un conjunto de Pods y proporciona garantías sobre el orden y la unicidad de estos Pods. Al igual que un Deployment, un StatefulSet administra pods que se basan en una especificación de contenedor idéntica. A diferencia de una Deployment, un StatefulSet mantiene una identidad fija para cada uno de sus Pods. Estos pods se crean a partir de la misma especificación, pero no son intercambiables: cada uno tiene un identificador persistente que mantiene durante cualquier reprogramación.
- kubectl scale --replicas num_replicas tipo_objeto nombre_objeto: Por ejemplo, kubectl scale --replicas 4 statefulset web, sube o baja el num de replicas a 4 para el statefulset llamado web.
- Codigo manifest de un statefulset es statefulset.yaml
- Se usan cuando un pod necesita acceder a otro (dentro de ellos mismos)
- Los volumenes en este contexto son uno para cada Pod. Se crean los volumenes y el statefulset se encarga de contruir los claim. Codigo statefulset_volume.yaml
- El comando rollout tambien se puede usar aqui.
- Para definir volumenes compartidos entre los pods ver codigo pv.yaml y pv_claim_compartido.yaml.
# Video 40: Clusters multi nodo y pod affinity/antiaffinity
- minikube start --nodes numero : Lanzar cierta cantidad de nodos con minikube. En el primer nodo estaran los componentes de kubernetes y en los demas solo de computo
- kubectl get nodes: Listar nodos
- kubectl get nodes --show-labels : Vemos las etiquetas que nos ayudaran a identificar cada nodo y asi asignar un pod a un nodo por su nombre. Imagina que tenemos un nodo con gpu y los demas no, entonces seria conveniente asignar un pod con un proceso muy pesado a ese nodo en particular.
- Flexibilidad: Affinity/Anti-Affinity: Permiten reglas más complejas y condicionales, como "preferir pero no requerir" ciertas condiciones.
nodeSelector: Solo permite un mapeo directo y rígido entre etiquetas de nodos y pods.
- Control de Distribución: Affinity: Permite distribuir cargas de trabajo para evitar la concentración en un solo nodo.
Anti-Affinity: Permite evitar que ciertos pods se ejecuten juntos en el mismo nodo, mejorando la resiliencia y el balanceo de carga.
- Gradual Enforcement:Affinity/Anti-Affinity: Ofrecen tanto reglas "preferentes" (soft) como "requeridas" (hard), lo que proporciona mayor control sobre la colocación.
nodeSelector: Solo soporta reglas "requeridas".
- Uso de Topologías:Affinity/Anti-Affinity: Pueden usar topologías como zonas de disponibilidad, racks o regiones, no solo nodos individuales.
nodeSelector: Se limita a etiquetas de nodos sin considerar la topología del clúster.
- Codigos para levantar Pod y asignarle un nod nodeselector.yaml y affinity_pod.yaml
# Video 41: Daemonsets
- Tipo de controlador que asegura que una copia de un pod se ejecute en cada nodo del clúster. Se utiliza comúnmente para implementar tareas de administración en cada nodo, como monitoreo, registro y redes. Algunos usos son monitoreo de nodos, coleccion de logs. Ejemplo en daemonset.yaml
- kubectl get ds : Obtener daemonsets
# Video 42: Probes
- Los probes son mecanismos utilizados para verificar el estado de los pods. Existen tres tipos principales de probes:
Liveness Probe:
        Propósito: Verifica si el contenedor está en funcionamiento.
        Acción: Si la probe falla, el contenedor se reinicia.
Readiness Probe:
        Propósito: Verifica si el contenedor está listo para aceptar tráfico.
        Acción: Si la probe falla, el contenedor se elimina de los endpoints del servicio.
Startup Probe:
        Propósito: Verifica si el contenedor ha iniciado correctamente.
        Acción: Si la probe falla, el contenedor se reinicia. Este tipo de probe es útil para aplicaciones con tiempos de inicio largos.

- Métodos Comunes de Probes
HTTP Probes:
        Envía solicitudes HTTP GET a un contenedor.
        Configurado con una URL y espera un código de estado 200-399.
TCP Probes:
        Intenta abrir una conexión TCP en el contenedor.
        Configurado con un puerto.
Exec Probes:
        Ejecuta un comando en el contenedor.
        Configurado con el comando a ejecutar y espera un código de salida 0.

Estas probes se configuran en el manifiesto de los pods y ayudan a Kubernetes a gestionar la salud y disponibilidad de las aplicaciones.
- Si entras al bash de un pod y eliminas su proceso principal (kill -15 1) matas al pod y esto tiene como consecuencia que kubelet en automatico vuelva a lanzar el pod. Esta es la forma principal en la que kubernetes decide reiniciar un pod, cuando el proceso principal a muerto.
- kubectl logs -f pod_name : logs del pod
- Codigos de probes en carpeta probes.
- Las probes no tienen sentido en un pod que ejecuta una tarea única y luego termina, como un script de Python que realiza un proceso y finaliza. Las probes son más útiles para aplicaciones de larga duración que deben estar siempre disponibles y responder correctamente a las solicitudes.
# Video 43: Jobs
- Cuando lanzamos un container con Deployment, replicaset, statefulset, etc, estos objetos estan disenados para ejecutar tareas infinitas, ie, un proceso que va a estar ahi corriendo continuamente como un webserver o una appi y si falla pues tenemos los mecanismos para relanzar de kubernetes. Si queremos lanzar un proceso finito (un script de python, por ejemplo), para eso estan los jobs.
- un Job es un recurso que asegura que una o más tareas (pods) se ejecuten hasta completarse satisfactoriamente. Es ideal para tareas que se ejecutan una vez y finalizan, como procesar un conjunto de datos o realizar una operación de copia de seguridad.
Características de un Job:
Ejecución de Tareas: Ejecuta uno o más pods hasta que las tareas especificadas hayan finalizado con éxito.
Reintentos: Si un pod falla, el Job puede reintentar ejecutar la tarea según la política de reintentos especificada.
Finalización: El Job se considera completado cuando todos los pods necesarios han terminado satisfactoriamente.
Tipos de Jobs:
Jobs Completos: Se ejecutan una vez y terminan cuando la tarea se completa.
Jobs Paralelos: Ejecutan múltiples pods en paralelo, útiles para tareas que pueden dividirse en trabajos independientes.
CronJobs: Se utilizan para programar tareas que deben ejecutarse de manera periódica.
- Codigos y notas de Jobs en la carpeta jobs_cronjobs
# Video 44: Cronjobs
- Ejecutar jobs de manera programada. Codigos en carpeta jobs_cronjobs
# Video 45: Annotations
- Son metadatos clave-valor que puedes agregar a objetos de Kubernetes como Pods, Services, Deployments, etc. A diferencia de las etiquetas (Labels), que se utilizan principalmente para organizar y seleccionar conjuntos de objetos, las Annotations se usan para almacenar información adicional que puede ser utilizada por herramientas y bibliotecas externas.
- Propósito: Las Annotations proporcionan una forma flexible de adjuntar metadatos no identificables a los objetos. Pueden contener información como notas, referencias, configuraciones específicas, etc.
- Formato: Se definen como pares clave-valor en la especificación del objeto.
- Uso: Las Annotations no son utilizadas para seleccionar o filtrar objetos (a diferencia de las labels). Son más adecuadas para adjuntar datos que no influyen en la operación principal de Kubernetes.
- Carpeta annotations_ingressController_ingressRules
# Video 46: Nginx ingress Controller e ingress Rules
- Los Controllers son componentes que gestionan el estado de los objetos en el clúster. Su función principal es asegurar que el estado actual del clúster coincida con el estado deseado especificado en los manifiestos de Kubernetes.
- Ejemplos: 
Deployment Controller: Asegura que el número deseado de réplicas de una aplicación estén ejecutándose.
Job Controller: Asegura que los Jobs se ejecuten hasta completarse.
ReplicaSet Controller: Mantiene un número específico de réplicas de un pod en ejecución.

En resumen, los controllers son fundamentales en Kubernetes para garantizar que los recursos del clúster se mantengan en el estado deseado, automatizando la gestión de estos recursos.
- Los Ingress Controllers en Kubernetes son componentes que implementan el recurso Ingress, que gestiona el acceso externo a los servicios dentro de un clúster. Actúan como controladores de tráfico, permitiendo que las solicitudes HTTP y HTTPS lleguen a los servicios adecuados en función de reglas definidas en objetos Ingress.
- Características clave de los Ingress Controllers
Balanceo de Carga: Distribuyen el tráfico entrante entre los servicios backend.
Enrutamiento: Dirigen el tráfico basado en reglas como rutas URL y nombres de host.
SSL/TLS: Gestionan la terminación SSL para proporcionar conexiones seguras.
Autenticación y Autorización: Pueden implementar políticas de seguridad para controlar el acceso.
- Ejemplos:
NGINX Ingress Controller: Un controlador popular y ampliamente utilizado.
Traefik: Otro Ingress Controller con características avanzadas como la gestión dinámica de rutas.
- En resumen, los Ingress Controllers(puntos de acceso) son esenciales para gestionar y dirigir el tráfico externo hacia los servicios dentro de un clúster de Kubernetes, proporcionando balanceo de carga, enrutamiento y seguridad.
- https://kubernetes.github.io/ingress-nginx/ : Documentacion de como el Ingress-NGINX controller trabaja
- Helm es un gestor de paquetes para Kubernetes. Facilita la instalación, actualización y gestión de aplicaciones y servicios en un clúster de Kubernetes mediante el uso de charts.
Charts: Son paquetes que contienen plantillas preconfiguradas para Kubernetes, junto con configuraciones y dependencias.
Repositorios de Charts: Son lugares donde se almacenan y distribuyen estos charts.
- Creamos un namespace donde se va a desplegar nuestro nginx ingress controller: kubectl create ns ingress-nginx
- helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx : Este comando agrega el repositorio de charts de NGINX Ingress a Helm, permitiéndote instalar el Ingress Controller de NGINX en tu clúster de Kubernetes utilizando Helm. (curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash  para instalar helm)
- helm install -n ingress-nginx ingress-nginx ingress-nginx/ingress-nginx : Instalar
- Este ingress controller, una vez instalado, incluye un Deployment donde se despliega un Pod a traves de un ReplicaSet. Adicional se crean 2 servicios, el primero es uno tipo LoadBalancer que no tiene IP externa pues se despliega en minikube pero si tiene puerto de exposicion. Y otro que es para configurarlo, pero esto nosotros lo haremos a traves de las reglas. Estos objetos son para el funcionamiento del ingress controller
- Para acceder al cluster tenemos que tener la IP del cluster de minikube (minikube ip) y el puerto de acceso que se ve con kubectl -n name_space get all (pues creamos un ns para esto)
- Codigo de los deploys y en Ingress Resource en carpeta annotations_... y notas importantes
- Con lo anterior hemos conseguido acceder mediante su IP(del cluster) y puerto(del servicio) a un servicio con /nginx y a otro servicio con /httpd (192.168.67.2:31393/httpd o 192.168.67.2:31393/nginx)
- Nota: Un dominio es un nombre único que identifica a un sitio web en Internet. Es la dirección que los usuarios escriben en sus navegadores para acceder a un sitio web específico.
Componentes de un Dominio
Nombre de dominio: La parte específica que identifica al sitio web, como example.
Extensión de dominio: El sufijo que sigue al nombre de dominio, como .com, .org, .net, etc.
Los dominios son gestionados por el Sistema de Nombres de Dominio (DNS), que traduce los nombres de dominio en direcciones IP para localizar y acceder a los servidores web.
En resumen, un dominio es una dirección legible por humanos que se utiliza para acceder a un sitio web en Internet.
# Video 47: Edit y Patch