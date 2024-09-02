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
# Video 69: Presentacion de la seccion ECR
- ECR servicio de registro de containers en aws, crear nuestras imagenes y subirlas ahi y no depender de dockerHub y es mas seguro.