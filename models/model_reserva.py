from conexionBD import Conexion
from datetime import datetime, timedelta

class Reserva:
    def __init__(self):
        pass
    
    def registrar_reserva(self, pasajero_id, fecha_reserva, observacion, detalles_viaje):
        ESTADO_RESERVA_ACTIVA = 14
        try:
            con = Conexion().open
            cursor = con.cursor()

            # Insertar en reserva
            sql_reserva = """
                INSERT INTO reserva (pasajero_id, fecha_reserva, observacion)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql_reserva, [pasajero_id, fecha_reserva, observacion])
            reserva_id = cursor.lastrowid
            if not reserva_id:
                raise Exception("No se pudo obtener el ID de la reserva")

            # Obtener fecha_hora_reserva (si es necesario)
            sql_fecha_hora = "SELECT fecha_hora_reserva FROM reserva WHERE id = %s"
            cursor.execute(sql_fecha_hora, [reserva_id])
            fecha_hora_reserva = cursor.fetchone()['fecha_hora_reserva']

            # Preparar sentencias SQL
            sql_actualizar_viaje = """
                UPDATE viaje
                SET asientos_disponibles = asientos_disponibles - 1
                WHERE id = %s AND asientos_disponibles > 0
            """
            sql_reserva_viaje = """
                INSERT INTO reserva_viaje (reserva_id, viaje_id, estado_id)
                VALUES (%s, %s, %s)
            """
            sql_validar_viaje = """
                SELECT fecha_hora_salida
                FROM viaje
                WHERE id = %s
            """

            # Procesar detalles del viaje
            for detalle in detalles_viaje:
                viaje_id = detalle.get("viaje_id")
                if not viaje_id:
                    raise Exception("Falta el ID del viaje en el detalle")

                cursor.execute(sql_validar_viaje, [viaje_id])
                viaje_info = cursor.fetchone()
                if not viaje_info:
                    raise Exception(f"No existe un viaje con el ID {viaje_id}")

                fecha_salida = viaje_info['fecha_hora_salida']
                if fecha_hora_reserva > fecha_salida:
                    raise Exception(f"No puedes hacer reservas para el viaje {viaje_id} con fecha ya pasada")

                # Actualizar asientos
                cursor.execute(sql_actualizar_viaje, [viaje_id])
                if cursor.rowcount == 0:
                    raise Exception(f"No hay asientos disponibles en el viaje con ID {viaje_id}")

                # Insertar reserva_viaje
                cursor.execute(sql_reserva_viaje, [reserva_id, viaje_id, ESTADO_RESERVA_ACTIVA])

            con.commit()
            return True, "Reserva y detalles registrados con éxito"
        
        except Exception as e:
            con.rollback()
            return False, f"Error al registrar la reserva: {str(e)}"
        
        finally:
            cursor.close()
            con.close()

            
    def anular_reserva(self, reserva_id, pasajero_id):
        ESTADO_RESERVA_ANULADA = 18
        try:
            con = Conexion().open
            cursor = con.cursor()

            # Verificar que la reserva existe y pertenece al pasajero
            sql_validar_reserva = """
                SELECT id FROM reserva
                WHERE id = %s AND pasajero_id = %s
            """
            cursor.execute(sql_validar_reserva, [reserva_id, pasajero_id])
            if not cursor.fetchone():
                raise Exception("La reserva no existe o no pertenece al pasajero")

            # Obtener los viajes activos (no anulados) asociados a la reserva
            sql_obtener_viajes = """
                SELECT v.id AS viaje_id, v.fecha_hora_salida
                FROM viaje v
                JOIN reserva_viaje rv ON v.id = rv.viaje_id
                WHERE rv.reserva_id = %s AND rv.estado_id not in (17, 18)
            """
            cursor.execute(sql_obtener_viajes, [reserva_id,])
            viajes = cursor.fetchall()

            if not viajes:
                raise Exception("La reserva ya fue anulada o no tiene viajes asociados")

            # Validar que falte más de 1 hora para la salida de cada viaje
            ahora = datetime.now()
            for viaje in viajes:
                fecha_salida = viaje['fecha_hora_salida']
                if fecha_salida - ahora <= timedelta(hours=1):
                    raise Exception(
                        f"No se puede anular la reserva. El viaje con ID {viaje['viaje_id']} está a menos de 1 hora de iniciar."
                    )

            # SQLs para actualizar
            sql_restaurar_asientos = """
                UPDATE viaje
                SET asientos_disponibles = asientos_disponibles + 1
                WHERE id = %s
            """
            sql_actualizar_estado_reserva_viaje = """
                UPDATE reserva_viaje
                SET estado_id = %s
                WHERE reserva_id = %s AND viaje_id = %s
            """

            # Anular la reserva y restaurar asientos
            for viaje in viajes:
                viaje_id = viaje['viaje_id']
                cursor.execute(sql_restaurar_asientos, [viaje_id])
                cursor.execute(sql_actualizar_estado_reserva_viaje, [ESTADO_RESERVA_ANULADA, reserva_id, viaje_id])

            con.commit()
            return True, "La reserva fue anulada correctamente"

        except Exception as e:
            con.rollback()
            return False, f"Error al anular la reserva: {str(e)}"

        finally:
            cursor.close()
            con.close()