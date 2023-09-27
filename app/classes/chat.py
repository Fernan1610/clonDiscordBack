from database.conexion_db import fetch_all, commint_db, execute_db
import mysql.connector
from flask import Flask, render_template, Markup


class Chat:
    def __init__(self):
        self

    def insert_chat(self, mensaje, canal_id, usuario_id):
        try:
            query = "INSERT INTO chats(mensaje, canal_id, usuario_id) VALUES (%s, %s, %s)"
            value = (mensaje, canal_id, usuario_id)
            resultado_insert = commint_db(query, value)
            if resultado_insert == 1:
                mensajes = lista_mensajes_chat(canal_id)
                return mensajes
            else:
                return []
        except mysql.connector.Error as e:
            print(F"ERROR procesar_form_chat mysql {e.args}")
            return f'Error MySQL al insertar el mensaje: {str(e)}'
        except Exception as e:
            print(F"ERROR procesar_form_chat {e.args}")
            return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'

    def update_mensaje(self, mensaje, id, usuario_id, canal_id):
        try:
            query = "UPDATE chats SET mensaje= %s"
            query += " WHERE id = %s"
            query += " AND usuario_id = %s"
            value = (mensaje, id, usuario_id)
            resultado_insert = commint_db(query, value)
            if resultado_insert == 1:
                mensajes = lista_mensajes_chat(canal_id)
                return mensajes
            else:
                return []
        except mysql.connector.Error as e:
            print(F"ERROR update_chat {e.args}")
            return f'Error MySQL al actualizar el mensaje: {str(e)}'
        except Exception as e:
            print(F"ERROR update_chat {e.args}")
            return f'Se produjo un error al actualizar registrar el mensaje: {str(e)}'

    def delete_mensaje(self, id, canal_id):
        try:
            query = f"DELETE FROM chats WHERE id = '{id}';"
            resp = execute_db(query)
            if (resp == True):
                mensajes = lista_mensajes_chat(canal_id)
                return mensajes
            else:
                return []
        except mysql.connector.Error as e:
            print(F"ERROR update_chat {e.args}")
            return f'Error MySQL al actualizar el mensaje: {str(e)}'
        except Exception as e:
            print(F"ERROR update_chat {e.args}")
            return f'Se produjo un error al eliminar el mensaje: {str(e)}'

    def delete_msg_by_channel_id(self, channel_id):
        try:
            query = f"DELETE FROM chats WHERE canal_id = '{channel_id}';"
            resp = execute_db(query)
            return resp
        except mysql.connector.Error as e:
            print(F"ERROR update_chat {e.args}")
            return f'Error MySQL al actualizar el mensaje: {str(e)}'
        except Exception as e:
            print(F"ERROR deelte_msg_by_channel_id {e.args}")
            return f'Se produjo un error al eliminar los mensaje: {str(e)}'


def lista_mensajes_chat(canal_id):
    try:
        query = "SELECT id, mensaje, canal_id, usuario_id, CAST(create_at AS CHAR) AS fecha_formateada "
        query += "FROM chats "
        query += f"WHERE canal_id = '{canal_id}' "
        query += "ORDER BY create_at ASC;"
        lista_chat = fetch_all(query)
        if len(lista_chat) > 0:
            return lista_chat
        else:
            return []
    except mysql.connector.Error as e:
        print(f"ERROR lista_mensajes_chat mysql: {e}")
        return f'Error MySQL al insertar el mensaje: {str(e)}'
    except Exception as e:
        print(f"ERROR lista_mensajes_chat: {e}")
        return f'Se produjo un error al insertar registrar el mensaje: {str(e)}'
