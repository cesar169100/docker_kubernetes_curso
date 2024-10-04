FROM python:3.9.13-buster

# Instalamos supervisor, usar yum en vez de apt si la imagen es amazon linux, por ejemplo
RUN apt update 
RUN apt-get install supervisor -y

WORKDIR /app
# Copiamos el archivo conf
COPY supervisor_services.conf /etc/supervisor/conf.d/
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN rm -rf /app/requirements.txt
COPY src/ /app/src/

EXPOSE 5000

# Comando normal
# CMD python3 /app/src/main.py
# Comando supervisor
CMD supervisord -n -c /etc/supervisor/supervisord.conf

# NOTA: supervisord.conf es el archivo principal, no supervisor_services.conf pues este ya 
# se incluye en el principal. Por eso supervisord.conf es el que se ejecuta en CMD