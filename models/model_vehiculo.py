from conexionBD import Conexion

class Vehiculo:
    def __init__(self):
        pass
    
    def listar_todos(self):
        con = Conexion().open   #Abrir conexión
        cursor = con.cursor()   #Crear cursor
        sql = """
            select 
                concat(us.apellido_paterno, ' ', us.apellido_materno, ', ', us.nombres) as 'conductor', 
                ve.marca, 
                ve.modelo, 
                ve.color, 
                ve.pasajeros, 
                es.nombre
            from vehiculo ve
            inner join usuario as us on ve.conductor_id = us.id
            inner join estado as es on ve.estado_id = es.id
        """
        cursor.execute(sql)             #Ejecutar sentencia
        resultados = cursor.fetchall()  #Obtener resultados
        cursor.close()                  #Cerrar cursor
        con.close()                     #Cerrar conexión
        
        return resultados if resultados else None
        
    def obtener_vehiculo_id(self, id):
        con = Conexion().open   #Abrir conexión
        cursor = con.cursor()   #Crear cursor
        sql = """
            select 
                concat(us.apellido_paterno, ' ', us.apellido_materno, ', ', us.nombres) as 'conductor', 
                ve.marca, 
                ve.modelo, 
                ve.color, 
                ve.pasajeros, 
                es.nombre
            from vehiculo ve
            inner join usuario as us on ve.conductor_id = us.id
            inner join estado as es on ve.estado_id = es.id
            where ve.id = %s
        """
        cursor.execute(sql, [id,])          #Ejecutar sentencia
        resultados = cursor.fetchone()      #Obtener resultados
        cursor.close()                      #Cerrar cursor
        con.close()                         #Cerrar conexión
        
        return resultados if resultados else None
    
    def insertar_vehiculo(self, id_conductor, marca, modelo, placa, color, pasajeros):
        con = Conexion().open   #Abrir conexión
        cursor = con.cursor()   #Crear cursor
        sql = """
            insert into vehiculo (conductor_id, marca, modelo, placa, color, pasajeros, estado_id)
            values (%s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(sql, [id_conductor, marca, modelo, placa, color, pasajeros, '5'])     #Ejecutar sentencia
            con.commit()            #Guardar cambios
            cursor.close()          #Cerrar cursor
            con.close()             #Cerrar conexión
            return True
        except Exception as e:
            con.rollback()          #Hacer rollback en caso de error
            cursor.close()          #Cerrar cursor
            con.close()             #Cerrar conexión
            return None
    
    def actualizar_vehiculo(self, id_conductor, marca, modelo, placa, color, pasajeros, id):
        con = Conexion().open   #Abrir conexión
        cursor = con.cursor()   #Crear cursor
        sql = """
            update vehiculo 
            set conductor_id = %s,
                marca = %s,
                modelo = %s,
                placa = %s,
                color = %s,
                pasajeros = %s
            where id = %s
        """
        
        try:
            cursor.execute(sql, [id_conductor, marca, modelo, placa, color, pasajeros, id])     #Ejecutar sentencia
            con.commit()            #Guardar cambios
            cursor.close()          #Cerrar cursor
            con.close()             #Cerrar conexión
            return True
        except Exception as e:
            con.rollback()          #Hacer rollback en caso de error
            cursor.close()          #Cerrar cursor
            con.close()             #Cerrar conexión
            return None
        
    def dar_baja_vehiculo(self, id):
        con = Conexion().open   #Abrir conexión
        cursor = con.cursor()   #Crear cursor
        sql = """
            update vehiculo 
            set estado_id = 8
            where id = %s
        """
        
        try:
            cursor.execute(sql, [id, ])     #Ejecutar sentencia
            con.commit()            #Guardar cambios
            cursor.close()          #Cerrar cursor
            con.close()             #Cerrar conexión
            return True
        except Exception as e:
            con.rollback()          #Hacer rollback en caso de error
            cursor.close()          #Cerrar cursor
            con.close()             #Cerrar conexión
            return None