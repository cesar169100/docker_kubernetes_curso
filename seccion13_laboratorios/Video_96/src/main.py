from flask import Flask

app = Flask(__name__)

@app.route('/') # Peticion get a raiz
def hello():
    return 'Hola Mundo'

@app.route('/chequeo')
def chequeo():
    return 'OK'

if __name__=='__main__':
    app.run(host='0.0.0.0')
