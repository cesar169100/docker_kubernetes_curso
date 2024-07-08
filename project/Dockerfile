FROM python:3.9

WORKDIR /app
# Librerias para chatbot con audio
RUN sudo apt-get update
RUN sudo apt-get install libasound-dev
RUN sudo apt-get install portaudio19-dev

COPY requirements.txt /app/requirements.txt
RUN pip install /app/requirements.txt

COPY src /app/src
COPY main.py /app/main.py
# Puerto de exposicion 8008 de fastapi o 8501 para streamlit
# EXPOSE 8008
CMD ["python", "main.py"]