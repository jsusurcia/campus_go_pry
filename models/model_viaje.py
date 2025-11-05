from conexionBD import Conexion

class Viaje:
    def __init__(self):
      pass  
    
    def listar_todos(self, filtros):
        try:
            con = Conexion().open
            cursor = con.cursor()

            sql_base = """
            SELECT vi.asientos_disponibles, vi.asientos_ofertados, vi.destino, es.nombre AS estado, 
                vi.fecha_hora_salida, vi.lat_destino, vi.lat_partida, vi.lng_destino, vi.lng_partida, 
                vi.punto_partida, vi.restricciones, ve.color AS vehiculo_color, ve.id AS vehiculo_id, 
                ve.marca AS vehiculo_marca, ve.modelo AS vehiculo_modelo, ve.placa AS vehiculo_placa, 
                vi.id AS viaje_id
            FROM viaje vi
            INNER JOIN estado es ON vi.estado_id = es.id
            INNER JOIN vehiculo ve ON vi.vehiculo_id = ve.id
            """

            where_clause = []
            parametros = []

            if filtros.get('desde') and filtros.get('hasta'):
                where_clause.append("vi.fecha_hora_salida BETWEEN %s AND %s")
                parametros.append(filtros['desde'])
                parametros.append(filtros['hasta'])

            texto_busqueda = filtros.get('texto_busqueda')
            campo_busqueda = filtros.get('campo_busqueda')
            if texto_busqueda and campo_busqueda:
                if campo_busqueda == 'destino':
                    where_clause.append("vi.destino LIKE %s")
                    parametros.append(f"%{texto_busqueda}%")
                elif campo_busqueda == 'punto_partida':
                    where_clause.append("vi.punto_partida LIKE %s")
                    parametros.append(f"%{texto_busqueda}%")

            if filtros.get('asientos_disponibles') == True:
                where_clause.append("vi.asientos_disponibles > 0")

            if filtros.get('sin_restricciones') == True:
                where_clause.append("vi.restricciones = 'Ninguna'")

            sql_final = sql_base
            if where_clause:
                sql_final += " WHERE " + " AND ".join(where_clause)
            sql_final += ";"

            cursor.execute(sql_final, parametros)
            rows = cursor.fetchall()

            viajes = []
            for r in rows:
                viaje = {
                    "viaje_id": r["viaje_id"],
                    "asientos_disponibles": r["asientos_disponibles"],
                    "asientos_ofertados": r["asientos_ofertados"],
                    "destino": r["destino"],
                    "estado": r["estado"],
                    "fecha_hora_salida": str(r["fecha_hora_salida"]),
                    "lat_destino": r["lat_destino"],
                    "lat_partida": r["lat_partida"],
                    "lng_destino": r["lng_destino"],
                    "lng_partida": r["lng_partida"],
                    "punto_partida": r["punto_partida"],
                    "restricciones": r["restricciones"],
                    "vehiculo": {
                        "id": r["vehiculo_id"],
                        "color": r["vehiculo_color"],
                        "marca": r["vehiculo_marca"],
                        "modelo": r["vehiculo_modelo"],
                        "placa": r["vehiculo_placa"]
                    }
                }
                viajes.append(viaje)

            return viajes

        except Exception as e:
            print(f"Error, ocurrió algo: {e}")
            return None
        finally:
            cursor.close()
            con.close()

    def obtener_usuarios_id(self, viaje_id):
        try:
            con = Conexion().open
            cursor = con.cursor()

            sql = """
            SELECT DISTINCT re.pasajero_id 
                FROM reserva re
                INNER JOIN reserva_viaje rv ON rv.reserva_id = re.id
                WHERE rv.viaje_id = %s;
            """

            cursor.execute(sql, [viaje_id])
            rows = cursor.fetchall()
            usuarios = [r['pasajero_id'] for r in rows]
            return usuarios

        except Exception as e:
            print(f"Error al obtener usuarios por viaje: {e}")
            return None
        finally:
            cursor.close()
            con.close()