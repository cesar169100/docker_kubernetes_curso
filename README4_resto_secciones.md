# Intro
En este documento se abordaran el resto de secciones del curso
# Video 67: Prometheus y Grafana
- Prometheus es un software libre para monitoreo de eventos y alertas. Sitio de prometheus: https://prometheus.io/
- En el codigo comandos del video 67 estan las instrucciones de la instalacion sencilla de prometheus y Grafana. Hay que instalar metric server
- Cosas como metricas custom, ambientes prod etc en prometheus no se veran en este curso, incluso hay una certificacion en prometheus.
- Prometheus tiene su propio lenguaje para hacer query a los datos que se almacenan: promql. Buscarlo en el navegador para ver como hacer querys
- Los recursos de prometheus no se levantaron por completo debido a que hay unos claims que no se estan asociando a un volumen, no existen al parecer volumenes. Mi hipotests es que, o hace falta un storageclass para aprovisionamiento o los recursos son insuficientes pues los claims traen request de hasta 8Gi de memoria, cosa que las maquinas t3.small no tienen, entonces seria cosa de probar con maquinas mas grandes a ver si jala, cosa q no hare por costos $$$ o implementar un autoscaler para que lo haga solo.
- Grafana funciono bien. Esta interfaz es la que se usa, lo primero es ir al conexiones y agregar un data source, entre ellos esta Prometheus y la url seria http://prometheus-server y lo demas igual, dar save and test, esto porque ambos estan configurados en el mismo namspace. Luego en explore ya podemos correr querys
- En grafana dashboards (pagina de grafana) podremos encontrar dashboards q la gente ha usado, en particular podemos buscar kubernetes y veremos esos dashboards para kubernetes. Si elijes un dash este traera un codigo de identificacion y desde grafana podras importar ese dasboard con su codigo.
- El dashboard 10000 de kubernetes es basico