
def migrate_data(conn):
    try:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT 
                    mission_id, target_country, target_city, 
                    target_latitude, target_longitude, 
                    target_type, target_industry, target_priority 
                FROM mission;
            """)
            rows = cur.fetchall()
            for row in rows:
                row_dict = {
                    'mission_id': row[0],
                    'target_country': row[1],
                    'target_city': row[2],
                    'target_latitude': row[3],
                    'target_longitude': row[4],
                    'target_type': row[5],
                    'target_industry': row[6],
                    'target_priority': row[7]
                }

                target_country = row_dict['target_country']
                target_city = row_dict['target_city']
                location_id = insert_or_find_location(cur, target_country, target_city)



                target_latitude = row_dict['target_latitude']
                target_longitude = row_dict['target_longitude']
                coordinates_id = insert_or_find_coordinates(cur, target_latitude, target_longitude)



                target_type = row_dict['target_type']
                target_industry = row_dict['target_industry']
                target_priority = row_dict['target_priority']


                new_target_id = insert_or_find_target(cur, target_type, target_industry, target_priority, location_id, coordinates_id)

                cur.execute("""
                        UPDATE mission 
                        SET target_id = %s 
                        WHERE mission_id = %s;
                    """, (new_target_id, row_dict['mission_id']))

                conn.commit()
            cur.execute("""
                ALTER TABLE mission
                    DROP COLUMN target_country,
                    DROP COLUMN target_city,
                    DROP COLUMN target_latitude,
                    DROP COLUMN target_longitude, 
                    DROP COLUMN target_type,
                    DROP COLUMN target_industry,
                    DROP COLUMN target_priority
            """)
            conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")


def insert_or_find_location(cur, target_country, target_city):
    if target_country is None and target_city is None:
        cur.execute("""
            SELECT id FROM location 
            WHERE country IS NULL AND city IS NULL;
        """)
    elif target_country is None:
        cur.execute("""
            SELECT id FROM location 
            WHERE country IS NULL AND city = %s;
        """, (target_city,))
    elif target_city is None:
        cur.execute("""
            SELECT id FROM location 
            WHERE country = %s AND city IS NULL;
        """, (target_country,))
    else:
        cur.execute("""
            SELECT id FROM location 
            WHERE country = %s AND city = %s;
        """, (target_country, target_city))

    location_row = cur.fetchone()

    if location_row:
        location_id = location_row[0]
    else:
        cur.execute("""
                          INSERT INTO location (country, city) 
                          VALUES (%s, %s) 
                          RETURNING id;
                      """, (target_country, target_city))
        location_id = cur.fetchone()[0]

    return location_id

def insert_or_find_coordinates(cur, target_latitude, target_longitude):
    if target_latitude is None and target_longitude is None:
        cur.execute("""
            SELECT id FROM coordinates 
            WHERE latitude IS NULL AND longitude IS NULL;
        """)
    elif target_latitude is None:
        cur.execute("""
            SELECT id FROM coordinates 
            WHERE latitude IS NULL AND longitude = %s;
        """, (target_longitude,))
    elif target_longitude is None:
        cur.execute("""
            SELECT id FROM coordinates 
            WHERE latitude = %s AND longitude IS NULL;
        """, (target_latitude,))
    else:
        cur.execute("""
            SELECT id FROM coordinates 
            WHERE latitude = %s AND longitude = %s;
        """, (target_latitude, target_longitude))

    coordinates_row = cur.fetchone()

    if coordinates_row:
        coordinates_id = coordinates_row[0]
    else:
        cur.execute("""
                          INSERT INTO coordinates (latitude, longitude) 
                          VALUES (%s, %s) 
                          RETURNING id;
                      """, (target_latitude, target_longitude))
        coordinates_id = cur.fetchone()[0]

    return coordinates_id

def insert_or_find_target(cur, target_type, target_industry, target_priority, location_id, coordinates_id):
    cur.execute(""" 
        SELECT target_id FROM target_details 
        WHERE (target_type = %s OR (target_type IS NULL AND %s IS NULL)) 
          AND (target_industry = %s OR (target_industry IS NULL AND %s IS NULL)) 
          AND (target_priority = %s OR (target_priority IS NULL AND %s IS NULL)) 
          AND location_id = %s 
          AND coordinates_id = %s;
    """, (
        target_type, target_type,
        target_industry, target_industry,
        target_priority, target_priority,
        location_id,
        coordinates_id
    ))
    target_row = cur.fetchone()

    if target_row:
        new_target_id = target_row[0]
    else:
        cur.execute("""
                          INSERT INTO target_details (target_type, target_industry, target_priority, location_id, coordinates_id) 
                          VALUES (%s, %s, %s, %s, %s)
                          RETURNING target_id;
                      """, (
            target_type, target_industry,
            target_priority, location_id, coordinates_id
        ))
        new_target_id = cur.fetchone()[0]

    return new_target_id
