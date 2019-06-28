import socket, threading, json, base64
from Crypto.Cipher import AES


host = "0.0.0.0" #empty string so that it accepts on all interfaces
port = 8888 #port we will use for the socket

def main():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        print"[*] Listening on %s:%d"%(host,port)

        while True:
                conn,addr = server.accept()
                print"[*]Accepted connection from:%s:%d"%(addr[0],addr[1])
                client_handler = threading.Thread(target=handle_client,args=(conn,))
                client_handler.start()


def handle_client(client_socket):
        auth_json = client_socket.recv(1024)
        auth_json = base64.b64decode(auth_json.decode())

        obj = AES.new('secretkeythatsexactly32byteslong', AES.MODE_CFB,'SuperRandomIV987')
        auth_json = obj.decrypt(auth_json)

        token = auth_json
        print "[*]Successfully acquired token: %s"%token

        client_socket.send(token.encode())
        client_socket.close()


main()

