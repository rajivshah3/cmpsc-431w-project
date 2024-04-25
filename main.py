import psycopg2
from psycopg2 import sql

def main_menu():
        invalid = False
        print("Welcome to the Database CLI Interface!\n")
        print("Please select an option:")
        print("1. Insert Data")
        print("2. Delete Data")
        print("3. Update Data")
        print("4. Search Data")
        print("5. Aggregate Functions")
        print("6. Sorting")
        print("7. Joins")
        print("8. Grouping")
        print("9. Subqueries")
        print("10. Transactions")
        print("11. Error Handling")
        print("12. Exit\n")
        choice_str = input("Enter your choice (1-12): ")
        print("\n")

        try:
            choice = int(choice_str)
        except ValueError:
            invalid = True
        
        if invalid or choice < 1 or choice > 12:
            print("Invalid option \n")
            return main_menu()
        
        return choice

statement_1 = """
INSERT INTO guests (guest_id, first_name, last_name, email, phone, nationality, birthdate, address, city, country)
VALUES (36137, 'John', 'Doe', 'johndoe@example.com', '302-555-1234', 'United States', '1980-10-10', '123 Main St', 'Anytown', 'United States');
"""
statement_2 = """
DELETE FROM guests WHERE guest_id = 36137;
"""

statement_3 = """
UPDATE reservations SET children = 2 WHERE reservation_id = 1441;
"""

statement_4 = """
SELECT * FROM reservations WHERE guest_id = 35906;
"""

statement_5 = """
SELECT COUNT(*) FROM reservations WHERE guest_id = 35906;
"""

statement_6 = """
SELECT reservation_id, checkin_time FROM reservations ORDER BY checkin_time LIMIT 10;
"""

statement_7 = """
SELECT * FROM guests g JOIN reservations r ON g.guest_id = r.guest_id LIMIT 10;
"""

statement_8 = """
SELECT COUNT(reservation_id), guest_id FROM reservations GROUP BY guest_id ORDER BY COUNT(reservation_id) DESC LIMIT 10;
"""

statement_9 = """
SELECT first_name, last_name FROM guests WHERE guest_id IN (
    SELECT r.guest_id FROM reservations r WHERE r.room_rate_id LIKE '1%'
);
"""

statement_10 = """
BEGIN;

UPDATE guests SET email = 'mynewemail@example.com' WHERE guest_id = 118;

UPDATE reservations SET reservation_source = 'Email' WHERE guest_id = 118;

COMMIT;
"""

statement_11 = """
DO
$$
BEGIN

SELECT guest_iid FROM reservations WHERE guest_iid = 1188292;

EXCEPTION
    WHEN undefined_column THEN
        RAISE EXCEPTION 'Column guest_iid not found';

END;
$$
"""


def main():
    try:
        conn = psycopg2.connect(database="hotels",
                            host="localhost",
                            user="postgres",
                            password="postgres",
                            port="5432")
        cur = conn.cursor()
    except Exception as e:
        print(f"{e}")
        print("Could not connect to db")

    print("Connected to db")

    while True:
        choice = main_menu()
        
        if choice == 1:
            print("Adding guest \"John Doe\"")
            print(f"Executing: {statement_1}")
            cur.execute(sql.SQL(statement_1))
            conn.commit()
        
        if choice == 2:
            print("Deleting guest with guest_id 36137")
            print(f"Executing: {statement_2}")
            cur.execute(sql.SQL(statement_2))
            conn.commit()

        if choice == 3:
            print("Changing number of children in reservation 1441 to 2")
            print(f"Executing: {statement_3}")
            cur.execute(sql.SQL(statement_3))
            conn.commit()

        if choice == 4:
            print("Searching for reservations for guest 35906")
            print(f"Executing: {statement_4}")
            cur.execute(sql.SQL(statement_4))
            print(cur.fetchall())
            conn.commit()

        if choice == 5:
            print("Finding how many reservations were made by guest 35906")
            print(f"Executing: {statement_5}")
            cur.execute(sql.SQL(statement_5))
            print(cur.fetchone()[0])
            conn.commit()

        if choice == 6:
            print("Getting 10 reservations sorted by check-in date")
            print(f"Executing: {statement_6}")
            cur.execute(sql.SQL(statement_6))
            print(cur.fetchall())
            conn.commit()

        if choice == 7:
            print("Getting 10 reservations with guest info")
            print(f"Executing: {statement_7}")
            cur.execute(sql.SQL(statement_7))
            print(cur.fetchall())
            conn.commit()
        
        if choice == 8:
            print("Getting top 10 guests by number of reservations")
            print(f"Executing: {statement_8}")
            cur.execute(sql.SQL(statement_8))
            print(cur.fetchall())
            conn.commit()

        if choice == 9:
            print("Finding names of people staying in room 1")
            print(f"Executing: {statement_9}")
            cur.execute(sql.SQL(statement_9))
            print(cur.fetchall())
            conn.commit()

        if choice == 10:
            print("Using a transaction to update guest 118's email and the source for all of their reservations")
            print(f"Executing: {statement_10}")
            cur.execute(sql.SQL(statement_10))
            print("Done")
            conn.commit()

        if choice == 11:
            print("Handling an error caused by an undefined column")
            print(f"Executing: {statement_11}")
            try:
                cur.execute(sql.SQL(statement_11))
            except psycopg2.errors.RaiseException as e:
                print("Exception:")
                print(e)
            conn.commit()

        if choice == 12:
            print("Goodbye")
            conn.close()
            return

        print("\n")

        

        
if __name__ == "__main__":
    main()
