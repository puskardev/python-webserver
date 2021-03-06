#Puskar Dev
#CSE 4344 : Lab 1 WebServer Programming
#Date: 02/28/2021
#Student ID: 1001516630

# This code implements a webserver in Python. This code runs perfectly on Chrome. While, on firefox and edge, the image on the webpage
# may not be displayed.

# RECOMMENDED TO TEST ON GOOGLE CHROME


import socket

# First we define socket host and port. we use 0.0.0.0 which .0.0.0 means all IPv4 addresses on the local machine.
HOST = '0.0.0.0'
PORT = 8095  #In this case, we are using this specific port-number.


# We create a TCP socket by setting server_socket variable and set it to AF_INET(IPv4 address family) and SOCK_STREAM(TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#bind method binds server_scoket to the HOST and IP mentioned above so that it can listen to incomming requests.
server_socket.bind((HOST, PORT))

#server begins listening for incomming requests
server_socket.listen(1)

print('The server is ready to receive at port %s ...' % PORT)


#GET is a function which takes two parameters args(filename) and type(fieltype). It bascially assists request handler function in reutrning the content 
#of a file. There are two types of files we are particularly interested in one is plain text, while other is image.
def get(args):

    # when user does not provide the file name i the request. this condition is satisfied.
    if args == '/':
        args = '/index.html'
        
    f = open('htdocs' + args, 'rb')

    # Reading the file contents
    content = f.read()

    #close the file after reading
    f.close()
    return content

def handle_request(request):
    # We print the request to the console, to show that request from the client is successfully received.
    print(request)

    # HTTP request sent by client has various line, we split each line of the request.
    headers = request.split('\n')

    # headers[0] will have the request line. and we split it using ' '. to acces the filename and method.
    get_content = headers[0].split()   
    

    #we try to complete the request in this block
    try:
        # get the filename from the request line.
        filename = get_content[1]

        #This is for 301 stattus code for 'index1.html'. It returns '301' which is handled below.
        if filename == '/index1.html':
            return '301'

        #if the method is GET in the request, we get the contents of that file calling the get function passing filename and filetype.
        if get_content[0] == "GET":
            content = get(filename)
            return content

    #if the file is not found then this condition is entered. which simply returns None which is handled below.        
    except FileNotFoundError:
        return None



#infinte loop 
while True:
    # Here we wait for the client conection
    client_connection, client_address = server_socket.accept()

    # client types their request in the broeswe to access a file, which is communicated through HTTP to the server.
    # Thus, the HTTP client(browser) sends a reuqest to our server which is received and decoded to string.
    request = client_connection.recv(10240).decode()

    # we call the handle_request function on the request to grab the required response requested by the client.
    # thus, the response is stored in content.
    content = handle_request(request)

       
    # if the conent returned is neither None (404) or '301' (301). It can be either a html or jpeg file, which is handled below
    if (content != None) and (content != '301'):

        #if the file is a html file, then send the response.
        if str(content).find("html") > 0:
            
            #status line of response indicatig success. 
            client_connection.send('HTTP/1.1 200 OK\n\n'.encode())
            client_connection.send(content)

        #if the file is image file, then send the response
        else:
            client_connection.send('HTTP/1.1 200 OK\r\n'.encode())

            #Header lines for the image response.
            client_connection.send("Content-Type: image/jpeg\r\n".encode())
            client_connection.send("Accept-Ranges: bytes\r\n\r\n".encode())
            client_connection.send(content)
    
    # if the is a 301 i.e. user requested 'index1.html' then the 301 status code with new location is sent.
    if (content == '301'):
        client_connection.send('HTTP/1.1 301 Moved Permanently\r\n'.encode())
        client_connection.send('Location: /index.html\r\n\r\n'.encode())
    
    # if the file is not fouund. 404 is retruned with message. File not found.
    if content == None:
        response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
        client_connection.send(response.encode())

    #client connection is closed.
    client_connection.close()

# server_socket is closed as per TCP.
server_socket.close()

#REFRENCES
#codement.io  
#stackoverflow 

