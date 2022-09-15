from flask import Flask, request, jsonify, render_template
import numpy as np
from joblib import load
from werkzeug.utils import secure_filename
import os
import dynamo
import requests

#Cargar el modelo
dt = load('modeloTitanic.joblib')

#Generar el servidor (Back-end)
servidorWeb = Flask(__name__)


@servidorWeb.route("/formulario",methods=['GET'])
def formulario():
    return render_template('pagina.html')


#Envio de datos a través de Forms
@servidorWeb.route('/modeloForm', methods=['POST'])
def modeloForm():
    #Procesar datos de entrada
    contenido = request.get_json()
    print(contenido)
    origin_data, dest_data = [0,0,0], [0,0,0]

    id_origin = int(contenido["origin"])
    origin_data[id_origin] = 1
    id_dest = int(contenido["destination"]) 
    dest_data[id_dest] = 1

    #Checar si id coincide con el colab
    cabin_section = [0 for _ in range(8)]
    print(len(cabin_section))
    id_section = int(contenido["cabinSection"])
    cabin_section[id_section] = 1

    datosEntrada = np.array([
            contenido['cryoSleep'],
            contenido['age'],
            contenido['vip'],
            contenido['roomService'],
            contenido['foodCourt'],
            contenido['shoppingMall'],
            contenido['spa'],
            contenido['VRDeck'],
            contenido['cabinType'],
            origin_data[0],
            origin_data[1],
            origin_data[2],
            dest_data[0],
            dest_data[1],
            dest_data[2],
            cabin_section[0],
            cabin_section[1],
            cabin_section[2],
            cabin_section[3],
            cabin_section[4],
            cabin_section[5],
            cabin_section[6],
            cabin_section[7]])
    
    #Utilizar el modelo
    resultado=dt.predict(datosEntrada.reshape(1,-1))
    #Guardar viaje en base de datosEntrada
    dynamo.write_to_dynamo(contenido, resultado[0])
    #Regresar la salida del modelo
    print({"Resultado":str(resultado[0])})

    #AWS lambda code insert element in dynamodb
    #URL = 'https://z94j2h4sol.execute-api.us-east-2.amazonaws.com/default/scores'
    # payload = {
    #     'initials': 'MA',
    #     'score': 15,
    #     "result": str(resultado[0])
    # }
    # result = requests.post(URL, json=payload)
    # print(result.status_code)
    # body = result.json()
    # print("mike", body['message'])

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
