import socket

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8090

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

def get(args, type):
    if args == '/':
        args = '/index.html'
        fin = open('htdocs' + args)
    if type != "image":
        fin = open('htdocs/' + args)

    if type == "image":
        fin = open('htdocs/' + args, 'rb')

    # Read file contents
    content = fin.read()
    fin.close()
    return content

def handle_request(request):
    # Parse headers
    print(request)
    headers = request.split('\n')
    get_content = headers[0].split()

    accept = headers[6].split()
    type_content = accept[1].split('/')

    try:
        # Filename
        filename = get_content[1]

        if filename == '/index1.html':
            return '301'

        if get_content[0] == "GET":
            content = get(get_content[1], type_content[0])


        return content
    
    except FileNotFoundError:
        return None




while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Handle client request
    request = client_connection.recv(10240).decode()
    content = handle_request(request)

       
    # Send HTTP response
    if (content != None) and (content != '301'):
        if str(content).find("html") > 0:
            client_connection.send('HTTP/1.1 200 OK\n\n'.encode())
            client_connection.send(content.encode())
        else:
            client_connection.send('HTTP/1.1 200 OK\r\n'.encode())
            client_connection.send("Content-Type: image/jpeg\r\n".encode())
            client_connection.send("Accept-Ranges: bytes\r\n\r\n".encode())
            client_connection.send(content)
    
    if (content == '301'):
        client_connection.send('HTTP/1.1 301 Moved Permanently\r\n'.encode())
        client_connection.send('Location: /index.html\r\n\r\n'.encode())
   
    if content == None:
        response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
        client_connection.send(response.encode())

    client_connection.close()

# Close socket
server_socket.close()

