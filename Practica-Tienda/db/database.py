import psycopg


def client():
    try:
        conexion = {
            "dbname": "tienda",
            "user": "user_postgres",
            "password": "pass_postgres",
            "host": "localhost",
            "port": "5432"
        }

        conn = psycopg.connect(**conexion)
        return conn

    except psycopg.Error as e:
        # Si hay un error en la conexión, manejarlo específicamente
        raise ConnectionError(f"Error de conexión a la base de datos: {e}")

    except Exception as e:
        # Otros errores no relacionados con la conexión
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")
