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
cur.execute(""" DROP TABLE IF EXISTS users CASCADE; """)
cur.execute("""
    CREATE TABLE users (user_id SERIAL PRIMARY KEY,
                        name varchar (150) NOT NULL,
                        email varchar (100) NOT NULL,
                        password varchar (100) NOT NULL,
                        province varchar (100) NOT NULL,
                        city varchar (100) NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Hotel
# Change 29/01/2023 --> Delete province_id column and change to province_name
cur.execute(""" DROP TABLE IF EXISTS hotels CASCADE; """)
cur.execute("""
    CREATE TABLE hotels (hotel_id SERIAL PRIMARY KEY,
                        hotel_image text NOT NULL,
                        hotel_name varchar (150) NOT NULL,
                        property_type varchar (100) NOT NULL,
                        hotel_city varchar (100) NOT NULL,
                        province_name varchar (150) NOT NULL,
                        hotel_address text NOT NULL,
                        hotel_rating decimal NOT NULL,
                        min_price integer NOT NULL,
                        max_price integer NOT NULL,
                        latitude decimal NOT NULL,
                        longitude decimal NOT NULL,
                        cluster INTEGER NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Hotel Facilities
cur.execute(""" DROP TABLE IF EXISTS hfacilities CASCADE; """)
cur.execute("""
    CREATE TABLE hfacilities (hfacilities_id SERIAL PRIMARY KEY,
                        f_hotel_id integer NOT NULL,
                        facilities_name varchar (150) NOT NULL,
                        facilities_image text NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (f_hotel_id) REFERENCES hotels(hotel_id));
            """)

# Provinsi
# Change 29/01/2023 --> province_id won't be connected to any of other entities
cur.execute(""" DROP TABLE IF EXISTS provinces CASCADE; """)
cur.execute("""
    CREATE TABLE provinces (province_id SERIAL PRIMARY KEY,
                        province_image text NOT NULL,
                        province_name text NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Tourism Type
# Change 29/01/2023 --> tourism_type_id won't be connected to any of other entities
cur.execute(""" DROP TABLE IF EXISTS tourism_type CASCADE; """)
cur.execute("""
    CREATE TABLE tourism_type (tourism_type_id SERIAL PRIMARY KEY,
                        tourism_type_image text NOT NULL,
                        tourism_type_name text NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Wisata
# Change 29/01/2023 --> Delete province_id column
#                   --> Change tourism_province to province_name for consistency
#                   --> Erase constraint of province_id
#                   --> Erase tourism_type_id
cur.execute(""" DROP TABLE IF EXISTS tourisms CASCADE; """)
cur.execute("""
    CREATE TABLE tourisms (tourism_id SERIAL PRIMARY KEY,
                            tourism_image text NOT NULL,
                            tourism_name text NOT NULL,
                            tourism_address text NOT NULL,
                            tourism_type varchar (150) NOT NULL,
                            tourism_city varchar (100) NOT NULL,
                            province_name varchar (150) NOT NULL,
                            open_hour varchar (100) NOT NULL,
                            close_hour varchar (100) NOT NULL,
                            tourism_description text NOT NULL,
                            entry_price integer NOT NULL,
                            traveling_time varchar (100) NOT NULL,
                            road_condition varchar (100) NOT NULL,
                            tourism_rating decimal NOT NULL,
                            latitude decimal NOT NULL,
                            longitude decimal NOT NULL,
                            created_at date DEFAULT CURRENT_TIMESTAMP,
                            updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)

# Tourism Routes
cur.execute(""" DROP TABLE IF EXISTS routes CASCADE; """)
cur.execute("""
    CREATE TABLE routes (routes_id SERIAL PRIMARY KEY,
                        r_tourism_id integer NOT NULL,
                        routes_desc text NOT NULL,
                        position integer NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (r_tourism_id) REFERENCES tourisms(tourism_id));
            """)

# Tourism Facilities
cur.execute(""" DROP TABLE IF EXISTS tfacilities CASCADE; """)
cur.execute("""
    CREATE TABLE tfacilities (tfacilities_id SERIAL PRIMARY KEY,
                        f_tourism_id integer NOT NULL,
                        facilities_name varchar (150) NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (f_tourism_id) REFERENCES tourisms(tourism_id));
            """)

# Favorite Hotel
cur.execute(""" DROP TABLE IF EXISTS favorite_hotel CASCADE; """)
cur.execute("""
    CREATE TABLE favorite_hotel (favorite_id SERIAL PRIMARY KEY,
                        h_user_id integer NOT NULL,
                        h_hotel_id integer NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (h_user_id) REFERENCES users(user_id),
                        FOREIGN KEY (h_hotel_id) REFERENCES hotels(hotel_id));
            """)

# Favorite Tourism
cur.execute(""" DROP TABLE IF EXISTS favorite_tourism CASCADE; """)
cur.execute("""
    CREATE TABLE favorite_tourism (favorite_id SERIAL PRIMARY KEY,
                        t_user_id integer NOT NULL,
                        t_tourism_id integer NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (tourism_id) REFERENCES tourisms(tourism_id));
            """)

# Nearest Event
cur.execute(""" DROP TABLE IF EXISTS nearest_event CASCADE; """)
cur.execute("""
    CREATE TABLE nearest_event (nearest_event_id SERIAL PRIMARY KEY,
                        event_image text NOT NULL,
                        event_name varchar (150) NOT NULL,
                        event_start_date varchar (100) NOT NULL,
                        event_end_date varchar (100) NOT NULL,
                        event_location varchar (150) NOT NULL,
                        event_description text NOT NULL,
                        created_at date DEFAULT CURRENT_TIMESTAMP,
                        updated_at date DEFAULT CURRENT_TIMESTAMP);
            """)


# Pivot Table Tourism Facilities
# cur.execute(""" DROP TABLE IF EXISTS tourism_facilities CASCADE; """)
# cur.execute("""
#     CREATE TABLE tourism_facilities (
#                         tfacilities_id integer REFERENCES tfacilities(tfacilities_id) ON UPDATE CASCADE ON DELETE CASCADE,
#                         tourism_id integer REFERENCES tourisms(tourism_id),
#                         CONSTRAINT tourism_facilities_pkey
#                             PRIMARY KEY (tfacilities_id, tourism_id));
#             """)

# Pivot Table Hotel Facilities
# cur.execute(""" DROP TABLE IF EXISTS hotel_facilities CASCADE; """)
# cur.execute("""
#     CREATE TABLE hotel_facilities (
#                         hfacilities_id integer REFERENCES hfacilities(hfacilities_id) ON UPDATE CASCADE ON DELETE CASCADE,
#                         hotel_id integer REFERENCES hotels(hotel_id),
#                         CONSTRAINT hotel_facilities_pkey
#                             PRIMARY KEY (hfacilities_id, hotel_id));
#             """)

conn.commit()

cur.close()
conn.close()