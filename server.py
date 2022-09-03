from flask import Flask, request, jsonify, render_template
import numpy as np
from joblib import load
from werkzeug.utils import secure_filename
import os

#Cargar el modelo
dt = load('modelo.joblib')

#Generar el servidor (Back-end)
servidorWeb = Flask(__name__)


@servidorWeb.route("/formulario",methods=['GET'])
def formulario():
    return render_template('pagina.html')

#Envio de datos a través de Archivos
@servidorWeb.route('/modeloFile', methods=['POST'])
def modeloFile():
    f = request.files['file']
    filename=secure_filename(f.filename)
    path=os.path.join(os.getcwd(),'files',filename)
    f.save(path)
    file = open(path, "r")

    for x in file:
        info=x.split()
    print(info)
    datosEntrada = np.array([
            float(info[0]),
            float(info[1]),
            float(info[2]),
            float(info[3]),
            float(info[4])
        ])
    #Utilizar el modelo
    resultado=dt.predict(datosEntrada.reshape(1,-1))
    #Regresar la salida del modelo
    return jsonify({"Resultado":str(resultado[0])})

#Envio de datos a través de Forms
@servidorWeb.route('/modeloForm', methods=['POST'])
def modeloForm():
    #Procesar datos de entrada
    contenido = request.get_json()
    
    origin_data, dest_data = [0,0,0], [0,0,0]
    
    id_origin = int(contenido["origin"])
    origin_data[id_origin] = 1
     
    id_dest = int(contenido["destination"]) 
    dest_data[id_dest] = 1

    datosEntrada = np.array([
            contenido['cryoSleep'],
            contenido['age'],
            contenido['vip'],
            origin_data[0],
            origin_data[1],
            origin_data[2],
            dest_data[0],
            dest_data[1],
            dest_data[2],
            ])
    
    #Utilizar el modelo
    resultado=dt.predict(datosEntrada.reshape(1,-1))
    #Regresar la salida del modelo
    print({"Resultado":str(resultado[0])})
    return jsonify({"Resultado":str(resultado[0])})


#Envio de datos a través de JSON
@servidorWeb.route('/modelo', methods=['POST'])
def modelo():
    #Procesar datos de entrada
    contenido = request.json
    print(contenido)
    datosEntrada = np.array([
            contenido['cryoSleep'],
            contenido['age'],
            contenido['vip'],
            contenido['origin'],
            contenido['destination'],
            ])
    #Utilizar el modelo
    resultado=dt.predict(datosEntrada.reshape(1,-1))
    #Regresar la salida del modelo
    return jsonify({"Transportado":str(resultado[0])})

if __name__ == '__main__':
    servidorWeb.run(debug=False,host='0.0.0.0',port='8080')
