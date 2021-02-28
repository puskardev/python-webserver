import socket


# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8082

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print (request)
    
    #parse the HTTP request
    split_request = request.split("\n")

    #get the request line from the request message
    request_line = split_request[0]   

    #get fielname from request line
    temp = request_line.split(" ")

    for i in range(len(temp)):
        if (i == 1):
            filename = temp[i]

    filename = filename[1:]
    print(filename)

    f = open('htdocs/' + filename)
    content = f.read()
    f.close()

    print(content)
      

    # Send HTTP response
    response = 'HTTP/1.0 200 OK\n\n' + content
    client_connection.sendall(response.encode())

    client_connection.close()

# Close socket
server_socket.close()

#https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
