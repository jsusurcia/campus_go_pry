from flask import Blueprint, request, jsonify
from models.model_reserva import Reserva
from tools.jwt_required import jwt_token_requerido

ws_reserva = Blueprint('ws_reserva', __name__)

reserva = Reserva()

@ws_reserva.route('/reserva/registrar', methods=['POST'])
# @jwt_token_requerido
def registrar():
    #Obtener los datos enviados como parámetros
    data = request.get_json()
    
    pasajero_id = data.get("pasajero_id")
    fecha_reserva = data.get("fecha_reserva")   #Fecha en que el usuario desea viajar
    observacion = data.get("observacion")
    detalles_viaje = data.get("detalles_viaje")
    
    #Validar si están todos los parámetros
    if not all([pasajero_id, fecha_reserva, observacion, detalles_viaje]):
        return jsonify({
            'status': False, 
            'data': None, 
            'message': 'Faltan datos obligatorios'
        }), 400
    
    #Validar que "detalles_viaje" no sea una lista vacía
    if not isinstance(detalles_viaje, list) or not detalles_viaje:
        return jsonify({'status': False, 'data': None, 'message': 'Detalles de viaje debe ser una lista con al menos un viaje'}), 400
    
    #Registrar la reserva
    try:
        resultado, mensaje = reserva.registrar_reserva(pasajero_id, fecha_reserva, observacion, detalles_viaje)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': mensaje}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': mensaje}), 500
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': f"Error interno: {str(e)}"}), 500
    

@ws_reserva.route('/reserva/anular', methods=['DELETE'])
# @jwt_token_requerido
def anular():
    data = request.get_json()
    
    reserva_id = data.get("reserva_id")
    pasajero_id = data.get("pasajero_id")
    
    if not all([reserva_id, pasajero_id]):
        return jsonify({
            'status': False, 
            'data': None, 
            'message': 'Faltan datos obligatorios'
        }), 400
    
    try:
        resultado, mensaje = reserva.anular_reserva(reserva_id, pasajero_id)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': mensaje}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': mensaje}), 500
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': f"Error interno: {str(e)}"}), 500