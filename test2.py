import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 65432))
print(s.recv(1024))
s.send(b"Bonjour Serveur 65432, nous sommes donc dans la phase de transfert")
s.send(b"Serveur 65432, je vous dis au revoir")
s.close()