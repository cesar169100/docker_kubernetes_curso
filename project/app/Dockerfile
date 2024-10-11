FROM python:3.9.13-buster

RUN apt update 

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN rm -rf /app/requirements.txt
COPY src/ /app/src/

EXPOSE 8000

# Comando normal
CMD python3 /app/src/main.py
