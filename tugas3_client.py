import socket
import sys
import threading

def read_msg(sock_cli):
    while True:
        data = sock_cli.recv(65535).decode("utf-8")
        if len(data) == 0:
            break
        print(data)

# Buat objek socket
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect ke server
sock_cli.connect(("127.0.0.1", 6666))

# Kirim Username
sock_cli.send(bytes(sys.argv[1], "utf-8"))

thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

while True:
    # Kirim/Terima pesan
    option = input("\nApa yang ingin anda lakukan?\n"
                   "Tambah teman\n"
                   "Kirim pesan\n"
                   "Kirim file\n"
                   "Keluar\n"
                   ">> ")

    if option == "Keluar":
        sock_cli.close()
        break
    elif option == "Tambah teman":
        dest = input("Masukkan username yang ingin ditambahkan sebagai teman: ")
        sock_cli.send(bytes(dest, "utf-8"))
    elif option == "Kirim pesan":
        dest = input("Masukkan username tujuan (ketikkan bcast untuk broadcast pesan): ")
        msg = input("Masukkan pesan anda: ")
        sock_cli.send(bytes("{}|{}".format(dest, msg), "utf-8"))
    elif option == "Kirim file":
        dest = input("Masukkan username tujuan (ketikkan bcast untuk broadcast pesan): ")
        filename = input("Masukkan nama file: ")
        #open file
        #send to server
