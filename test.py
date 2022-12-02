import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 65432))
s.listen(10)
conn, t = s.accept()
conn.send(b"Bonjour Client, je suis le serveur 65432, la connexion est etablie")
print(conn.recv(1024))
print(conn.recv(1024))
conn.close()