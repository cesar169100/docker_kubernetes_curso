# Intro
En este readme estara lo correspondiente a kubernetes en aws con EKS
# Video 49: Intro y preparacion del entorno
- Es mala practica de seguridad el acceso a la consola mediante el usuario root. Podemos ir  IAM -> Users y crear uno nuevo, darle nombre y elegir la casilla: Provide user access to the AWS Management Console - optional. Elegir, ahora, la opcion: I want to create an IAM user de las nuevas que se desplegaron y dar crear a custom password y crearla; quitar la casilla de crear new pass despues del primer loggeo y dar next. Ahora pide los permisos, dar en Attach policies directly y elegir AdministratorAccess y next. Ya solo dar create, bajjar en csv el user y pass. Con esto ya puedes salir y volver a entrar con la nueva URL y tu pass, al entrar, dar de alta un MFA para este user y crear sus access keys (access key y secret key)
- Instalar aws cli: Solo poner aws cli install en google y dar en la primer opcion de la pagina de aws docs. Ahi vendran los comandos para tu sistema operativo. Despues hacer el aws configure. Ejecutar aws sts get-caller-identity para ver con que usuario estamos atacando el api de aws
# Video 50: Creacion del control plane
- AWS EKS (Elastic Kubernetes Service) es un servicio administrado de Kubernetes en la nube de Amazon Web Services. Permite ejecutar aplicaciones en contenedores usando Kubernetes sin tener que instalar y gestionar manualmente los clústeres de Kubernetes.
Beneficios:
Gestión simplificada: AWS se encarga del control plane y la infraestructura subyacente.
Escalabilidad: Fácil de escalar según la demanda.
Seguridad: Integración con otros servicios de AWS para seguridad y gestión de identidades.

En resumen, AWS EKS facilita el uso de Kubernetes al gestionar la infraestructura y permitir que los usuarios se concentren en el desarrollo y la administración de aplicaciones.
- Service role: Un service role (rol de servicio) en AWS es un rol de AWS IAM que un servicio de AWS asume para realizar acciones en nombre del usuario. Este rol permite que el servicio tenga permisos específicos necesarios para ejecutar tareas en AWS.
Características:
Permisos Delegados: Permite a los servicios de AWS realizar acciones en tu cuenta con los permisos definidos en el rol.
Seguridad: Ayuda a mantener la seguridad y el control al delegar permisos necesarios sin usar credenciales de usuario.
Uso Común: Servicios como AWS Lambda, Amazon ECS, y AWS EKS usan roles de servicio para ejecutar funciones y tareas.
En resumen, un service role permite a los servicios de AWS realizar acciones en tu cuenta AWS con permisos específicos y controlados.
- Crear cluster-role: IAM -> Roles -> Create -> Elegir tipo AWS Service -> En use case elegimos EKS -> Elegimos EKS Cluster de la lista de subcasos y next -> En add permissions ya puso una politica correspondiente y solo vuelve a dar next -> En Name, review and create pon un nombre y una descripcion y create.
- Crear cluster: EKS -> Crear cluster -> Dar nombre y elegir nuestro cluster-role -> Elige la version default de kubernetes -> 
-> Cluster access: Dar en allow cluster admin access y en Cluster authentication mode dejar EKS api and ConfigMap
-> Secrets encryption: Si esta en on encripta el secret que hagamos en el cluster, aqui lo pondremos en off y next
-> Networking: Dejamos la vpc y subnets por defecto(eliminar la subnet us-east-1e o la que sea que mande error por disponibilidad en la zona), elegimos el security group por defecto tambien, en Choose cluster IP address family dejamos IPv4 y Configure Kubernetes service IP address range en off
-> Cluster endpoint access: Lo dejamos en Public y next
-> Configure observability: Prometheus lo dejamos en off y en Control plane logging dejamos todos en off tambien (a menos que queramos guardar los logs en cloudWatch) y next
-> Select add-ons: Solo dejamos CoreDNS, Kube-proxy, VPC CNI, EKS Pod Identity Agent y next
-> Configure selected add-ons settings: Dejar todo en su version default y next
-> Review: Dar crear
- El API server endpoint en la sección Details de tu clúster EKS es la URL que los clientes (como kubectl y otras herramientas) usan para interactuar con el servidor API de Kubernetes. Este endpoint es la puerta de entrada para realizar todas las operaciones de gestión del clúster, como despliegue de aplicaciones, escalado de pods y obtención de información del estado del clúster. En la seccion Compute estan los nodos(aun no creados)
- aws eks list-clusters --region us-east-1: Lista los clusters en esa region, region es opcional
- aws eks describe-cluster --name cluster_name : Toda la info del cluster
- Configurar kubectl: Eliminar cluster de minikube(minikube delete) -> ir a raiz con cd -> 
cd .kube/ -> debe haber un archivo config -> lo borramos (rm config) -> ejecutamos el siguiente comando: aws eks update-kubeconfig --name cluster_name , este lo que hace es actualizar la configuracion para que kubectl interactue con nuestro cluster de eks.
- Nota: .kube/ es la carpeta donde ira el archivo config que es donde se configura el acceso de kubectl a nuestro cluster
- Ya podemos ejecutar comandos tipo kubectl get all, etc
# Video 51: Desplegar workers a traves de node groups  
- Una vez desplegado el cluster, ir a Compute -> Node Groups
- Debemos crear otro IAM role para nuestro node group si es que no existe ya uno con algun nombre como estos: eksNodeRole, AmazonEKSNodeRole, or NodeInstanceRole.
- Crear rol -> trusted entity: aws service -> use case: EC2 y EC2 en los subcasos tambien, next -> Elegimos las politicas basicas: AmazonEKSWorkerNodePolicy, AmazonEC2ContainerRegistryReadOnly y AmazonEKS_CNI_Policy, next -> Damos nombre como AmazonEKSNodeRole, ponemos descripcion y crear.
- Volvemos a eks donde nos quedamos, en Compute y Node Groups -> Crear grupo -> Dar nombre y elegir el rol que acabamos de crear -> LaunchTemplate en off y las labels(podemos especificar si es un grupo de maquinas grandes, por ejemplo) y taints las dejamos vacias, next ->  Node group compute: Elegimos la AMI(Amazon machine image for node) linux estandar, Capacity: On demand(pagas el tiempo de uso), elegimos una maquina (t3.small en mi caso) y disk size lo dejamos en 20G -> Node group scaling: Damos el numero de nodos que queremos, 2 en este caso -> Node group update configuration: Numero o % de nodos no disponibles que permitiremos durante una actualizacion de nodos, en este caso dejamos 1, es decir, si hay actualizacion se hara de uno por uno, next -> Specify networking: Dejamos como esta, next -> Review y create: Create.
- Launch Template: Permite especificar configuraciones detalladas para las instancias EC2 que formarán parte del grupo de nodos. Estas configuraciones incluyen detalles como el tipo de instancia, el AMI, los discos de almacenamiento, las etiquetas y otros parámetros avanzados. Usar un Launch Template asegura consistencia y control sobre la configuración de los nodos. Se crean en la seccion de EC2
- Una vez creado el nodegroup se crea un autoscaling group visible desde EC2 y las instancias tambien aparecen en instances. Podemos editar el nodegroup al elegirlo y darle edit, podemos modificar la cantidad de nodos activos/deseados, minimos, maximos y etiquetas.
- Supon tenemos un grupo con 2 nodos activos y lo editamos para tener solo 1 activo. El nodo que ya no estara activo pasa a eliminarse y al proceso que hace kubernetes para mandar la carga de este nodo en proceso de muerte a los demas vivos, se llama eviction.
# Video 52: Desplegar Deployment y servicio tipo ELB
- El codigo y notas en carpeta EKS/Video_52
- Poner la DNS del pod en el navegador te permitira ver el contenido del container
# Video 53: eksctl
- eksctl es una herramienta de linea de comandos para crear y administrar clusters en EKS.
- Ir a amazon EKS docs -> busca eksctl -> debe haber algun link de instalacion -> sigue los pasos, eksctl version para comprobar.
- Codigo para crear cluster en carpeta Video_53
- eksctl se apoya de CloudFormation para la creacion de la infra del cluster. Borra el .kube/config antes de levantar el cluster
- eksctl create cluster -f archivo.yaml : Levanta el cluster definido en ese manifest
# Video 54: Intro a Helm
- Sistema para empaquetar aplicaciones de kubernetes(deployments, ingress etc) en algo llamado charts, que son parametrizables.
- Dar helm en navegador -> Installing Helm -> From Script -> Ejecutar los comandos y rm get_helm.sh
- Para instalar un chart debemos agregar un repo de charts a nuestro helm. En el artifacthub y bitnami hay un repo con charts para descargar
- helm repo add bitnami https://charts.bitnami.com/bitnami : añade el repositorio de charts de Bitnami a tu instalación de Helm. Esto te permite buscar, descargar e instalar aplicaciones empaquetadas (charts) desde el repositorio de Bitnami usando Helm.
- helm install mi-nginx bitnami/nginx : Un ejemplo de como descargar una api empaquetada
- Al bajar el chart, este contiene una serie de manifest y en nuestro cluster se crearan una serie de recursos (kubectl get all) como un deployment,  replicaset, servicios(incluido un loadbalancer) y el Pod donde esta nginx
- helm ls : Lista todos los charts descargados, helm ls -A si tenemos otros namespaces
- helm uninstall chart_name : Elimina el chart instalado
- helm repo list : Lista de los repos agregados hasta ahora
# Video 55: Visualizacion de logs de varios pods con Stern
- Stern es herramienta para obtener logs de varios pods al mismo tiempo
- Damos stern github en navegador -> Entramos a la opcion de github/stern/stern -> Releases -> Assets -> Elegimos la version stern_linux_amd64 -> clic derecho y copiamos direccion de enlace -> en consola hacemos wget direccion_copiada y esto bajara un binario -> Lo descomprimimos: tar -xvzf archivo_stern.tar.gz -> Damos permisos de ejecucion chmod +x stern -> Lo movemos al path: sudo mv stern /usr/local/bin/stern
- Ya podemos ejecutar stern para ver que esta instalado
- stern nginx-d-77d6dd4bd8 : Nos muestra los logs de todos los pods cuyo nombre empiece con ese patron.
# Video 56: AWS Load Balancer Ingress Controller
- La diferencia principal entre un Elastic Load Balancer (ELB) y un Application Load Balancer (ALB) en AWS radica en su tipo y características:
- Elastic Load Balancer (ELB):
Tipo: ELB es un término genérico que AWS usa para referirse a su servicio de balanceo de carga.
Subtipos:
    Classic Load Balancer (CLB): El tipo más antiguo, utilizado para balancear tráfico tanto en nivel de aplicación (HTTP/HTTPS) como en nivel de transporte (TCP).
    Application Load Balancer (ALB): Diseñado específicamente para balancear tráfico HTTP/HTTPS, con características avanzadas para aplicaciones web.
    Network Load Balancer (NLB): Orientado a balancear tráfico TCP/UDP, ideal para aplicaciones de baja latencia y alto rendimiento.
- Application Load Balancer (ALB):
Tipo: Subtipo de ELB especializado en el balanceo de tráfico HTTP/HTTPS.
Características:
    Capas de Aplicación: Opera en la capa 7 del modelo OSI, lo que permite balancear tráfico basado en contenido (por ejemplo, rutas y headers).
    Routing avanzado: Soporta reglas complejas de enrutamiento, como la redirección de URLs, path-based routing, y host-based routing.
    Integración con ECS y EKS: Facilita el despliegue de servicios en contenedores, integrándose con AWS ECS y EKS.
    WebSocket y HTTP/2: Soporta estos protocolos, proporcionando una mejor experiencia en aplicaciones modernas.

En resumen, ALB es un tipo de ELB más moderno y enfocado en aplicaciones web, con características avanzadas para manejo de tráfico HTTP/HTTPS, mientras que ELB (en su forma de CLB) es más general y de propósito múltiple, pero con menos capacidades específicas para aplicaciones.
- El archivo iam_policy.json  es una politica de aws que permite que los workers de nuestro cluster sean capaces de gestionar balanceadores de carga.
- Para crear la politica, el comando esta en el archivo enlaces.txt
- Activar oidc en nuestro cluster. Nota: OIDC (OpenID Connect) es un protocolo de autenticación basado en OAuth 2.0, que permite a los usuarios autenticarse en aplicaciones web y móviles utilizando una identidad federada (como Google, Facebook, etc.). OIDC proporciona una capa adicional de autenticación al permitir que las aplicaciones verifiquen la identidad del usuario y obtengan su información de perfil básica de manera segura y estandarizada. En este caso, cualquier pod que se despliegue en kubernetes sea capaz de autenticarse con aws via oidc. El comando viene en enlaces.txt
- Crear cuenta se servicio. Un IAM Service Account en AWS es una combinación de una cuenta de servicio de Kubernetes y un rol de IAM. Permite a los pods en un clúster de Kubernetes, como EKS, asumir permisos específicos de AWS directamente a través de IAM, sin necesidad de usar credenciales a nivel de nodo. Esto facilita que los pods interactúen de manera segura con otros servicios de AWS, como S3 o DynamoDB. Codigo para crearla en el mismo enlaces.txt. Se creara un nuevo stack en CloudFormation que a su vez tendra un rol que permitira que cuando despleguemos el Load Balancer ingress controller tenga acceso a las politicas de seguridad definidas en el iam_policy.json
- Desplegar AWS Load Balancer: Ver enlaces.txt
- Nota: AWS Load Balancer actua como un ingress controller
- Desplegamos un deploy y un servicio en deployment.yaml
- Desplegamos el ingress en ingress.yaml, se creara el load balancer y el target group (ver en EC2), en el target group, en Targets estaran nuestros nodos
- Notas: Hubo que agregar a la politica la accion: "elasticloadbalancing:AddTags" y en el manifest del ingress especificar las subnets: alb.ingress.kubernetes.io/subnets: subnet-07e47efa777a5210b, ..., etc
- Entrando al Load Balancer y ver en los details en DNS name, esta es la direccion para acceder al container. Eliminar el ingress elimina el Load y el Target
# Video 57: External DNS (ingress controller)
- External DNS es una herramienta que gestiona automáticamente los registros DNS para los servicios de Kubernetes. Permite que los recursos de Kubernetes, como Ingress y servicios, se registren en un proveedor de DNS externo, facilitando la configuración y actualización de los nombres de dominio asociados a esos recursos.
- Route 53 es un proveedor de DNS de AWS y puede ser utilizado como el proveedor externo de DNS para gestionar los registros a través de External DNS en Kubernetes.
- Codigos para desplegar external DNS en comandos.txt
- Crear hosted zone: Ir a Route53 -> hosted zones, crear nueva -> dar nombre (mi-diminio.com, por ejemplo) -> Type: Selecciona Public hosted zone si el dominio será accesible desde internet, o Private hosted zone si es para uso interno dentro de una VPC. -> Crear
- Se deben crear dos, una tipo NS y otra tipo SOA. Debe existir un dominio (hosted zone) a la que apuntar cuando se genere el ingress. Ver en ingress.yaml correspondiente a este video
- Entonces, una vez creado el cluster y sus nodegroups se despliega el aws load balancer ingress controller como en el video pasado, segundo, se depliega el external dns ingress como se vio aqui, tercero, se crea el hosted zone. Con esto ya se puede desplegar un deploy con su servicio y el ingress, este ultimo creara un balanceador de carga en EC2 que a su vez tendra un DNS name con el que se puede acceder al container, este mismo DNS name estara en la hosted zone creada con un record tipo A, en ese vendra el dominio elegido y se podra acceder con el. No pude acceder con el dominio, segun a veces puede tardar mucho...
# Video 58: EBS con EBS CSI Controller
- Esta vez se asignaran los volumenes mediante aprovisionamiento dinamico. Este aprovisionamiento, kubernetes, lo hace mediante CSI
- CSI (Container Storage Interface) es un estándar que define una interfaz para que los proveedores de almacenamiento desarrollen plugins que permitan que los contenedores gestionen volúmenes de almacenamiento de manera uniforme. Esto facilita la integración de distintos tipos de almacenamiento con Kubernetes, independientemente de la tecnología subyacente.
CSI se comunica con el api de aws para crear volumenes y estos iran montados en nuestros pods
- Desplegar el CSI controller: archivo comandos.txt del video correspondientes
- Desplegar storage class, claim y un pod donde se monte ese volumen. El volumen sera visible desde EC2 en Volumes.
- Entramos al pod: kubectl exec -it pod_name bash, nos vamos a /data que fue donde se monto el volumen y creamos un archivo, eliminamos el pod (el volumen no se elimina, obvio), volvemos a levantar ese pod y en la ruta data/ estara nuestro archivo creado. Para eliminar el volumen, elimina el claim
- Hasta ahora:
1) Levantamos cluster y node group(Video 56)
2) Levantamos el aws Load balancer ingress controller(Video 57)
3) Levantar el CSI (si quieres volumen)(Video 58)
4) Crear el storageclass y el claim (si quieres volumen)(Video 58)
5) Crear la hosted zone (route53)(Video 57)
4) Levantar deployment con su servicio, luego el ingress, en el deploy especificar volumenes.(Video 58)
# Video 59: HPA(Horizontal pod autoscaler)
- Escalado horizontal: Añadir más instancias o servidores al sistema para manejar la carga, distribuyendo el trabajo entre múltiples nodos.
- Escalado vertical: Aumentar la capacidad de un solo servidor o instancia, mejorando sus recursos (CPU, RAM, almacenamiento) para manejar una mayor carga.
- La doc de kubernetes: Horizontal Pod autoscaling, revisar
- En Kubernetes, un HorizontalPodAutoscaler actualiza automáticamente un recurso de carga de trabajo (como un Deployment o StatefulSet), con el objetivo de escalar/reducir automáticamente los recursos(mas pods) para satisfacer la demanda.
- Para trabajar con HPA necesitamos kubernetes metric server, componente para metricas sobre el uso de rcursos en el cluster. Con estas metricas, HPA sabra cuando escalar, reducir, o dejar igual. Para instalar metric server ver comandos.txt de este video
- Tambien se despliega un deployment, servicio  y un nuevo objeto tipo HorizontalPodAutoscaler que actua sobre un deploy/statefulset para subir o bajar las replicas segun una metrica.
- El HPA se puede aplicar sobre un ingress, si las solicitudes aumentan entonces que escale el ingress
- Entonces, hasta ahora:
1) Levantamos cluster y node group(Video 56) manual o con eksctl
2) Instalamos metric server (Video 59)
3) Levantamos el aws Load balancer ingress controller(Video 57)
4) Levantar el CSI (si quieres volumen)(Video 58)
5) Crear el storageclass y el claim (si quieres volumen)(Video 58)
6) Crear la hosted zone (route53)(Video 57)
7) Levantar deployment con su servicio, luego el hpa, luego el ingress, en el deploy especificar volumenes.(Video 58)
