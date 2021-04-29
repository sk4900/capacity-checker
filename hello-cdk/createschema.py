import boto3 as bt3
import psycopg2 as psql
import json
import sys

arg1 = str(sys.argv[1])
 
with open(r'.\frontend\src\cdk-outputs.json') as f:
    data = json.load(f)

ENDPOINT=data['HelloCdkStack']['rdsendpoint']
PORT="5432"
USR="team9"
PASS="swen614Team9"
REGION="us-east-1"
DBNAME="CCDatabase"


try:
    conn = psql.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS  rooms, admins, room_admins, records, room_records")

    create_schema = (
        """
        CREATE TABLE rooms 
        (
            id                INT GENERATED ALWAYS AS IDENTITY NOT NULL,
            room_number       TEXT NOT NULL,
            building_number   TEXT NOT NULL,
            max_capacity      INT NOT NULL,
            alert             BOOLEAN NOT NULL,
            PRIMARY KEY(id)
        )
        """,
        """
        CREATE TABLE admins
        (
            id              INT GENERATED ALWAYS AS IDENTITY NOT NULL,
            first_name      TEXT NOT NULL,
            last_name       TEXT NOT NULL,
            department      TEXT NOT NULL,
            phone           TEXT NOT NULL,
            email           TEXT NOT NULL,
            PRIMARY KEY(id)
        )
        """,
        """
         CREATE TABLE room_admins
        (
            room_id      INT NOT NULL,
            admin_id     INT NOT NULL,
            CONSTRAINT fk_room
                FOREIGN KEY(room_id)
                    REFERENCES rooms(id),
            CONSTRAINT fk_admin
                FOREIGN KEY(admin_id)
                    REFERENCES admins(id)
        )
        """,
        """
        CREATE TABLE records
        (
            id              INT GENERATED ALWAYS AS IDENTITY NOT NULL,
            record_date     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            num_occupants   INT NOT NULL,
            PRIMARY KEY(id)
        )
        """,
        """
        CREATE TABLE room_records
        (
            room_id      INT NOT NULL,
            record_id    INT NOT NULL,
            CONSTRAINT fk_room
                FOREIGN KEY(room_id)
                    REFERENCES rooms(id),
            CONSTRAINT fk_record
                FOREIGN KEY(record_id)
                    REFERENCES records(id)
        )
        """
    )
    for table in create_schema :
            cur.execute(table)

    rooms_insert_query = """ INSERT INTO rooms( room_number,building_number,max_capacity, alert ) VALUES (%s,%s,%s,%s)"""
    rooms_to_insert = ('2000','GOL',9,False)

    admins_insert_query = """ INSERT INTO admins(first_name, last_name, department, phone, email ) VALUES (%s,%s,%s,%s,%s)"""
    admins_to_insert = ('Devan', 'Lad', 'CS', arg1, 'dpl2047@g.rit.edu')

    room_admin_insert_query = """ INSERT INTO room_admins(room_id,admin_id) VALUES (%s,%s)"""
    room_admin_to_insert = (1,1)

    cur.execute(rooms_insert_query, rooms_to_insert)

    cur.execute(admins_insert_query, admins_to_insert)

    cur.execute(room_admin_insert_query, room_admin_to_insert)

    

    conn.commit()
    conn.close()
except Exception as e:
    print("Database connection failed due to {}".format(e))   
