import boto3
import psycopg2 as psql;
import os;
import json;

ENDPOINT=os.environ['DB_HOST']
PORT="5432"
USR="team9"
PASS="swen614Team9"
REGION="us-east-1"
DBNAME="CCDatabase"

sns = boto3.client('sns')


def determineStatus(numocc, maxcap,phonenumber, cursor, alert, room, building):
    result = numocc/maxcap * 100
    if(result <= 33):
        if(alert == True):
            update(room, building, cursor, alert)
            sns.publish(PhoneNumber = '+14089214831', Message='Status has dropped from Red', MessageAttributes={'AWS.SNS.SMS.SMSType' :{'DataType': 'String','StringValue': 'Transactional'}} )
        return 'green'
    elif (33 < result <= 67):
        if(alert == True):
            update(room, building, cursor, alert)
            sns.publish(PhoneNumber = phonenumber, Message='Status has dropped from Red', MessageAttributes={'AWS.SNS.SMS.SMSType' : {'DataType' : 'String','StringValue': 'Transactional'}} )
        return 'yellow'
    elif ( 67 < result):
        update(room, building, cursor, alert)
        sns.publish(PhoneNumber = '+14089214831', Message='Guidelines have been violated RED STATUS', MessageAttributes={'AWS.SNS.SMS.SMSType' :{'DataType': 'String','StringValue': 'Transactional'}} )
        return 'red'


def update(room, building, cursor, alert):
    if(alert == False):
        update_query = f"""UPDATE rooms SET alert = True WHERE room_number = '{room}' AND building_number = '{building}' """
    elif(alert==True):
        update_query = f"""UPDATE rooms SET alert = False WHERE room_number = '{room}' AND building_number = '{building}' """
    
    cursor.execute(update_query)


def main(event, context):
    
    try:
        conn = psql.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
        cur = conn.cursor()

        #Get the id for the room and building number from the file
        select_query = f""" SELECT DISTINCT ON (room_number) room_number, building_number, max_capacity, phone, num_occupants, alert FROM rooms JOIN room_admins ON rooms.id = room_admins.admin_id JOIN admins on admins.id = room_admins.room_id JOIN room_records ON room_records.room_id = room_admins.room_id JOIN records ON records.id = room_records.record_id  """
        cur.execute(select_query)
        roomrecords = cur.fetchall()
        for room in roomrecords:
            status = determineStatus(room[4],room[2],room[3], cur, room[5], room[0], room[1])
        conn.commit()
        conn.close()

    except Exception as e:
        print("Database connection failed due to {}".format(e))
    return {
        'statusCode': 200,
        "body": json.dumps({
            'room_number': roomrecords[0][0],
            'building_number': roomrecords[0][1],
            'max_capacity':roomrecords[0][2],
            'curr_capacity':roomrecords[0][4],
            'status':status
        }),
        "headers":{ 'Access-Control-Allow-Origin' : '*' }
        
    }