import mysql.connector
import config

connection = None


def get_cursor(autocommit=True):
    global connection
    connection = mysql.connector.connect(user=config.user,
                                         password=config.password,
                                         host=config.host,
                                         port=config.port,
                                         database=config.name,
                                         autocommit=autocommit)
    return connection.cursor(dictionary=True)

def get_connection_and_cursor():
    global connection
    connection = mysql.connector.connect(user=config.user,
                                         password=config.password,
                                         host=config.host,
                                         port=config.port,
                                         database=config.name,
                                         autocommit=False)
    return connection, connection.cursor(dictionary=True)


def query(stmt, params=None):
    cursor = get_cursor()
    cursor.execute(stmt, params)
    return cursor.fetchall()

# stmts: [(stmt, params), (stmt, params), (stmt, params)]
def transaction(stmts):
    cursor = get_cursor(autocommit=False)
    try:
        for stmt, params in stmts:
            cursor.execute(stmt, params)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(e)
    finally:
        cursor.close()
        connection.close()
