from conexionBD import Conexion

class Viaje:
    def __init__(self):
      pass  
    
    def listar_todos(self, filtros):
        try:
            con = Conexion().open   #Abrir conexión
            cursor = con.cursor()   #Crear cursor
            
            #Consulta base
            sql_base = """
            SELECT vi.asientos_disponibles, vi.asientos_ofertados, vi.destino, es.nombre AS estado, 
                vi.fecha_hora_salida, vi.lat_destino, vi.lat_partida, vi.lng_destino, vi.lng_partida, 
                vi.punto_partida, vi.restricciones, ve.color, ve.id AS vehiculo_id, ve.marca, 
                ve.modelo, ve.placa, vi.id AS viaje_id
            FROM 
                viaje vi
            INNER JOIN 
                estado es ON vi.estado_id = es.id
            INNER JOIN 
                vehiculo ve ON vi.vehiculo_id = ve.id
            """
            
            #Construcción dinámica de cláusulas WHERE
            where_clause = []   #Condicionales
            parametros = []     #Valores
            
            #Agregar validación de fecha
            if filtros.get('desde') and filtros.get('hasta'):
                where_clause.append("vi.fecha_hora_salida BETWEEN %s AND %s")
                parametros.append(filtros['desde'])
                parametros.append(filtros['hasta'])
                
            #Agregar validación de búsqueda (texto, campo)
            texto_busqueda = filtros.get('texto_busqueda')
            campo_busqueda = filtros.get('campo_busqueda')
            if texto_busqueda and campo_busqueda:
                if campo_busqueda == 'destino':
                    where_clause.append("vi.destino LIKE %s")
                    parametros.append(f"%{texto_busqueda}%")
                elif campo_busqueda == 'punto_partida':
                    where_clause.append("vi.punto_partida LIKE %s")
                    parametros.append(f"%{texto_busqueda}%")
            
            #Agregar validación de asientos
            if filtros.get('asientos_disponibles') == True:
                where_clause.append("vi.asientos_disponibles > 0")
                
            #Agregar validación de restricciones
            if filtros.get('sin_restricciones') == True:
                where_clause.append("vi.restricciones = 'Ninguna'")
                
            #Ensamblar la consulta final
            sql_final = sql_base
            if where_clause:
                sql_final += " WHERE " + " AND ".join(where_clause)
            sql_final += ";"
            
            print(f"SQL: {cursor.mogrify(sql_final, parametros)}")
            cursor.execute(sql_final, parametros)
            resultado = cursor.fetchall()
            return resultado
        except Exception as e:
            print(f"Error, ocurrió algo: {e}")
            return None
        finally:
            cursor.close()
            con.close()