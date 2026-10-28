from app.database import get_db_connection

class VehiculoIOTService:
    def __init__(self):
        pass

    def obtener_vehiculos(self):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_obtener_vehiculos")
                return cursor.fetchall()
        finally:
            connection.close()

    def obtener_vehiculo(self, id_vehiculo: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_obtener_vehiculo", (id_vehiculo,))
                return cursor.fetchone()
        finally:
            connection.close()

    def crear_vehiculo(self, nombre: str, modelo: str, descripcion: str, microcontrolador: str):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_crear_vehiculo", (nombre, modelo, descripcion, microcontrolador))
                connection.commit()
                return cursor.fetchone()
        finally:
            connection.close()

    def actualizar_vehiculo(self, id_vehiculo: int, nombre: str, modelo: str, descripcion: str, microcontrolador: str, activo: bool):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_actualizar_vehiculo", (id_vehiculo, nombre, modelo, descripcion, microcontrolador, activo))
                connection.commit()
                return {"message": "Vehículo actualizado correctamente"}
        finally:
            connection.close()

    def eliminar_vehiculo(self, id_vehiculo: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_eliminar_vehiculo", (id_vehiculo,))
                connection.commit()
                return {"message": "Vehículo eliminado correctamente"}
        finally:
            connection.close()

    def obtener_comandos_vehiculo(self, id_vehiculo: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_obtener_comandos_vehiculo", (id_vehiculo,))
                return cursor.fetchall()
        finally:
            connection.close()

    def crear_comando(self, id_vehiculo: int, nombre: str, codigo: int, descripcion: str):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_crear_comando", (id_vehiculo, nombre, codigo, descripcion))
                connection.commit()
                return cursor.fetchone()
        finally:
            connection.close()

    def actualizar_comando(self, id_comando: int, nombre: str, codigo: int, descripcion: str, activo: bool):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_actualizar_comando", (id_comando, nombre, codigo, descripcion, activo))
                connection.commit()
                return {"message": "Comando actualizado correctamente"}
        finally:
            connection.close()

    def eliminar_comando(self, id_comando: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_eliminar_comando", (id_comando,))
                connection.commit()
                return {"message": "Comando eliminado correctamente"}
        finally:
            connection.close()

    def obtener_estado(self, id_vehiculo: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_obtener_estado", (id_vehiculo,))
                return cursor.fetchall()
        finally:
            connection.close()

    def actualizar_estado(self, id_vehiculo: int, id_comando: int, conectado: bool):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_actualizar_estado", (id_vehiculo, id_comando, conectado))
                connection.commit()
        finally:
            connection.close()

    def registrar_historial(self, id_vehiculo: int, id_comando: int, origen: str):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_registrar_historial", (id_vehiculo, id_comando, origen))
                connection.commit()
        finally:
            connection.close()

    def obtener_historial(self, id_vehiculo: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_obtener_historial", (id_vehiculo,))
                resultados = cursor.fetchall()
                return resultados[:10]  
        finally:
            connection.close()

    def obtener_demos(self, id_vehiculo: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_obtener_demos", (id_vehiculo,))
                return cursor.fetchall()
        finally:
            connection.close()

    def crear_demo(self, id_vehiculo: int, nombre: str, descripcion: str):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_crear_demo", (id_vehiculo, nombre, descripcion))
                connection.commit()
                return cursor.fetchone()
        finally:
            connection.close()

    def actualizar_demo(self, id_demo: int, nombre: str, descripcion: str, activo: bool):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_actualizar_demo", (id_demo, nombre, descripcion, activo))
                connection.commit()
                return {"message": "Demo actualizada correctamente"}
        finally:
            connection.close()

    def eliminar_demo(self, id_demo: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_eliminar_demo", (id_demo,))
                connection.commit()
                return {"message": "Demo eliminada correctamente"}
        finally:
            connection.close()

    def obtener_movimientos_demo(self, id_demo: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_obtener_movimientos_demo", (id_demo,))
                return cursor.fetchall()
        finally:
            connection.close()

    def agregar_movimiento_demo(self, id_demo: int, id_comando: int, orden: int, duracion_ms: int, pausa_ms: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_agregar_movimiento_demo", (id_demo, id_comando, orden, duracion_ms, pausa_ms))
                connection.commit()
                return {"message": "Movimiento de demo agregado exitosamente"}
        finally:
            connection.close()

    def actualizar_movimiento_demo(self, id_demo_movimiento: int, id_comando: int, orden: int, duracion_ms: int, pausa_ms: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_actualizar_movimiento_demo", (id_demo_movimiento, id_comando, orden, duracion_ms, pausa_ms))
                connection.commit()
                return {"message": "Movimiento actualizado"}
        finally:
            connection.close()

    def eliminar_movimiento_demo(self, id_demo_movimiento: int):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_eliminar_movimiento_demo", (id_demo_movimiento,))
                connection.commit()
                return {"message": "Movimiento eliminado"}
        finally:
            connection.close()