import socket
import threading

def read_msg(clients, sock_cli, addr_cli, username_cli, userlist, friendlist):
    while True:

        # Terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        # Parsing pesan
        msg = data.decode("utf-8")
        if msg == "Tambah teman":
            send_msg(sock_cli, "\nDaftar user tersedia:")
            for user in userlist:
                if user != username_cli and user not in friendlist[username_cli]:
                    send_msg(sock_cli, user)
            adduser = sock_cli.recv(65535).decode("utf-8")
            if adduser != username_cli and adduser in userlist:
                friendlist[username_cli].append(adduser)
                friendlist[adduser].append(username_cli)
                send_msg(sock_cli, adduser + " berhasil ditambahkan")
                print(username_cli + " dan " + adduser + " sekarang berteman")
            else:
                send_msg(sock_cli, "Username tidak ditemukan")
    sock_cli.close()
    print("Connection closed", addr_cli)
    userlist.remove(username_cli)
    #for flist in friendlist:
    #    flist.remove(username_cli)
    #friendlist[username_cli] = []

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