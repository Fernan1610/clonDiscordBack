from database.conexion_db import execute_db, commint_db, fetch_all, fetch_one
import mysql.connector


class Canal:
    def __init__(self):
        self

    def crear_canal(self, nombre, servidor_id, activo):
        try:
            query = "INSERT INTO canales(nombre, servidor_id,activo) VALUES (%s,%s,%s);"
            value = (nombre, servidor_id, activo)
            commint_db(query, value)
            return True
        except mysql.connector.Error as e:
            print(f"ERROR crear_canal: {e.args}")
            return f'Error MySQL al insertar el canal: {str(e)}'
        except Exception as e:
            print(f"ERROR crear_canal: {e.args}")
            return f'Se produjo un error al insertar registrar el canal: {str(e)}'

    def get_canales(self, servidor_id):
        try:
            query = f"SELECT * FROM canales WHERE servidor_id = '{servidor_id}' AND activo = 1;"
            return fetch_all(query)
        except mysql.connector.Error as e:
            print(f"ERROR get_canales: {e.args}")
            return f'Error MySQL al traer los canales: {str(e)}'
        except Exception as e:
            print(f"ERROR get_canales: {e.args}")
            return f'Se produjo un error al traer los canales: {str(e)}'
        
    def get_nameServidor(self, servidor_id):
        try:
            query = f"SELECT nombre FROM servidores WHERE id = '{servidor_id}' AND activo = 1;"
            return fetch_all(query)
        except mysql.connector.Error as e:
            print(f"ERROR get_canales: {e.args}")
            return f'Error MySQL al traer los canales: {str(e)}'
        except Exception as e:
            print(f"ERROR get_canales: {e.args}")
            return f'Se produjo un error al traer los canales: {str(e)}'


    def update_canal(self, nombre, canal_id):
        try:
            query = "UPDATE canales SET nombre = %s, activo = 1 WHERE id = %s;"
            value = (nombre, canal_id)
            commint_db(query, value)
            return True
        except mysql.connector.Error as e:
            print(f"ERROR update_canal: {e.args}")
            return f'Error MySQL al actualizar el canal: {str(e)}'
        except Exception as e:
            print(f"ERROR update_canal: {e.args}")
            return f'Se produjo un error al actualizar el canal: {str(e)}'

    def delete_canal(self, canal_id):
        try:
            query = f"DELETE FROM canales WHERE id = '{canal_id}';"
            execute_db(query)
            return True
        except mysql.connector.Error as e:
            print(F"ERROR delete_canal {e.args}")
            return f'Error MySQL al borrar el canal: {str(e)}'
        except Exception as e:
            print(F"ERROR delete_canal {e.args}")
            return f'Se produjo un error al borrar el canal: {str(e)}'

    def get_canal(self, canal_name, servidor_id):
        try:
            query = f"SELECT * FROM canales WHERE nombre = '{canal_name}' and servidor_id = '{servidor_id}';"
            return fetch_one(query)
        except mysql.connector.Error as e:
            print(F"ERROR delete_canal {e.args}")
            return f'Error MySQL al borrar el canal: {str(e)}'
        except Exception as e:
            print(F"ERROR delete_canal {e.args}")
            return f'Se produjo un error al borrar el canal: {str(e)}'
