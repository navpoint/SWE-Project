import zmq
import csv
import json
import mysql.connector

# Establish the ZeroMQ context
context = zmq.Context()

# Establish the reply socket
socket = context.socket(zmq.REP)
socket.bind("tcp://*:33333")

# Connect to MySQL Database
def connect_mysql():
    return mysql.connector.connect(
        host='localhost',
        user='worker_user_service_test',
        password='usingservices',
        database='finance_tracker'
    )

def generate_csv(user_id):

    database = connect_mysql() #Cannot connect due to hashed password
    cursor = database.cursor(dictionary=True)

    query = "SELECT * FROM plans JOIN users ON plans.user_id = users.user_id WHERE users.user_id = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchall()

    if not user_data:
        return "No data found for this user ID. Please try again."
    
    with open("user_data_export.csv", mode="w", newline="") as csv_file:
        write_csv = csv.DictWriter(csv_file, fieldnames=user_data[0].keys())
        write_csv.writeheader()
        write_csv.writerows(user_data)
    
    return "File successfully received!"

while True:
    # Receive request from the sender
    csv_request_json = socket.recv()

    csv_request = json.loads(csv_request_json.decode('utf-8'))
    
    user_id = csv_request.get("user_id")

    if user_id:
        result_message = generate_csv(user_id)
        socket.send(result_message.encode())

        print("Generating CSV file...")
        
