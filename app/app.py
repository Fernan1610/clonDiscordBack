from flask import Flask, Response, jsonify, render_template, request, redirect, url_for, session
import re
from werkzeug.security import check_password_hash
from flask_socketio import SocketIO, emit
from classes.user import User
from classes.chat import Chat, lista_mensajes_chat
from classes.country import Country
from classes.canales import Canal
from classes.servidores import Servidor
from classes.usuario_servidor import UsuarioServidor
from middleware.errorHandler import CustomException
import json
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
app.secret_key = '97110c78ae51a45af397be6534caef90ebb9b1dcb3380af008f90b23a5d1616bf19bc29098105da20fe'
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})
CORS(app, resources={r"/socket.io/*": {"origins": "http://127.0.0.1:5100"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)


@app.route("/socket.io/")
def socket_io():
    return "Hello, world!"

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ZONA USUARIO


"""LOGIN"""


@app.route('/login_user', methods=['POST'])
def login_user():
    try:
        if request.method == 'POST':
            data = request.get_json()
            email = data.get('email', '')
            password = data.get('password', '')
            account = User.user_exist("", email)
            if account and check_password_hash(account['password'], password):
                pais = Country.get_pais("", account['pais_id'])
                session['conectado'] = True
                session['id'] = account['idLogin']
                session['nombre'] = account['nombre']
                session['apellido'] = account['apellido']
                session['email'] = account['email']
                session['sexo'] = account['sexo']
                session['pais'] = pais['name_country']
                session['avatar'] = None
                session['create_at'] = account['create_at']
                session['fecha_nacimiento'] = account['fecha_nacimiento']
                session.permanent = True
                data_login = User.data_login_sesion("", session)
                return jsonify(data_login)
    except Exception as e:
        error = CustomException(500, "Error al intentar loguearse", e.args)
        return error.get_response()


"""REGISTRO USUARIO"""


@app.route('/registro-usuario', methods=['GET', 'POST'])
def register_user():
    msg = 'El metodo no es un post.'
    try:
        if request.method == 'POST':
            data = request.get_json()
            nombre = data.get('nombre', '')
            apellido = data.get('apellido', '')
            email = data.get('email', '')
            password = data.get('password', '')
            repite_password = data.get('repite_password', '')
            sexo = data.get('sexo', '')
            fecha_nacimiento = data.get('fecha_nacimiento', '')
            pais = data.get('pais_id', '')
            account = User.user_exist("", email)
            if account:
                msg = 'Ya existe el Email!'
            elif password != repite_password:
                msg = 'Disculpa, las clave no coinciden!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Disculpa, formato de Email incorrecto!'
            elif not email or not password or not password or not repite_password:
                msg = 'El formulario no debe estar vacio!'
            else:
                User.create_user("", nombre, apellido, email,
                                 password, sexo, pais, None, fecha_nacimiento)
                msg = 'Cuenta creada correctamente!'
            return msg
        error_post = CustomException(400, msg, msg)
        return error_post.get_response()
    except Exception as e:
        error = CustomException(500, "Error al intentar registrarse", e.args)
        return error.get_response()


"""ACTUALIZAR PERFIL"""


@app.route('/actualizar-mi-perfil', methods=['POST'])
def actualizar_perfil():
    try:
        id = request.form['idLogin']
        if id:
            if request.method == 'POST':
                nombre = request.form['nombre']
                apellido = request.form['apellido']
                email = request.form['email']
                sexo = request.form['sexo']
                pais = str(request.form['pais_id'])
                imagen = request.files['imagen']
                fecha_nacimiento = request.form['fecha_nacimiento']
                update = False
                if (request.form['password']):
                    password = request.form['password']
                    repite_password = request.form['repite_password']
                    if password != repite_password:
                        error = CustomException(
                            400, "Las contraseñas no coinciden", "Las contraseñas no coinciden")
                        return error.get_response()
                    else:
                        update = User.update_profile_with_password(
                            "", nombre, apellido, email, password, sexo, pais, imagen, fecha_nacimiento, id)
                else:
                    update = User.update_profile_out_password("",
                                                              nombre, apellido, email, sexo, pais, imagen, fecha_nacimiento, id)
                if (update):
                    update_user = User.user_exist("", email)
                    return jsonify(update_user)
            error = CustomException(400, "No es un post", "No es un post")
            return error.get_response()
    except Exception as e:
        error = CustomException(500, "Error al intentar actualizar", e.args)
        return error.get_response()


@app.route('/get-foto-profile', methods=['POST'])
def get_foto_profile():
    try:
        data = request.get_json()
        if data:
            id = data.get('idLogin', '')
            avatar = User.get_imagen_perfil("", id)
            content_type = 'image/jpeg'
            return Response(avatar['avatar'], mimetype=content_type)
    except Exception as e:
        error = CustomException(500, "Error al intentar guardar", e.args)
        return error.get_response()


"""EDITAR PERFIL"""


@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    try:
        if 'conectado' in session:
            data_user = User.data_perfil_usuario("", session)
            pais = Country.get_pais("", data_user['pais_id'])
            session['pais'] = pais['name_country']
            return render_template('public/dashboard/home.html')
    except Exception as e:
        error = CustomException(500, "Error al intentar guardar", e.args)
        return error.get_response()


"""CERRAR SESSION"""


@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.pop('conectado', False)
        session.pop('id', None)
        session.pop('email', None)
        return "True"
    except Exception as e:
        error = CustomException(500, "Error al cerrar sesion", e.args)
        return error.get_response()


@app.errorhandler(404)
def not_found(error):
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template('public/modulo_login/Login_base.html')

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ZONA CHAT


"""TRAE LOS MENSAJES"""


@app.route('/get_messages/<uuid:channel_id>')
def get_messages(channel_id):
    try:
        if channel_id:
            messages = lista_mensajes_chat(channel_id)
            return jsonify(messages)
    except Exception as e:
        error = CustomException(500, "Error al traer los mensajes", e.args)
        return error.get_response()


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ZONA CANALES


"""TRAE LOS CANALES"""


@app.route('/get_channels/<uuid:server_id>', methods=['GET'])
def get_channels(server_id):
    try:
        if server_id:
            channels = Canal.get_canales("", server_id)
            return jsonify(channels)
    except Exception as e:
        error = CustomException(500, "Error al traer los canales", e.args)
        return error.get_response()


@app.route('/get_serverName/<uuid:server_id>', methods=['GET'])
def get_server_name(server_id):
    try:
        if server_id:
            channels = Canal.get_nameServidor("", server_id)
            return jsonify(channels)
    except Exception as e:
        error = CustomException(
            500, "Error al traer el nombre del servidor", e.args)
        return error.get_response()


@app.route('/delete_channel', methods=['POST'])
def delete_channel():
    try:
        data = request.get_json()
        if data:
            channel_id = data.get('channel_id', '')
            server_id = data.get('server_id', '')
            chat_delete = Chat.delete_msg_by_channel_id("", channel_id)
            if (chat_delete):
                canal_delete = Canal.delete_canal("", channel_id)
                if (canal_delete):
                    canales = Canal.get_canales("", server_id)
                    return jsonify(canales)
    except Exception as e:
        error = CustomException(500, "Error al traer los canales", e.args)
        return error.get_response()


"""CREA UN CANAL"""


@app.route("/createChanel", methods=['POST'])
def create_chanel():
    try:
        data = request.get_json()
        if request.method == 'POST' and data:
            nombre_canal = data.get('nombre', '')
            id_servidor = data.get('serverId', '')
            creado = Canal.crear_canal("", nombre_canal, id_servidor, True)
            if (creado):
                channels = Canal.get_canales("", id_servidor)
                return jsonify(channels)
    except Exception as e:
        error = CustomException(500, "Error al crear el canal", e.args)
        return error.get_response()


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ZONA PAISES
"""TRAE TODOS LOS PAISES"""


@app.route('/getListaPaises')
def get_lista_paises():
    try:
        lista_paises = Country.lista_paises("")
        return jsonify(lista_paises)
    except Exception as e:
        error = CustomException(500, "Error al traer los paises", e.args)
        return error.get_response()


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ZONA SERVIDORES
"""CREA SERVIDOR"""


@app.route("/createServer", methods=['POST'])
def create_server():
    try:
        if request.method == 'POST':
            nombre_servidor = request.form.get('nombre', '')
            id_login = request.form.get('idLogin', '')
            # imagen = request.form.get('', None)
            Servidor.crear_servidor("", nombre_servidor, None, True)
            servidor = Servidor.get_servidor_by_nombre("", nombre_servidor)
            if (servidor != None):
                usuario_serv = UsuarioServidor.insert_usuario_servidor(
                    "", id_login, servidor['id'], "administrador")
                if (usuario_serv == 1):
                    servers = UsuarioServidor.get_usuario_servidor(
                        "", id_login)
                    if (servers):
                        return jsonify(servers)
    except Exception as e:
        error = CustomException(500, "Error al crear el servidor", e.args)
        return error.get_response()


"""TRAE LOS SERVIDORES POR USUARIO"""


@app.route('/getServidoresByUsuario/<uuid:user_id>', methods=['GET'])
def get_servidores_by_usuario(user_id):
    try:
        if user_id:
            servers = UsuarioServidor.get_usuario_servidor("", user_id)
            return jsonify(servers)
    except Exception as e:
        error = CustomException(500, "Error al traer los servidores", e.args)
        return error.get_response()


"""TRAE LOS SERVIDORES QUE NO LE PERTENECEN A UN USUARIO"""


@app.route('/getListServers/<uuid:user_id>', methods=['GET'])
def get_list_servers(user_id):
    try:
        if user_id:
            servers = UsuarioServidor.get_list_serv_dis_user("", user_id)
            return jsonify(servers)
    except Exception as e:
        error = CustomException(500, "Error al traer los servidores", e.args)
        return error.get_response()


"""UNIRSE A SERVIDOR"""


@app.route('/unirseServidor', methods=['POST'])
def unirse_servidor():
    try:
        data = request.get_json()
        if data:
            servidor_id = data.get('serverId', '')
            id_login = data.get('idLogin', '')
            usuario_serv = UsuarioServidor.insert_usuario_servidor(
                "", id_login, servidor_id, "invitado")
            if (usuario_serv == 1):
                servers = UsuarioServidor.get_usuario_servidor(
                    "", id_login)
                return jsonify(servers)
    except Exception as e:
        error = CustomException(
            500, "Error al traer de unirse al servidor", e.args)
        return error.get_response()


"""ELIMINAR A SERVIDOR"""


@app.route('/eliminarServidor', methods=['POST'])
def eliminar_servidor():
    try:
        data = request.get_json()
        if data:
            servidor_id = data.get('server_id', '')
            id_login = data.get('idLogin', '')
            canales_list = Canal.get_canales("", servidor_id)
            for canal in canales_list:
                canal_id = canal['id']
                delete_canal = Chat.delete_msg_by_channel_id("", canal_id)
                if (delete_canal):
                    Canal.delete_canal("", canal_id)
            usuario_servidores = UsuarioServidor.delete_usuario_servidor_by_server_id(
                "", servidor_id)
            if (usuario_servidores):
                delete_sev = Servidor.delete_servidor("", servidor_id)
                if (delete_sev):
                    servers = UsuarioServidor.get_usuario_servidor(
                        "", id_login)
                    return jsonify(servers)
    except Exception as e:
        error = CustomException(
            500, "Error al traer de unirse al servidor", e.args)
        return error.get_response()


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# ZONA WEB SOCKET

"""CONECTA EL WEB SOCKET"""


@socketio.on('connect')
def handle_connect():
    # if 'user_id' in session:
    #     user_id = session['user_id']
    #     join_room(user_id)
    #     emit('message', {'text': f'Usuario {user_id} se ha conectado.'}, room=user_id)
    print('Cliente conectado')


@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')
    session['conectado'] = False
    session['id'] = ""
    session['nombre'] = ""
    session['apellido'] = ""
    session['email'] = ""
    session['sexo'] = ""
    session['pais'] = ""
    session['avatar'] = None
    session['create_at'] = ""
    session['fecha_nacimiento'] = ""
    User.data_login_sesion("", session)


"""ESCUCHA LOS MENSAJES QUE SE ENVIAN Y LOS GUARDA EN LA DB"""


@socketio.on('mensaje_chat')
def recibir_mensaje(data):
    try:
        if data:
            mensaje_chat = data['mensaje']
            canal_id = data['canal_id']
            usuario_id = data['id_user']
            mensaje_insertado = Chat.insert_chat(
                "", mensaje_chat, canal_id, usuario_id)
            cadena_json = json.dumps(mensaje_insertado)
            emit('mensaje_chat', cadena_json, broadcast=True)
    except Exception as e:
        error = CustomException(500, "Error al enviar el mensaje", e.args)
        return error.get_response()


"""ELIMINA UN MENSAJE"""


@socketio.on('delete_mensaje')
def delete_mensaje(data):
    try:
        if data:
            messages = Chat.delete_mensaje(
                "", data['message_id'], data['canal_id'])
            cadena_json = json.dumps(messages)
            emit('delete_mensaje', cadena_json, broadcast=True)
    except Exception as e:
        error = CustomException(500, "Error al eliminar el mensaje", e.args)
        return error.get_response()


"""ACTUALIZA UN MENSAJE"""


@socketio.on('update_mensaje')
def update_message(data):
    try:
        if data:
            user_id = data['id_user']
            mensaje_id = data['mensaje_id']
            nuevo_mensaje = data['mensaje']
            channel_id = data['channel_id']
            messages = Chat.update_mensaje(
                "", nuevo_mensaje, mensaje_id, user_id, channel_id)
            cadena_json = json.dumps(messages)
            emit('update_mensaje', cadena_json, broadcast=True)
    except Exception as e:
        error = CustomException(500, "Error al editar el mensaje", e.args)
        return error.get_response()


"""INICIA EL WEB SOCKET"""
if __name__ == "__main__":
    socketio.run(app, debug=True, port=5100)
