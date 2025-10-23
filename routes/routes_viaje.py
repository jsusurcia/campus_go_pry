from flask import Blueprint, request, jsonify
from models.model_viaje import Viaje

ws_viaje = Blueprint('ws_viaje', __name__)
viaje = Viaje()

#Endpoint para listar viajes con parámetros
@ws_viaje.route('/viaje/listado', methods=['POST'])
def listar_todos():
    try:
        filtros = request.json
        
        #Suponiendo que las fechas son obligatorias
        if not filtros.get('desde') or not filtros.get('hasta'):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
        
        try:
            resultado = viaje.listar_todos(filtros)
            if resultado:
                return jsonify({'status': True, 'data': resultado, 'message': 'Viajes encontrados exitosamente'}), 200
            else:
                return jsonify({'status': False, 'data': None, 'message': 'No se encontraron viajes con estas especificaciones'}), 401
        except Exception as e:
            return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    except Exception as e:
        print(e)