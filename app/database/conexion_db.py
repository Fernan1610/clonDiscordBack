
import mysql.connector

from .dump import insert_countries


def connection_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Fredi001",
            database="clon_discord"
        )
        if mydb:
            return mydb
    except Exception as e:
        raise e.args


def close_conexion(conexion_db, cursor):
    cursor.close()  # cerrrando conexion SQL
    conexion_db.close()  # cerrando conexion de la BD


def get_connection_cursor():
    conexion = connection_db()
    cursor = conexion.cursor(dictionary=True)
    return (conexion, cursor)


def fetch_all(query):
    connection, mycursor = get_connection_cursor()
    mycursor.execute(query)
    fetch = mycursor.fetchall()  # fetchall () Obtener todos los registros
    close_conexion(connection, mycursor)
    return fetch


def fetch_one(query):
    connection, mycursor = get_connection_cursor()
    mycursor.execute(query)
    fetch_one_resp = mycursor.fetchone()  # fetchone () Obtener un registro
    close_conexion(connection, mycursor)
    return fetch_one_resp


def commint_db(query, values):
    connection, mycursor = get_connection_cursor()
    mycursor.execute(query, values)
    connection.commit()  # commit() commit a la base de datos
    resultado_insert = mycursor.rowcount
    close_conexion(connection, mycursor)
    return resultado_insert


def execute_db(query):
    try:
        connection, mycursor = get_connection_cursor()
        mycursor.execute(query)
        connection.commit()
        close_conexion(connection, mycursor)
        return True
    except Exception as e:
        print(f"ERROR execute_db: {e.args}")
        return False


############### TABLAS ###############

def check_table_existence(table_name):
    try:
        query = f"SHOW TABLES LIKE '{table_name}'"
        table_exists = fetch_one(query) is not None
        return table_exists
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def check_and_create_tables():
    try:
        tables = [("paises", countries()),
                  ("usuarios", usuario()),
                  ("servidores", servidor()),
                  ("canales", canal()),
                  ("chats", mensaje()),
                  ("usuarios_servidores", usuario_servidor())
                  ]
        for table, query in tables:
            if check_table_existence(table) is False:
                print(f"Tabla {table} no existe, creando ...")
                execute_db(query)
                if (table == "paises"):
                    print("PAISES")
                    insert_p = insert_countries()
                    execute_db(insert_p)
                print(f"Tabla {table}, creada")
    except Exception as e:
        print(f"ERROR check_and_create_tables: {e.args}")


def countries():
    query = "CREATE TABLE `paises` ("
    query = query + \
        "`id` varchar(40) default (uuid()) not null primary key,"
    query = query + "`iso` varchar(2) NOT NULL,"
    query = query + "`name` varchar(250) NOT NULL,"
    query = query + "`name_country` varchar(250) NOT NULL,"
    query = query + "`iso3` varchar(3) NOT NULL,"
    query = query + "`numcode` varchar(4) NOT NULL,"
    query = query + "`phonecode` int(5) NOT NULL,"
    query = query + "`LifeEx_Male` float NOT NULL,"
    query = query + "`LifeEx_Female` float NOT NULL"
    query = query + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    return query


def usuario():
    query = "CREATE TABLE `usuarios` ("
    query = query + \
        "`id` VARCHAR(40) DEFAULT (uuid()) NOT NULL PRIMARY KEY,"
    query = query + "`nombre` VARCHAR(50) DEFAULT NULL,"
    query = query + "`apellido` VARCHAR(50) DEFAULT NULL,"
    query = query + "`email` VARCHAR(100) DEFAULT NULL,"
    query = query + "`password` text DEFAULT NULL,"
    query = query + "`sexo` VARCHAR(20) DEFAULT NULL,"
    query = query + "`pais_id` VARCHAR(50) DEFAULT NULL,"
    query = query + "`avatar` LONGBLOB DEFAULT NULL,"
    query = query + "`create_at` timestamp NOT NULL DEFAULT current_timestamp(),"
    query = query + "`fecha_nacimiento` VARCHAR(30) DEFAULT NULL,"
    query = query+"CONSTRAINT pais_fk FOREIGN KEY (pais_id)"
    query = query+"REFERENCES paises (id)"
    query = query + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    return query


def servidor():
    query = "CREATE TABLE `servidores` ("
    query = query + \
        "`id` VARCHAR(40) DEFAULT (uuid()) NOT NULL PRIMARY KEY,"
    query = query + "`nombre` VARCHAR(50) DEFAULT NULL,"
    query = query + "`avatar` LONGBLOB DEFAULT NULL,"
    query = query + "`activo` BOOLEAN DEFAULT NULL,"
    query = query + "`create_at` timestamp NOT NULL DEFAULT current_timestamp()"
    query = query + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    return query


def canal():
    query = "CREATE TABLE `canales` ("
    query = query + \
        "`id` VARCHAR(40) DEFAULT (uuid()) NOT NULL PRIMARY KEY,"
    query = query + "`nombre` VARCHAR(50) DEFAULT NULL,"
    query = query + "`servidor_id` VARCHAR(40) NOT NULL,"
    query = query + "`activo` BOOLEAN DEFAULT NULL,"
    query = query + "`create_at` timestamp NOT NULL DEFAULT current_timestamp(), "
    query = query + "CONSTRAINT servidor_fk FOREIGN KEY (servidor_id) "
    query = query + "REFERENCES servidores (id)"
    query = query + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    return query


def mensaje():
    query = "CREATE TABLE `chats` ("
    query = query + \
        "`id` VARCHAR(40) DEFAULT (uuid()) NOT NULL PRIMARY KEY,"
    query = query + "`mensaje` mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,"
    query = query + "`canal_id` VARCHAR(40) NOT NULL,"
    query = query + "`usuario_id` VARCHAR(40) NOT NULL,"
    query = query + "`create_at` timestamp NOT NULL DEFAULT current_timestamp(), "
    query = query + "CONSTRAINT canal_fk FOREIGN KEY (canal_id) "
    query = query + "REFERENCES canales (id),"
    query = query + "CONSTRAINT usuario_fkey FOREIGN KEY (usuario_id) "
    query = query + "REFERENCES usuarios (id)"
    query = query + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    return query


def usuario_servidor():
    query = "CREATE TABLE `usuarios_servidores` ("
    query = query + \
        "`id` VARCHAR(40) DEFAULT (uuid()) NOT NULL PRIMARY KEY,"
    query = query + "`usuario_id` VARCHAR(50) DEFAULT NULL,"
    query = query + "`servidor_id` VARCHAR(40) NOT NULL,"
    query = query + "`rol` VARCHAR(40) DEFAULT NULL,"
    query = query + "`create_at` timestamp NOT NULL DEFAULT current_timestamp(),"
    query = query + "CONSTRAINT servidor_fkey FOREIGN KEY (servidor_id) "
    query = query + "REFERENCES servidores (id),"
    query = query + "CONSTRAINT usuario_fk FOREIGN KEY (usuario_id) "
    query = query + "REFERENCES usuarios (id)"
    query = query + ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    return query


check_and_create_tables()
