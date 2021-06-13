import socket
import sys
import threading
        
# Buat objek socket
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_cli.settimeout(1)

# Connect ke server
sock_cli.connect(("127.0.0.1", 6666))

# Kirim Username
sock_cli.send(bytes(sys.argv[1], "utf-8"))

while True:
    # Kirim/Terima pesan
    option = input("\nApa yang ingin anda lakukan?\n"
                   "Tambah teman\n"
                   "Kirim pesan pribadi\n"
                   "Kirim pesan broadcast\n"
                   "Kirim file\n"
                   "Keluar\n"
                   ">> ")

    if option == "Keluar":
        sock_cli.close()
        break
    else:
        sock_cli.send(bytes(option, "utf-8"))
        if option == "Tambah teman":
            while True:
                try:
                    data = sock_cli.recv(65535).decode("utf-8")
                    print(data)
                except socket.timeout:
                    break
            adduser = input("Masukkan nama user yang ingin ditambahkan:\n")
            sock_cli.send(bytes(adduser, "utf-8"))
            msg = sock_cli.recv(65535).decode("utf-8")
            print(msg)