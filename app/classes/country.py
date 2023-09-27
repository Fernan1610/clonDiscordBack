from database.conexion_db import fetch_all, fetch_one
import mysql.connector


class Country:
    def __init__(self):
        self

    def lista_paises(self):
        try:
            query = "SELECT * FROM paises"
            return fetch_all(query)
        except mysql.connector.Error as e:
            print(f"ERROR lista_paises: {e.args}")
            return f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(f"ERROR lista_paises: {e.args}")
            return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'

    def get_pais(self, pais_id):
        try:
            query = f"select * from paises where id = '{pais_id}'"
            return fetch_one(query)
        except mysql.connector.Error as e:
            print(f"ERROR lista_paises: {e.args}")
            return f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(f"ERROR lista_paises: {e.args}")
            return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'
