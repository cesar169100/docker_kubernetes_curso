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
6) NOTA IMPORTANTE: Cuando construimos una imagen esta se construye segun la arquitectura del equipo en el que la hicimos. En este caso mi equipo tiene arquitectura amd64 de Intel con linux (tipear uname -a en la terminal para ver), pero tambien hay otras arquitecturas como la arch64. Si subimos una imagen a dockerhub esta se guardara con su arquitectura, supongamos amd64, si despues queremos descargar esta imagen desde un equipo o instancia con arquitetura arch64 entonces no correra en este equipo. Consejo: crea una version de tu imagen para cada arquitectura en la que creas que puede correr. Las MAC y Raspberrypy suelen tener arquitecturas arch/arm (lo mismo)

### Kubernetes con Minikube
# Video 22: Presentacion
Configurar cluster de kubernetes de manera local, en vez e la nube pues eso acarrea costos y es lento.
# Video 23: Cluster local en minikube