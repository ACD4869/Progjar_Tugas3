import socket
import sys
import threading

def read_msg(sock_cli):
    while True:
        # Terima pesan
        data = sock_cli.recv(65535)
        if len (data) == 0:
            break
        print(data)
        
# Buat objek socket
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect ke server
sock_cli.connect(("127.0.0.1", 6666))

# Kirim Username
sock_cli.send(bytes(sys.argv[1], "utf-8"))

# Buat thread untuk membaca pesan
thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

while True:
    # Kirim/Terima pesan
    dest = input("Masukkan username tujuan (ketikkan bcast untuk broadcast pesan): ")
    msg = input("Masukkan pesan anda: ")

    if msg == "exit":
        sock_cli.close()
        break

    sock_cli.send(bytes("{}|{}".format(dest, msg), "utf-8"))
