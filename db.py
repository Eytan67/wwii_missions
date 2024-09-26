import psycopg2
from psycopg2 import pool
from services.normal_service2 import migrate_data

connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )

def get_db_connection():
    if connection_pool:
        conn = connection_pool.getconn()
        print(True)
        return conn

def release_db_connection(conn):
    connection_pool.putconn(conn)
    print(True)

conn = get_db_connection()
migrate_data(conn)





# cur.execute(create_location_query)
# cur.execute(create_coordinates_query)
# cur.execute(create_target_query)

# connect.commit()
# al_data = cur.fetchall()
release_db_connection(conn)