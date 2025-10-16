from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Usuario:
    def __init__(self):
        self.ph = PasswordHasher()
        
    def login(self, email, clave):
        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        #Definir la sentencia sql
        sql = "select id, apellido_paterno, apellido_materno, nombres, email, clave from usuario where email = %s"
        
        #Ejecutar la sentencia
        cursor.execute(sql,[email])
        
        #Recuperar los datos del usuario
        resultado = cursor.fetchone()
        
        #Cerrar el curso y la conexión
        cursor.close()
        con.close()
        
        if resultado: #Verificando si se encontró al usuario con el email ingresado
            try:
                hash_almacenado = str(resultado['clave'])
                self.ph.verify(hash_almacenado, clave) #Verificando la clave almacenada en la BD con la clave que ingresó el usuario
                return resultado
            except VerifyMismatchError:
                return None
            
        else: #No se ha encontrado al usuario con el email ingreso
            return None
        
    def obtener_foto(self, id):
        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        #Definir la sentencia sql
        sql = "select coalesce(foto, 'x') as foto from usuario where id = %s"
        
        #Ejecutar la sentencia
        cursor.execute(sql,[id, ])
        
        #Recuperar los datos del usuario
        resultado = cursor.fetchone()
        
        #Cerrar el curso y la conexión
        cursor.close()
        con.close()
        
        if resultado and resultado['foto'] != 'x':
            return resultado
        
        #Si no hay foto
        return None
    
    def registrar(self, apellido_paterno, apellido_materno, nombres, dni, telefono, email, clave):
        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        #Definir la sentencia sql
        sql = "insert into usuario (apellido_paterno, apellido_materno, nombres, dni, telefono, email, estado_id, clave) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        
        #Hashear la contraseña
        hash_clave = self.ph.hash(clave)
        
        try:
            #Ejecutar la sentencia
            cursor.execute(sql,[apellido_paterno, apellido_materno, nombres, dni, telefono, email, '1', hash_clave])
            
            #Hacer commit para guardar los cambios
            con.commit()
            
            #Cerrar el curso y la conexión
            cursor.close()
            con.close()
            
            return True
        
        except Exception as e:
            #Si hay error hacer rollback
            con.rollback()
            
            #Cerrar el curso y la conexión
            cursor.close()
            con.close()
            
            return None
         
    def actualizar(self, apellido_paterno, apellido_materno, nombres, dni, telefono, email, id):
        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        #Definir la sentencia sql
        sql = """
            update usuario
            set apellido_paterno = %s,
                apellido_materno = %s,
                nombres = %s,
                dni = %s,
                telefono = %s,
                email = %s,
                fecha_modificacion = now()
            where id = %s;
        """
        
        try:
            #Ejecutar la sentencia
            cursor.execute(sql, [apellido_paterno, apellido_materno, nombres, dni, telefono, email, id])
            
            #Confirmar los datos en la BD
            con.commit()
            
            #Cerrar el cursor y la conexion
            cursor.close()
            con.close()
            
            return True
        except Exception as e:
            #Si ocurrió un error, aplicar rollback
            con.rollback()
            
            #Cerrar el cursor y la conexion
            cursor.close()
            con.close()
            
            return None
        
    def dar_baja(self, id):
        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        #Definir la sentencia sql
        sql = """
            update usuario
            set estado_id = 2,
                fecha_modificacion = now()
            where id = %s;
        """
        
        try:
            #Ejecutar la sentencia
            cursor.execute(sql, [id, ])
            
            #Confirmar los datos en la BD
            con.commit()
            
            #Cerrar el cursor y la conexion
            cursor.close()
            con.close()
            
            return True
        except Exception as e:
            #Si ocurrió un error, aplicar rollback
            con.rollback()
            
            #Cerrar el cursor y la conexion
            cursor.close()
            con.close()
            
            return None
        
    def actualizar_foto(self, foto, id):
        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        #Definir la sentencia sql
        sql = """
            update usuario
            set foto = %s,
                fecha_modificacion = now()
            where id = %s;
        """
        
        try:
            #Ejecutar la sentencia
            cursor.execute(sql, [foto, id])
            
            #Confirmar los datos en la BD
            con.commit()
            
            #Cerrar el cursor y la conexion
            cursor.close()
            con.close()
            
            return True
        except Exception as e:
            #Si ocurrió un error, aplicar rollback
            con.rollback()
            
            #Cerrar el cursor y la conexion
            cursor.close()
            con.close()
            
            return None
        
        
    def verificar_contrasena_actual(self, id, clave):
        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        #Definir la sentencia sql
        sql = "select clave from usuario where id = %s"
        
        #Ejecutar la sentencia
        cursor.execute(sql,[id,])
        
        #Recuperar los datos del usuario
        resultado = cursor.fetchone()
        
        #Cerrar el curso y la conexión
        cursor.close()
        con.close()
        
        if resultado:
            hash_almacenado = resultado['clave']
            try:
                #Verificar la contraseña con el verificddor
                if self.ph.verify(hash_almacenado, clave):
                    return True
            except Exception as e:
                return False
            return True
        
        return False
    
    def actualizar_contrasena(self, clave, id):
        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        #Definir la sentencia sql
        sql = """
            update usuario
            set clave = %s,
                fecha_modificacion = now()
            where id = %s;
        """
        
        #Hashear la contraseña
        hash_clave = self.ph.hash(clave)
        
        try:
            #Ejecutar la sentencia
            cursor.execute(sql, [hash_clave, id])
            
            #Confirmar los datos en la BD
            con.commit()
            
            #Cerrar el cursor y la conexion
            cursor.close()
            con.close()
            
            return True
        except Exception as e:
            #Si ocurrió un error, aplicar rollback
            con.rollback()
            
            #Cerrar el cursor y la conexion
            cursor.close()
            con.close()
            
            return None