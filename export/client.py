import zmq
import json

# Establish the ZeroMQ context
context = zmq.Context()

# Establish the request socket
print("Connecting to CS361 server..")
client_socket = context.socket(zmq.REQ)
client_socket.connect("tcp://localhost:33333")

user_id = input("Please enter user ID: ")

request_user_id = {
    "user_id": user_id
}

client_socket.send_string(json.dumps(request_user_id))

response = client_socket.recv()
print(response.decode())
