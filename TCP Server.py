import socket
import threading
import hashlib
from threading import Thread

ip = socket.gethostbyname(socket.gethostname())
porta = 5000
destino = (ip, porta)
buffer_size = 4096
arq = None

def escutar_cliente(tcp, endereco):
    msg_rec = ""
    while msg_rec != "__FIM":
        #print("Escutando o servidor...")
        msg_rec = tcp.recv(buffer_size).decode("cp860")
        tcp.send(msg_rec.encode("cp860"))

def handle_client(conexao, endereco):
    print("Nova conexão com a porta {}.".format(endereco))

    conectado = True
    while conectado:
        msg = conexao.recv(buffer_size).decode("cp860")
        if msg == "__solicitacao":
            msg2 = conexao.recv(buffer_size).decode("cp860")
            print("Vai abrir o arquivo {}...".format(msg2))
            try:
                arq = open(msg2, "rb")
            except:
                conexao.send("ERRO_ARQ".encode("cp860"))
                continue

            i = 1
            arq.seek(0, 0)
            info = arq.read(buffer_size)
            while len(info) == buffer_size:
                checksum = hashlib.sha256(info).digest()
                pacote = bytes(str(str(i) + " " + checksum.decode("cp860") + " "), "cp860")
                pacote += info
                conexao.send(pacote)

                msg2 = conexao.recv(buffer_size).decode("cp860")
                while msg2 == "":
                    msg2 = conexao.recv(buffer_size).decode("cp860")
                print(msg2)
                if msg2.split()[0] == "OK" and int(msg2.split()[1]) == i:
                    i += 1
                    info = arq.read(buffer_size)
            
            #RETRANSMITIR ÚLTIMO PACOTE.
            checksum = hashlib.sha256(info).digest()
            pacote = bytes(str(str(i) + " " + checksum.decode("cp860") + " "), "cp860")
            pacote += info
            while 1 == 1:

                conexao.send(pacote)

                msg2 = conexao.recv(buffer_size).decode("cp860")
                while msg2 == "":
                    msg2 = conexao.recv(buffer_size).decode("cp860")
                print(msg2)
                if msg2.split()[0] == "OK" and int(msg2.split()[1]) == i:
                    info = arq.read(buffer_size)
                    break

            conexao.send("fim_arq".encode("cp860"))

        elif msg == "__desconectar":
            conectado = False

        elif msg == "__CHAT":
            t1 = Thread(target=escutar_cliente, args=(conexao,endereco))
            t1.daemon = True
            t1.start()
            t1.join()

    conexao.close()

def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(destino)
    tcp.listen()

    while 1 == 1:
        conexao, endereco = tcp.accept()
        thread = threading.Thread(target=handle_client, args=(conexao, endereco))
        thread.start()
        print("Conectado com {}.".format(endereco))
        print("Conexões ativas: {}".format(threading.active_count() - 1))

if __name__ == "__main__":
    main()