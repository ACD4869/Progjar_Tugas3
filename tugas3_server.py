import socket
import threading

def read_msg(clients, sock_cli, addr_cli, username_cli, userlist, friendlist):
    while True:

        # Terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        # Parsing pesan
        msg = data.decode("utf-8").split("|")
        if len(msg) == 1:
            if msg[0] not in userlist:
                send_msg(sock_cli, msg[0] + " tidak ditemukan")
            elif msg[0] in friendlist[username_cli]:
                send_msg(sock_cli, "Sudah berteman dengan " + msg[0])
            elif msg[0] != username_cli:
                friendlist[username_cli].append(msg[0])
                friendlist[msg[0]].append(username_cli)
                send_msg(sock_cli, msg[0] + " berhasil ditambahkan")
                send_msg(clients[msg[0]][0], username_cli + " telah menambahkanmu")
        elif len(msg) == 2:
            sendmsg = "<{}>: {}".format(username_cli, msg[1])
            if msg[0] == "bcast":
                send_bcast(clients, sendmsg, addr_cli)
            else:
                if msg[0] in friendlist[username_cli]:
                    send_msg(clients[msg[0]][0], sendmsg)
                else:
                    send_msg(sock_cli, "User belum menjadi temanmu")
    sock_cli.close()
    print("Connection closed", addr_cli)
    userlist.remove(username_cli)
    for user in friendlist:
        if username_cli in friendlist[user]:
            friendlist[user].remove(username_cli)

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
userlist = []
friendlist = {}

while True:
    # Accept connection dari klien
    sock_cli, addr_cli = sock_server.accept()

    # Baca Username
    username_cli = sock_cli.recv(65535).decode("utf-8")
    print(username_cli, " joined")
    userlist.append(username_cli)

    # Thread untuk membaca pesan
    thread_cli = threading.Thread(target=read_msg, args=(clients, sock_cli, addr_cli, username_cli, userlist, friendlist))
    thread_cli.start()

    # Simpan informasi klien ke dictionary
    clients[username_cli] = (sock_cli, addr_cli, thread_cli)
    friendlist[username_cli] = []