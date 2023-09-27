from database.conexion_db import fetch_one, commint_db
from werkzeug.security import generate_password_hash
import mysql.connector


class User:
    def __init__(self):
        self

    def user_exist(self, email):
        try:
            query = (
                f"SELECT id as idLogin,nombre,apellido,email,sexo,create_at,fecha_nacimiento,pais_id,password FROM usuarios WHERE email = '{email}'")
            return fetch_one(query)
        except mysql.connector.Error as e:
            print(f"ERROR user_exist: {e.args}")
            return f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(f"ERROR user_exist: {e.args}")
            return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'

    def create_user(self, nombre, apellido, email, password, sexo, pais, avatar, fecha_nacimiento):
        try:
            avatar_bytes = None
            if (avatar != None):
                avatar_bytes = self.img_bytes(avatar)
            password_encriptada = generate_password_hash(
                password, method='sha256')
            query_db = "INSERT INTO usuarios (nombre, apellido, email, password, sexo, pais_id, avatar,fecha_nacimiento) "
            query_db += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (nombre, apellido, email, password_encriptada,
                      sexo, pais, avatar_bytes, fecha_nacimiento)
            commint_db(query_db, values)
        except mysql.connector.Error as e:
            print(f"ERROR create_user: {e.args}")
            return f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(f"ERROR create_user: {e.args}")
            return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'

    def update_profile_with_password(self, nombre, apellido, email, password, sexo, pais_id, avatar, fecha_nacimiento, id):
        try:
            avatar_bytes = None
            if (avatar.filename != ''):
                avatar_bytes = avatar.read()

            nueva_password = generate_password_hash(password, method='sha256')
            query = "UPDATE usuarios "
            query += "SET nombre = %s, apellido = %s, email = %s, password = %s, sexo = %s, pais_id = %s, "
            if (avatar.filename != ''):
                query += "avatar=%s, "
            query += "fecha_nacimiento=%s"
            query += "WHERE id = %s"

            values = ()
            if (avatar.filename != ''):
                values = (nombre, apellido, email, nueva_password, sexo,
                          pais_id, avatar_bytes, fecha_nacimiento, id)
            else:
                values = (nombre, apellido, email, nueva_password, sexo,
                          pais_id, fecha_nacimiento, id)

            commint_db(query, values)
            return True
        except mysql.connector.Error as e:
            print(f"ERROR update_profile_with_password: {e.args}")
            return f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(f"ERROR update_profile_with_password: {e.args}")
            return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'

    def update_profile_out_password(self, nombre, apellido, email, sexo, pais_id, avatar, fecha_nacimiento, id):
        try:
            img = None
            if avatar.filename != '':
                img = avatar.read()

            query_db = "UPDATE usuarios "
            query_db += "SET nombre = %s, apellido = %s, email = %s, sexo = %s, pais_id = %s, "
            if (avatar.filename != ''):
                query_db += "avatar=%s, "
            query_db += "fecha_nacimiento=%s "
            query_db += "WHERE id = %s"

            values_db = ()

            if (avatar.filename != ''):
                values_db = (nombre, apellido, email, sexo,
                             pais_id, img, fecha_nacimiento, id)
            else:
                values_db = (nombre, apellido, email, sexo,
                             pais_id, fecha_nacimiento, id)

            commint_db(query_db, values_db)
            return True
        except mysql.connector.Error as e:
            print(f"ERROR update_profile_out_password: {e.args}")
            return f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(f"ERROR update_profile_out_password: {e.args}")
            return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'

    def data_login_sesion(self, session):
        infor_login = {
            "conectado": session['conectado'],
            "idLogin": session['id'],
            "nombre": session['nombre'],
            "apellido": session['apellido'],
            "emailLogin": session['email'],
            "sexo": session['sexo'],
            "pais": session['pais'],
            "avatar": session['avatar'],
            "create_at": session['create_at'],
            "fecha_nacimiento": session['fecha_nacimiento']
        }
        return infor_login

    def data_perfil_usuario(self, session):
        try:
            id_user = session['id']
            query = ("SELECT * FROM usuarios WHERE id='%s'" % (id_user,))
            return fetch_one(query)
        except mysql.connector.Error as e:
            print(f"ERROR data_perfil_usuario: {e.args}")
            return f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(f"ERROR data_perfil_usuario: {e.args}")
            return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'

    def img_bytes(self, avatar):
        avatar_bytes = None
        if (avatar != b'' and not isinstance(avatar, bytes)):
            with open(avatar, 'rb') as file:
                avatar_bytes = file.read()
        return avatar_bytes

    def get_imagen_perfil(self, id_usuario):
        try:
            query = ("SELECT avatar FROM usuarios WHERE id='%s'" %
                     (id_usuario,))
            return fetch_one(query)
        except mysql.connector.Error as e:
            print(f"ERROR data_perfil_usuario: {e.args}")
            return f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(f"ERROR data_perfil_usuario: {e.args}")
            return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'
