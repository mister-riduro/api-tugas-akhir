import os
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('DB_USERNAME'))

conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))

cur = conn.cursor()

# User
cur.execute(""" DROP TABLE IF EXISTS users; """)
cur.execute("""
    CREATE TABLE users (user_id serial PRIMARY KEY,
                        name varchar (150) NOT NULL,
                        email varchar (100) NOT NULL,
                        password varchar (100) NOT NULL,
                        province varchar (100) NOT NULL,
                        city varchar (100) NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Hotel
cur.execute(""" DROP TABLE IF EXISTS hotels; """)
cur.execute("""
    CREATE TABLE hotels (hotel_id serial PRIMARY KEY,
                        hotel_image text NOT NULL,
                        hotel_name varchar (150) NOT NULL,
                        property_type varchar (100) NOT NULL,
                        hotel_city varchar (100) NOT NULL,
                        hotel_address text NOT NULL,
                        hotel_rating decimal NOT NULL,
                        min_price integer NOT NULL,
                        max_price integer NOT NULL,
                        lattitude decimal NOT NULL,
                        longitude decimal NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Provinsi
cur.execute(""" DROP TABLE IF EXISTS provinces; """)
cur.execute("""
    CREATE TABLE provinces (province_id serial PRIMARY KEY,
                        province_image text NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Wisata
cur.execute("""
    CREATE TABLE tourisms (tourism_id serial PRIMARY KEY,
                            tourism_name text NOT NULL,
                            tourism_address text NOT NULL,
                            tourism_type varchar (100) NOT NULL,
                            tourism_city varchar (100) NOT NULL,
                            tourism_province varchar (100) NOT NULL,
                            province_id integer,
                            operational_hour varchar (100) NOT NULL,
                            tourism_description text NOT NULL,
                            entry_price integer NOT NULL,
                            route text NOT NULL,
                            traveling_time varchar (100) NOT NULL,
                            road_condition varchar (100) NOT NULL,
                            max_price integer NOT NULL,
                            tourism_rating decimal NOT NULL,
                            lattitude decimal NOT NULL,
                            longitude decimal NOT NULL,
                            created_at date DEFAULT CURRENT_TIMESTAMP,
                            updated_at date DEFAULT CURRENT_TIMESTAMP,
                            
                            CONSTRAINT fk_prrovince
                                FOREIGN KEY(province_id)
                                    REFERENCES provinces(province_id));
            """)

# Nearest Event
cur.execute(""" DROP TABLE IF EXISTS nearest_event; """)
cur.execute("""
    CREATE TABLE nearest_event (nearest_event_id serial PRIMARY KEY,
                        event_image text NOT NULL,
                        event_name varchar (150) NOT NULL,
                        event_date varchar (100) NOT NULL,
                        event_location text NOT NULL,
                        event_description text NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Tourism Facilities
cur.execute(""" DROP TABLE IF EXISTS tfacilities; """)
cur.execute("""
    CREATE TABLE tfacilities (tfacilities_id serial PRIMARY KEY,
                        facilities_name varchar (150) NOT NULL,
                        facilities_image text NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Pivot Table Tourism Facilities
cur.execute("""
    CREATE TABLE tourism_facilities (
                        tfacilities_id integer REFERENCES tfacilities(tfacilities_id) ON UPDATE CASCADE ON DELETE CASCADE,
                        tourism_id integer REFERENCES tourisms(tourism_id),
                        CONSTRAINT tourism_facilities_pkey
                            PRIMARY KEY (tfacilities_id, tourism_id));
            """)

# Hotel Facilities
cur.execute(""" DROP TABLE IF EXISTS hfacilities; """)
cur.execute("""
    CREATE TABLE hfacilities (hfacilities_id serial PRIMARY KEY,
                        facilities_name varchar (150) NOT NULL,
                        facilities_image text NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Pivot Table Hotel Facilities
cur.execute("""
    CREATE TABLE hotel_facilities (
                        hfacilities_id integer REFERENCES hfacilities(hfacilities_id) ON UPDATE CASCADE ON DELETE CASCADE,
                        hotel_id integer REFERENCES hotels(hotel_id),
                        CONSTRAINT hotel_facilities_pkey
                            PRIMARY KEY (hfacilities_id, hotel_id));
            """)

conn.commit()

cur.close()
conn.close()