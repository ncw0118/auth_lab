import socket, threading, json, requests, base64
from hashlib import sha256
from Crypto.Cipher import AES


host = "0.0.0.0" #empty string so that it accepts on all interfaces
port = 9999 #port we will use for the socket

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
        creds = client_socket.recv(1024)
        creds = json.loads(creds.decode())
        username = creds.get("un")
        password = creds.get("pw")
        censored = ""
        for char in password:
                censored += "*"
        print"[*]Received Username: %s and Password: %s from client"%(username,censored)

        data = {
                'grant_type': 'client_credentials'
        }

        response = requests.post('http://192.168.58.131/token.php', data=data, auth=(username, password))

        response = response.json()
        token = response.get("access_token")
        print"[*]User Token from OAuth: %s"%(token)

        if token == None:
                client_enc = json.dumps({"auth": "fail", "token": ""})
        else:
                apptoken = secret_key_enc(token)
                client_data = json.dumps({"auth": "success", "token": apptoken.encode()})
                client_enc = encrypt(password, client_data)

        client_socket.send(base64.b64encode(client_enc).encode())
        client_socket.close()


def secret_key_enc(token):
        obj = AES.new('secretkeythatsexactly32byteslong', AES.MODE_CFB, 'SuperRandomIV987')
        return base64.b64encode(obj.encrypt(token))


def encrypt(password, client_data):
        hashedWord = sha256(password.strip()).digest()
        obj = AES.new(hashedWord.strip(), AES.MODE_CFB, 'SuperRandomIV123')
        return obj.encrypt(json.dumps(client_data))


main()


