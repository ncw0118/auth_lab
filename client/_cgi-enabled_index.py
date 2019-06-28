#!/usr/bin/env python

import cgi, cgitb, json, socket, base64
from hashlib import sha256
from Crypto.Cipher import AES

form = cgi.FieldStorage()
usrname = form.getvalue('username')
passwd = form.getvalue('password')
censor = ""
for char in passwd:
        censor += "*"

print "Content-type: text/html\n\n"
print "<html>\n<body>"
print "<div style=\"width: 100%; font-size: 24px; font-weight: bold; text-align: center;\">"
print "Authenticating with credentials: username=%s | password=%s"%(usrname,censor)
print "</div>\n</body>\n</html>"

host = "10.150.101.4" # Replace with the servers IP Addr
port = 9999     # servers socket port

host2 = "10.150.101.6"
port2 = 8888

def main():
        data = json.dumps({"un": usrname, "pw": passwd})
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        client.send(data.encode())
        receive = client.recv(4096)
        receive = base64.b64decode(receive.decode())

        if receive[0:2] == '{"':
                receive_d = json.loads(receive.decode())
                token = receive_d.get("token")
        else:
                hashedWord = sha256(passwd.strip()).digest()
                obj = AES.new(hashedWord.strip(), AES.MODE_CFB,'SuperRandomIV123')
                plaintext = obj.decrypt(receive)
                token = "0"
                plaintext = plaintext.split('"')[4]

        if token != "":
                print "Received data: %s<br>"%plaintext
                client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client2.connect((host2,port2))
                client2.send(plaintext.encode())
                receive = client2.recv(4096)
                print "Authenticated with token: %s"%receive.decode()
        else:
                print "Authentication Failure: Username and Password combination incorrect.<br>"
                print "Received %s from Authentication Server."%receive


main()

