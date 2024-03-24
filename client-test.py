import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = '127.0.0.1'  # Server address
port_number = 50007  # Server port
client_socket.connect((server_address, port_number))

try:
    
    # Send data
    message = 'Hello, Server!'
    print(f"Sending: {message}")
    client_socket.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = client_socket.recv(1024)
        amount_received += len(data)
        print(f"Received: {data.decode()}")
finally:
    # Clean up the connection
    client_socket.close()


def connection_loop():
    """loops through sending requests and printing responses"""

    try:
        while True:
            #Asks for user input
            request_message = input("Please input request message: ")
            print(f"Sending: {message}")

    #handles exception in the message sending/recieving process
    except Exception as e:
        print(f"Encountered error : {e}")
    #closes up the connection even if there's an error
    finally:
        client_socket.close()