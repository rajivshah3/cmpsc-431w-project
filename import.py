import psycopg2
from psycopg2 import sql

table_data = ["guests", "rooms", "room_rates", "reservations", "payments"]

conn = psycopg2.connect(database="hotels",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")
cur = conn.cursor()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
tables = cur.fetchall()
        
# Drop each table
for table in tables:
    print(f"Dropping {table}")
    cur.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table[0])))

conn.commit()

create_statement = sql.SQL("""
CREATE TABLE IF NOT EXISTS guests (
    guest_id BIGINT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    nationality TEXT,
    birthdate TIMESTAMP,
    address TEXT,
    city TEXT,
    country TEXT
);
""")
cur.execute(create_statement)
conn.commit()

create_statement = sql.SQL("""
CREATE TABLE IF NOT EXISTS rooms (
    room_number BIGINT PRIMARY KEY,
    floor_number BIGINT,
    room_type TEXT
);
""")
cur.execute(create_statement)
conn.commit()

# cur.execute("""SELECT table_name FROM information_schema.tables 
#                           WHERE table_schema = 'public'""")
# tables = cur.fetchall()
# print(tables)

create_statement = sql.SQL("""
CREATE TABLE IF NOT EXISTS room_rates (
    room_number BIGINT,
    FOREIGN KEY (room_number) REFERENCES rooms(room_number),
    room_rate BIGINT,
    room_rate_id TEXT PRIMARY KEY
);
""")
cur.execute(create_statement)
conn.commit()

create_statement = sql.SQL("""
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id BIGINT PRIMARY KEY,
    guest_id BIGINT,
    FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
    checkin_time TIMESTAMP,
    checkout_time TIMESTAMP,
    adults BIGINT,
    children BIGINT,
    reservation_source TEXT,
    booking_date TIMESTAMP,
    special_requests TEXT,
    breakfast_included BOOLEAN,
    spa_package_included BOOLEAN,
    airport_pickup_included BOOLEAN,
    room_rate_id TEXT,
    prepayment_id TEXT,
    other_payment_id TEXT,
    FOREIGN KEY (room_rate_id) REFERENCES room_rates(room_rate_id)
);
""")
cur.execute(create_statement)
conn.commit()

create_statement = sql.SQL("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id TEXT PRIMARY KEY,
    payment_method TEXT,
    payment_status TEXT,
    payment_amount DOUBLE PRECISION
);
""")
cur.execute(create_statement)
conn.commit()

for table in table_data:
    with open(f"./{table}.csv") as f:
        # Skip header
        next(f)
        print(f"Importing {table}")
        cur.copy_from(f, table=table, sep=',', null='<NA>')
        conn.commit()

cur.execute("SELECT * FROM guests")
cur.fetchone()
cur.close()
conn.close()
print("Done")
