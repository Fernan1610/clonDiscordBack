from database.conexion_db import fetch_all, commint_db, execute_db
import mysql.connector


class UsuarioServidor:
    def __init__(self, id_usuario):
        self.id = id_usuario

    def insert_usuario_servidor(self, usuario_id, servidor_id, rol):
        try:
            query = "INSERT INTO usuarios_servidores (usuario_id,servidor_id, rol) VALUES (%s,%s,%s)"
            value = (usuario_id, servidor_id, rol)
            return commint_db(query, value)
        except mysql.connector.Error as e:
            print(f"ERROR insert_usuario_servidor: {e}")
            return f'Error MySQL al insertar en la tabla usuario_seridor: {str(e)}'
        except Exception as e:
            print(f"ERROR insert_usuario_servidor: {e}")
            return f'Se produjo un error al insertar en la tabla usuario_seridor: {str(e)}'

    def get_usuario_servidor(self, usuario_id):
        try:
            query = "SELECT s.* FROM servidores s "
            query += "INNER JOIN usuarios_servidores us ON s.id = us.servidor_id "
            query += f"WHERE us.usuario_id = '{usuario_id}' AND s.activo = 1;"
            return fetch_all(query)
        except mysql.connector.Error as e:
            print(f"ERROR get_usuario_servidor: {e}")
            return f'Error MySQL al traer de la tabla usuario_servidor: {str(e)}'
        except Exception as e:
            print(f"ERROR get_usuario_servidor: {e}")
            return f'Se produjo un error al traer de la tabla usuario_servidor: {str(e)}'

    def update_rol_usuario_servidor(self, rol):
        try:
            query = f"UPDATE usuarios_servidores SET rol = {rol};"
            execute_db(query)
            return True
        except mysql.connector.Error as e:
            print(f"ERROR update_usuario_servidor: {e.args}")
            return f'Error MySQL al actualizar el usuario_servidor: {str(e)}'
        except Exception as e:
            print(f"ERROR update_usuario_servidor: {e.args}")
            return f'Se produjo un error al actualizar el usuario_servidor: {str(e)}'

    def delete_usuario_servidor(self, id):
        try:
            query = f"DELETE FROM usuarios_servidores WHERE id = '{id}';"
            execute_db(query)
            return True
        except mysql.connector.Error as e:
            print(F"ERROR delete_usuario_servidor {e.args}")
            return f'Error MySQL al borrar el usuario_servidor: {str(e)}'
        except Exception as e:
            print(F"ERROR delete_usuario_servidor {e.args}")
            return f'Se produjo un error al borrar el v: {str(e)}'

    def get_list_serv_dis_user(self, user_id):
        try:
            query = 'SELECT s.*, COALESCE(user_count, 0) AS numero_usuarios '
            query += 'FROM servidores s '
            query += 'LEFT JOIN ('
            query += 'SELECT servidor_id, COUNT(usuario_id) AS user_count '
            query += 'FROM usuarios_servidores '
            query += 'GROUP BY servidor_id '
            query += ') counts ON s.id = counts.servidor_id '
            query += 'WHERE s.activo = 1 AND s.id NOT IN ('
            query += f"SELECT servidor_id FROM usuarios_servidores WHERE usuario_id = '{user_id}');"
            return fetch_all(query)
        except mysql.connector.Error as e:
            print(F"ERROR get_list_serv_dis_user {e.args}")
            return f'Error MySQL al traer el usuario_servidor: {str(e)}'
        except Exception as e:
            print(F"ERROR get_list_serv_dis_user {e.args}")
            return f'Se produjo un error al trer el v: {str(e)}'

    def delete_usuario_servidor_by_server_id(self, id):
        try:
            query = f"DELETE FROM usuarios_servidores WHERE servidor_id = '{id}';"
            execute_db(query)
            return True
        except mysql.connector.Error as e:
            print(F"ERROR delete_usuario_servidor {e.args}")
            return f'Error MySQL al borrar el usuario_servidor: {str(e)}'
        except Exception as e:
            print(F"ERROR delete_usuario_servidor {e.args}")
            return f'Se produjo un error al borrar el v: {str(e)}'
