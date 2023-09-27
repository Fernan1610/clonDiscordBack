from database.conexion_db import execute_db, commint_db, fetch_all, fetch_one
import mysql.connector


class Servidor:
    def __init__(self):
        self

    def crear_servidor(self, nombre, avatar, activo):
        try:
            avatar_bytes = None
            if avatar != None:
                avatar_bytes = avatar.read()

            query = "INSERT INTO servidores(nombre, avatar, activo) VALUES (%s,%s,%s);"
            value = (nombre, avatar_bytes, activo)
            commint_db(query, value)
            return True
        except mysql.connector.Error as e:
            print(f"ERROR crear_servidor: {e.args}")
            raise f'Error MySQL al insertar el servidor: {str(e)}'
        except Exception as e:
            print(f"ERROR crear_servidor: {e.args}")
            raise f'Se produjo un error al insertar registrar el servidor: {str(e)}'

    def update_servidor(self, nombre, avatar, activo):
        try:
            avatar_bytes = self.img_bytes(avatar)
            query = "UPDATE servidores SET nombre = %s, avatar = %s, activo = %s WHERE id = %s;"
            value = (nombre, avatar_bytes, activo, id)
            commint_db(query, value)
            return True
        except mysql.connector.Error as e:
            print(f"ERROR update_servidor: {e.args}")
            raise f'Error MySQL al actualizar el servidor: {str(e)}'
        except Exception as e:
            print(f"ERROR update_servidor: {e.args}")
            raise f'Se produjo un error al actualizar el servidor: {str(e)}'

    def img_bytes(self, avatar):
        avatar_bytes = None
        if (avatar != b'' and not isinstance(avatar, bytes)):
            with open(avatar, 'rb') as file:
                avatar_bytes = file.read()
        return avatar_bytes

    def delete_servidor(self, id):
        try:
            query = f"DELETE FROM servidores WHERE id = '{id}';"
            execute_db(query)
            return True
        except mysql.connector.Error as e:
            print(F"ERROR delete_servidor {e.args}")
            raise f'Error MySQL al borrar el servidor: {str(e)}'
        except Exception as e:
            print(F"ERROR delete_servidor {e.args}")
            raise f'Se produjo un error al borrar el servidor: {str(e)}'

    def get_servidor_by_nombre(self, server_name):
        try:
            query = f"select * from servidores where nombre = '{server_name}'"
            return fetch_one(query)
        except mysql.connector.Error as e:
            print(f"ERROR get_servidor_by_nombre: {e.args}")
            raise f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(f"ERROR get_servidor_by_nombre: {e.args}")
            raise f'Se produjo un error al insertar registrar el mensaje: {str(e)}'
