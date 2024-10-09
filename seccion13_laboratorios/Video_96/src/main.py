import mysql.connector
from flask import Flask
import os

app = Flask(__name__)

# debug_mode = os.getenv('DEBUG', False)

@app.route('/') # Peticion get a raiz
def hello():
    return 'Hola Mundo2'

@app.route('/chequeo')
def chequeo():
    return 'OK'

# @app.route('/users')
# def get_users():
#     mydb = mysql.connector.connect(host='db', user='user',password='password',database='db')
#     mycursor = mydb.cursor()
#     mycursor.execute('select * from users')
#     result = mycursor.fetchall()
#     return result
    
if __name__=='__main__':
    # El parámetro debug=debug_mode en app.run() indica si la aplicación debe ejecutarse en 
    # modo de depuración (debug mode) o no, dependiendo del valor de debug_mode.
    app.run(host='0.0.0.0')
    # app.run(host='0.0.0.0', debug=debug_mode)

# NOTA sobre debug_mode: 
# Ventajas:
# Recarga automática del código sin tener que reiniciar el servidor.
# Muestra mensajes de error detallados y un traceback interactivo en el navegador si ocurre una 
# excepción.
# Riesgos:
# No se recomienda usar en producción porque muestra información sensible sobre la aplicación 
# en caso de error.
