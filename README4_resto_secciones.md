# Intro
En este documento se abordaran el resto de secciones del curso
# Video 67: Prometheus y Grafana
- Prometheus es un software libre para monitoreo de eventos y alertas. Sitio de prometheus: https://prometheus.io/
- En el codigo comandos del video 67 estan las instrucciones de la instalacion sencilla de prometheus y Grafana. Hay que instalar metric server
- Cosas como metricas custom, ambientes prod etc en prometheus no se veran en este curso, incluso hay una certificacion en prometheus.
- Prometheus tiene su propio lenguaje para hacer query a los datos que se almacenan: promql. Buscarlo en el navegador para ver como hacer querys
- Para levantar Prometheus es necesario hacer el paso 6 de las intrucciones del repaso final de la seccion eks, el oidc e instalar el CSI driver para que aprovisione volumenes. Tambien seguir los comandos de instalacion en la documentacion de aws eks prometheus
- Grafana funciono bien. Esta interfaz es la que se usa, lo primero es ir al conexiones y agregar un data source, entre ellos esta Prometheus y la url seria http://prometheus-server y lo demas igual, dar save and test, esto porque ambos estan configurados en el mismo namspace. Luego en explore ya podemos correr querys
- En grafana dashboards (pagina de grafana) podremos encontrar dashboards q la gente ha usado, en particular podemos buscar kubernetes y veremos esos dashboards para kubernetes. Si elijes un dash este traera un codigo de identificacion y desde grafana podras importar ese dasboard con su codigo.
- El dashboard 10000 de kubernetes es basico
# Video 68: ELK Stack-(Elasticsearch, Logstash, Kibana)
- El ELK Stack es un conjunto de herramientas de código semiabierto compuesto por Elasticsearch, Logstash y Kibana. Se utiliza para buscar, analizar y visualizar grandes volúmenes de datos en tiempo real. Elasticsearch es un motor de búsqueda y análisis, Logstash es un procesador de datos que ingiere, transforma y envía los datos, y Kibana proporciona una interfaz gráfica para visualizar los datos y crear dashboards.
- Esto solo es una intro como con Prometheus, hay cursos completos de ELK
- El cluster necesita nodos t3.medium y minimo 3 workers para este ejercicio
- A igual que prometheus, no es psible continuar la instalacion debido a que se crean claims pero lo logra asociarlos a volumenes por lo que se queda en estado pending. Intente, en elasticsearch-install.yaml agregar el storageClass default(gp2) para que asiganara volumen pero no funciona y no es tema de recursos. En una prueba a parte(pvc_test.yaml) verifique que el stotageClass gp2 si funciona bien.
- De momento dejare esta seccion de monitorear y avanzare en el curso...
## Seccion: ECR
# Video 69: Presentacion de la seccion ECR
- ECR servicio de registro de containers en aws, crear nuestras imagenes y subirlas ahi y no depender de dockerHub y es mas seguro.
# Video 70: Configurar ECR(Elastic Container Registry) y subir imagenes
- Crear un repositorio privado(para publicos mejor usar dockerhub): Ir a ECR -> Private registry -> repositories -> Create -> Dar nombre de la siguiente manera namespace/nombre, esto es, hay que indicarle en que ns va a ir. Yo puse el ns default en esta primera prueba 
default/hola-mundo -> Ponemos tag mutability en mutable para poder editar los nombres de las etiquetas de nuestras imagenes. -> Image scan en disabled(y ya parece deprecado) -> En encryption settings elejimos la AES-256 que es la estandar de la industria -> Create
- El image scanning en ECR es una característica que analiza las imágenes de contenedores almacenadas en el registro para detectar vulnerabilidades de seguridad conocidas. Utiliza bases de datos de vulnerabilidades como CVE (Common Vulnerabilities and Exposures) para identificar posibles riesgos en las capas de la imagen y generar reportes con los hallazgos.
- Una vez creado el repo hay un boton que dice 'view push commands', aqui veremos para linux o windows los comandos para subir nuestras imagenes. El primer comando es para obtenere una password y usarla para conectarnos al server de nuestro repo -> Una vez que tengamos un dockerfile para construir una imagen podemo ejecutar el segundo paso "docker build -t default/hola-mundo ." y parados en la ruta donde tengamos nuestro dockerfile. Si la imagen ya existe entonces este paso no es necesario. -> Reetiquetamos la imagen en el tercer paso -> Finalmente hacemos push al repo
- La imagen anterior ya esta disponible para traernosla con un pull. En la consola, ya debe aparecer la imagen junto con su image URI (url). Si nos metemos en la imagen veremos los detalles y podremos hacer el scaneo manual de vulnerabilidades.
- Podemos poner etiqueta diferente a latest: docker build -t default/hola-mundo:18.04 .
- Al reetiquetar poner la etiqueta correcta: docker tag default/hola-mundo:18.04 590184078061.dkr.ecr.us-east-1.amazonaws.com/default/hola-mundo:18.04
- Y al push igual: docker push 590184078061.dkr.ecr.us-east-1.amazonaws.com/default/hola-mundo:18.04
- La seccion de permisos en para permisos entre cuentas de aws. Si hay una cuenta distinta a la tuya y le quieres dar permiso de bajarse una imagen tuya, por ejemplo.
# Video 71: Makefile
- Crear imagenes en automatico en un pipeline.
- Un Makefile es un archivo que define una serie de comandos y dependencias para automatizar tareas, como la compilación de código o la gestión de proyectos. Es utilizado por la herramienta make para ejecutar estas tareas de manera eficiente, solo recompilando lo necesario según los cambios.
- En seccion7_ECR/Video_71 hay un makefile, cada target es una tarea. Si no tienes make: sudo apt install make
- En los Makefile se pueden meter parametros a los comandos, usar variables de entorno, ect. Eso no se vera aqui, investigar en la doc GNU make
## Seccion ECS y Fargate
# Video 72: Presentacion de la leccion
- AWS ECS (Elastic Container Service) es un servicio de orquestación de contenedores que permite ejecutar y escalar aplicaciones en contenedores usando Docker. Facilita la gestión de contenedores en una infraestructura de AWS, soportando tanto entornos con instancias EC2 como con AWS Fargate (serverless). Alternativa a Kubernetes
# Video 73: Crear imagen
Se crea la imagen a partir del dockerfile de este video. Se hace lo mismo que en la seccion ECR.
# Video 74: Crear cluster en ECS
- Ir a ECS -> clusters -> Create cluster -> Damos nombre -> Podemos dar un namespace, yo lo dejare asi -> Infra: Elegir aws ec2 o fargate -> Dejar la opcion de autoscaling group en create new -> provisionamiento ON DEMAND -> AMI deja la estandar amazon linux 2 que marque ahi -> Elige el tipo de instancia ec2 si elegiste ec2(puse t3.small), deja en crear un nuevo rol para EC2 -> Pon la capacidad deseada de instancias -> Root EBS volume size dejalo en 30 -> Networking: Dejalo todo estandar hasta el security group, pon crear uno nuevo y ponle la inbound rule con puerto 80 y source anywhere(0.0.0.0/0), abre el puerto 80 a todos lados. -> En monitoring activa la opcion Use Container Insights de cloudwatch -> Crear
# Video 75: Task Definition
- Una task definition en AWS ECS es un archivo JSON que define cómo ejecutar contenedores en ECS. Especifica configuraciones como la imagen de Docker, los recursos (CPU y memoria), las variables de entorno, los volúmenes y las políticas de IAM necesarias para una tarea o servicio en ECS.
- Ir a ECS -> Task definitions -> Create new (no json) -> dar nombre -> Infra: Elegir ec2 o fargate, sistema operativo (linux) y networking mode awsvpc -> Dar task size 1vCPU=1024Cpu puedes ponerlo en enteros y esto serian cpus y megas o como 1 vCPU o 1 GB -> Definir Task role en caso de que el container necesite hacer peiciones, por ejemplo, a S3 -> Task execution role create new -> En el container, dar nombre y poner la image URI de ECR -> Dejar todo estandar hasta la parte de loggeo: Dejar activada la opcion Use log collection ->
Crear.
# Video 76: Tasks
- Task: Una ejecucion de un container
- En el cluster creado ir a task -> Run Task -> En Compute configuration elige Launch Type y tipo EC2 o fargate. -> En Deployment configuration Elige task para una tarea simple o service para una aplicacion, elige la familia(nombre de la task definition) -> DEfine el numero de Desired tasks (replicas) y lo demas estandar -> Crear
# Video 77: Servicios
- Se define igual que la task, el servicio es un deployment y las task son las replicas. 
# Video 78: Balanceadores de carga
- Durante la definicion de un servicio, como en el video anterior, hay una opcion de definir un LB. Elegir esta opcion y darle en application load balancer, darle nombre, que haga uno nuevo y lo demas estandar.
# Video 79 y 80: Replicar en Fargate y temas de monitoreo
Revisar bien si en algun momento es necesario.
## Seccion Helm
# Video 81: Presentacion
Tomar los recursos de un manifest (deploys, servicios, etc) y empaquetarlos en un chart de helm y parametrizado. Recordar que helm es el manejador de paquetes de kubernetes.
# Video 82: Introduccion en instalar charts
- En la seccion charts de la pagina oficial de helm vienen todos los charts que pueden ser descargados. Helm se comunica automaticamente con nuestro cluster, no necesita comandos para establecer comunicacion.
- helm repo list : repos agregados
- helm ls : Charts descargados
- helm install nombre -n namespace el_resto : Instalar en un namespace
- helm ls -A : Todos los charts instalados
- helm ls -n namespace : Los charts instalados en ese ns
- helm search repo repo_name -l : Te da las versiones disponibles de ese chart
- helm install nombre -n namespace el_resto --version 13.1.2 : Ejemplo de como instalar una version en concreto.
- Ejemplos:
helm install nginx-staging -n nginx-staging bitnami/nginx --version 16.0.0
helm install nginx-prod -n nginx-prod bitnami/nginx --version 18.1.11
# Video 83: Parametros
- En el artifact Hub de Helm, para cada chart si esta bien documentado tendremos su seccion de parametros. Hay globales, comunes, especiales de ese chart, etc. En esta doc aparecen los valores por defecto de cada parametro.
- Hay parametros que aparecen, por ejemplo, como service.type o param.algo.algomas en la doc del artifact hub. Este punto es un separador, es decir si ves service.type, y quieres modificar este parametro en un archivo yaml tendrias que ponerlo asi:
service:
  type: NodePort
Por ejemplo...
