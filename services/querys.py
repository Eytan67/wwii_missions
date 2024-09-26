create_coordinates_query = """
    CREATE TABLE IF NOT EXISTS coordinates (
        id SERIAL PRIMARY KEY,
        latitude DECIMAL(9, 6),
        longitude DECIMAL(9, 6)
    );
"""
create_location_query = """
    CREATE TABLE IF NOT EXISTS location (
        id SERIAL PRIMARY KEY,
        country VARCHAR(50),
        city VARCHAR(50)
    );
"""
create_target_query = """
     CREATE TABLE target_details (
        target_id SERIAL PRIMARY KEY,
        target_type VARCHAR(100),
        target_industry VARCHAR(255),
        target_priority VARCHAR(5),
        location_id INTEGER REFERENCES location(id),
        coordinates_id INTEGER REFERENCES coordinates(id) 
        );
"""
get_source_table = """
    SELECT * FROM mission;
"""
