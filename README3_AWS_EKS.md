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
