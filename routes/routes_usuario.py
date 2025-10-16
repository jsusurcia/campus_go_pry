from flask import Blueprint, request, jsonify, send_from_directory
from models.model_usuario import Usuario
from tools.jwt_utils import generar_token
from tools.jwt_required import jwt_token_requerido
from tools.security import password_validate
from werkzeug.utils import secure_filename
import os

#Crear un modulo blueprint para implementar el servicio web de usuario (login, cambiar contrasena, agregar, etc)
ws_usuario = Blueprint('ws_usuario', __name__)

#Instanciar a la clase usuario
usuario = Usuario()

#Crear un endpoint para permitir al usuario iniciar sesión(login)
@ws_usuario.route('/login', methods=['POST'])
# @jwt_token_requerido
def login():
    #Obtener los datos que se envian como parámetros de entrada
    data = request.get_json()
    
    #pasar los datos de email y contrasena a variables
    email = data.get('email')
    clave = data.get('clave')
    
    #Validar si contamos con los parámetros de email y contrasena
    if not all([email, clave]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    try:
        #Llamar al método login
        resultado = usuario.login(email, clave)
        
        if resultado: #Si hay resultado
            #retirar la contrasena del resultado antes de imprimir
            resultado.pop('clave', None)
            
            #Generar el token con JWT
            token = generar_token({"usuario_id":resultado['id']}, 60)
            
            #Incluir en el resultado el token generado
            resultado['token'] = token
            
            #Imprimir el resultado
            return jsonify({'status': True, 'data': resultado, 'message':'Inicio de sesión satisfactorio'}), 200
        
        else:
            return jsonify({'status': False, 'data': None, 'message': 'Credenciales incorrectas'}), 401
            
    except Exception as e:
        print(e)
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500

#Crear un endpoint para obtener la foto del usuario mediante su ID
@ws_usuario.route('/usuario/foto/<id>', methods=['GET'])
@jwt_token_requerido
def obtener_foto(id):
    #Validar si se cuenta con el ID para mostrar la foto
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400

    try:
        resultado = usuario.obtener_foto(id)
        if resultado:
            return send_from_directory('uploads/fotos/usuarios', resultado['foto'])
        else:
            return send_from_directory('uploads/fotos/usuarios', 'default.png')
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
#Crear un endpoint para registrar nuevos usuarios
@ws_usuario.route('/usuario/registrar', methods=['POST'])
# @jwt_token_requerido
def registrar():
    #Obtener los datos que se envian como parámetros de entrada
    data = request.get_json()
    
    #pasar los datos a variables
    apellido_paterno = data.get('apellido_paterno')
    apellido_materno = data.get('apellido_materno')
    nombres = data.get('nombres')
    dni = data.get('dni')
    telefono = data.get('telefono')
    email = data.get('email')
    clave = data.get('clave')
    clave_confirmada = data.get('clave_confirmada')
    
    #Validar si contamos con todos los parámetros
    if not all([apellido_paterno, apellido_materno, nombres, dni, telefono, email, clave, clave_confirmada]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    #Validar que las claves coincidan
    if clave != clave_confirmada:
        return jsonify({'status': False, 'data': None, 'message': 'Las contraseñas ingresadas no coinciden'}), 500
    
    #Validar complejidad de la clave
    valida, mensaje = password_validate(clave)
    if not valida:
        return jsonify({'status': False, 'data': None, 'message': mensaje}), 500
    
    #Registrar el usuario
    try:
        resultado = usuario.registrar(apellido_paterno, apellido_materno, nombres, dni, telefono, email, clave)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'Usuario registrado'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'Ocurrió un error al registrar el usuario'}), 500
    except Exception as e:
        print(e)
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
     
@ws_usuario.route('/usuario/actualizar', methods=['PUT'])
# @jwt_token_requerido
def actualizar():
    #Obtener los datos que se envian como parámetros de entrada
    data = request.get_json()
    
    #pasar los datos a variables
    apellido_paterno = data.get('apellido_paterno')
    apellido_materno = data.get('apellido_materno')
    nombres = data.get('nombres')
    dni = data.get('dni')
    telefono = data.get('telefono')
    email = data.get('email')
    id = data.get('id')
    
    #Validar si contamos con todos los parámetros
    if not all([apellido_paterno, apellido_materno, nombres, dni, telefono, email, id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    #Actualizar los datos del usuario
    try:
        resultado = usuario.actualizar(apellido_paterno, apellido_materno, nombres, dni, telefono, email, id)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'Datos del usuario actualizados'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'Ocurrió un error al actualuzar el usuario'}), 500
    except Exception as e:
        print(e)
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
@ws_usuario.route('/usuario/baja', methods=['DELETE'])
# @jwt_token_requerido
def baja():
    #Obtener los datos que se envian como parámetros de entrada
    data = request.get_json()
    
    #pasar los datos a variables
    id = data.get('id')
    
    #Validar si contamos con todos los parámetros
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    #Actualizar los datos del usuario
    try:
        resultado = usuario.dar_baja(id)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'El usuario fue dado de baja exitosamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'Ocurrió un error al dar de baja al usuario'}), 500
    except Exception as e:
        print(e)
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
@ws_usuario.route('/usuario/foto/actualizar', methods=['PUT'])
# @jwt_token_requerido
def actualizar_foto():
    #Obtener los datos que se envian como parámetros de entrada
    data = request.form
    
    #pasar los datos a variables
    foto = request.files.get('foto')
    id = data.get('id')
    
    #Validar si contamos con todos los parámetros
    if not all([foto, id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    #Actualizar la foto del usuario
    try:
        #Cargar la foto del usuario al server
        nombre_foto = None
        
        if foto:
            extension = os.path.splitext(foto.filename)[1]      #Obtiene ".jpg", ".png", etc.
            nombre_foto = secure_filename(f"{id}{extension}")   #Obtiene "3.jpg", "3.png", etc.
            ruta_foto = os.path.join("uploads", "fotos", "usuarios", nombre_foto)
            foto.save(ruta_foto)
        
            resultado = usuario.actualizar_foto(nombre_foto, id)
            if resultado:
                return jsonify({'status': True, 'data': None, 'message': 'Se ha actualizado la foto correctamente'}), 200
            else:
                return jsonify({'status': False, 'data': None, 'message': 'Ocurrió un error al actualizar la foto del usuario'}), 500
        else:
            return jsonify({'status': False, 'data': None, 'message': 'La fotografía no es válida'}), 500
    except Exception as e:
        print(e)
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
@ws_usuario.route('/usuario/actualizar_contrasena', methods=['PUT'])
# @jwt_token_requerido
def actualizar_contrasena():
    #Obtener los datos que se envian como parámetros de entrada
    data = request.get_json()
    
    #pasar los datos a variables
    clave = data.get('contrasena')
    clave_confirmada = data.get('contrasena_confirmada')
    clave_antigua = data.get('contrasena_antigua')
    id = data.get('id')
    
    #Validar si contamos con todos los parámetros
    if not all([clave, clave_confirmada, clave_antigua, id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    #Validar que la contraseña antigua es la correcta
    actual = usuario.verificar_contrasena_actual(id, clave_antigua)
    if not actual:
        return jsonify({'status': False, 'data': None, 'message': 'La contraseña actual es incorrecta'}), 500
    
    #Validar que las claves coincidan
    if clave != clave_confirmada:
        return jsonify({'status': False, 'data': None, 'message': 'Las contraseñas ingresadas no coinciden'}), 500
    
    #Validad que la contrasena nueva no sea igual a la antigua
    if clave_antigua == clave:
        return jsonify({'status': False, 'data': None, 'message': 'La nueva contraseña no puede ser igual a la actual'}), 500
    
    #Validar complejidad de la clave
    valida, mensaje = password_validate(clave)
    if not valida:
        return jsonify({'status': False, 'data': None, 'message': mensaje}), 500
    
    #Actualizar la contrasena del usuario
    try:
        resultado = usuario.actualizar_contrasena(clave, id)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'Se ha actualizado la contraseña correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'Ocurrió un error al actualizar la contraseña del usuario'}), 500
    except Exception as e:
        print(e)
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500