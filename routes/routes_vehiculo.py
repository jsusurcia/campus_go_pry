from flask import Blueprint, request, jsonify
from models.model_vehiculo import Vehiculo

ws_vehiculo = Blueprint('ws_vehiculo', __name__)

vehiculo = Vehiculo()

#Endpoint para listar todos los vehículos
@ws_vehiculo.route('/vehiculo/obtener', methods=['GET'])
# @jwt_token_requerido
def obtener_todos():
    try:
        resultado = vehiculo.listar_todos()
        if resultado:
            return jsonify({'status': True, 'data': resultado, 'message':'Vehículos listados correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'No se encontraron vehículos habilitados'}), 401
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500


#Endpoint para obtener un vehículo por su ID
@ws_vehiculo.route('/vehiculo/obtener/<id>', methods=['GET'])
# @jwt_token_requerido
def obtener_por_id(id):
    try:
        resultado = vehiculo.obtener_vehiculo_id(id)
        if resultado:
            return jsonify({'status': True, 'data': resultado, 'message':'Vehículo encontrado'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'No se encontró el vehículo'}), 401
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500


#Endpoint para insertar un nuevo vehículo   
@ws_vehiculo.route('/vehiculo/insertar', methods=['POST'])
# @jwt_token_requerido
def insertar():
    data = request.get_json()
    
    id_conductor = data.get('id_conductor')
    marca = data.get('marca')
    modelo = data.get('modelo')
    placa = data.get('placa')
    color = data.get('color')
    pasajeros = data.get('pasajeros')
    
    if not all([id_conductor, marca, modelo, placa, color, pasajeros]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    try:
        resultado = vehiculo.insertar_vehiculo(id_conductor, marca, modelo, placa, color, pasajeros)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'Vehículo registrado correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'Ocurrió un error al registrar el vehículo'}), 500
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500


#Endpoint para actualizar los datos de un vehículo       
@ws_vehiculo.route('/vehiculo/actualizar', methods=['PUT'])
# @jwt_token_requerido
def actualizar():
    data = request.get_json()
    
    id_conductor = data.get('id_conductor')
    marca = data.get('marca')
    modelo = data.get('modelo')
    placa = data.get('placa')
    color = data.get('color')
    pasajeros = data.get('pasajeros')
    id = data.get('id')
    
    if not all([id_conductor, marca, modelo, placa, color, pasajeros, id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    try:
        resultado = vehiculo.actualizar_vehiculo(id_conductor, marca, modelo, placa, color, pasajeros, id)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'Vehículo actualizado correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'Ocurrió un error al actualizar el vehículo'}), 500
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    

#Endpoint para dar de bajar un vehículo
@ws_vehiculo.route('/vehiculo/baja', methods=['PUT'])
# @jwt_token_requerido
def baja():
    data = request.get_json()
    
    id = data.get('id')
    
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    try:
        resultado = vehiculo.dar_baja_vehiculo(id)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'Vehículo dado de baja correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'Ocurrió un error al dar de baja al vehículo'}), 500
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500