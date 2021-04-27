import boto3
import psycopg2 as psql;
import os;

ENDPOINT=os.environ['DB_HOST']
PORT="5432"
USR="team9"
PASS="swen614Team9"
REGION="us-east-1"
DBNAME="CCDatabase"

def main(event, context):
    # save event to logs
    
    #test statements
    
    filename = f"""{event['Records'][0]['body']}"""
    peopleCount = f"""{event['Records'][0]['messageAttributes']['Count']['stringValue']}"""
    fsplit = filename.split("_")
    building = fsplit[0]
    room_number = fsplit[1]
    try:
        conn = psql.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
        cur = conn.cursor()

        #Get the id for the room and building number from the file
        select_room_query = f""" SELECT id FROM rooms WHERE room_number = '{room_number}' AND building_number = '{building}'"""
        cur.execute(select_room_query)
        room_id = cur.fetchone()[0]

        #insert the count
        records_insert_query = f""" INSERT INTO records(num_occupants) VALUES ({peopleCount}) RETURNING id"""
        cur.execute(records_insert_query)
        records_id =  cur.fetchone()[0]


        room_records_insert_query = f""" INSERT INTO room_records(room_id, record_id) VALUES ({room_id},{records_id})"""

        cur.execute(room_records_insert_query)

        conn.commit()
        conn.close()
    except Exception as e:
        print("Database connection failed due to {}".format(e))
    return {
        'statusCode': 200,
        'body': event
    }
