import socket
import threading

def read_msg(clients, sock_cli, addr_cli, username_cli):
    while True:

        # Terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        # Parsing pesan
        dest, msg = data.decode("utf-8").split("|")
        msg = "<{}>: {}".format(username_cli, msg)

        # Teruskan ke semua client
        if dest == "bcast":
            send_bcast(clients, msg, addr_cli)
        else:
            dest_sock_cli = clients[dest][0]
            send_msg(dest_sock_cli, msg)
        print(data)

    sock_cli.close()
    print("Connection closed", addr_cli)

# Broadcast
def send_bcast(clients, data, sender_addr_cli):
    for sock_cli, addr_cli, _ in clients.values():
        if not (sender_addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            send_msg(sock_cli, data)

def send_msg(sock_cli, data):
    sock_cli.send(bytes(data, "utf-8"))

# Buat object socket server
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding object socket ke IP dan port tertentu
sock_server.bind(("0.0.0.0", 6666))

# Listen 
sock_server.listen(5)

# Dictionary informasi klien
clients = {}

while True:
    # Accept connection dari klien
    sock_cli, addr_cli = sock_server.accept()

    # Baca Username
    username_cli = sock_cli.recv(65535).decode("utf-8")
    print(username_cli, " joined")

    # Thread untuk membaca pesan
    thread_cli = threading.Thread(target=read_msg, args=(clients, sock_cli, addr_cli, username_cli))
    thread_cli.start()

    # Simpan informasi klien ke dictionary
    clients[username_cli] = (sock_cli, addr_cli, thread_cli)