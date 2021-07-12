import socketserver

BUFFER_SIZE = 1024

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        
        #full = False
        # self.request is the TCP socket connected to the client
        f = open('11.jpg','wb+') # Open in binary
        while (True):
            
            # Recibimos y escribimos en el fichero
            l = self.request.recv(100*1024)
            # while l:
            f.write(l)
            #     l = self.request.recv(1024)
            #     if not l:
            #         print('file rec.')
            #         full = True
            #         break
            self.request.sendall(b'hello')
            break   
            # break
        #if full:
        f.close()
            
        # self.data = self.request.recv(1024).strip()
        # print("{} wrote:".format(self.client_address[0]))
        # print(self.data)
        # # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8889

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()