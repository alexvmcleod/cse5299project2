import socket
import struct

# we connect the socket to the server's address and port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '127.0.0.1' 
server_port_number = 50007 
client_socket.connect((server_address, server_port_number))

try:
    # we send the data
    message = input("Enter Request Message: ")
    print(f"Sending: {message}")
    client_socket.sendall(message.encode())
    
    # we recieve first 4 bytes to print out header value
    response_header_bytes = client_socket.recv(4)
    response_header = struct.unpack('!i', response_header_bytes)[0]

    # header value either indicates the response length (positive)
    # or the error message (negative)
    match response_header:
        # -1 is thrown if the user inputs a non letter character (barring wildcards)
        case -1:
            print("Error Detected! Invalid Input")
        # -2 is thrown if the server finds no values
        case -2:
            print("Error Detected! No Items Found")
        # -3 is thrown if there is an error on the server side (server encounters an exception)
        case -3:
            print("Error Detected! Internal Server Error")
        #indicates succesful response
        case default:
            print("Successful Response! Printing out response:")
            payload = client_socket.recv(response_header)
            print(payload.decode())

finally:
    # Clean up the connection
    client_socket.close()