import socket
import threading
import hashlib
from threading import Thread

ip = socket.gethostbyname(socket.gethostname())
porta = 5000
destino = (ip, porta)
buffer_size = 4096
arq = None
flag_nok = 0
msg_rec = ""
conexoes = []
enderecos = []
global g
g = ""

def input_com_thread(tcp):
    msg_env = ""
    while msg_rec != "__FIM" and msg_env != "__FIM":
        msg_env = input("> ")
        tcp.send(msg_env.encode("ansi"))

def escutar_cliente(tcp, endereco):
    msg_rec = ""
    while msg_rec != "__FIM":
        #print("Escutando o servidor...")
        msg_rec = tcp.recv(buffer_size).decode("ansi")
        if msg_rec != '' and msg_rec != "__FIM":
            print("\n[CLIENTE {}]: {}".format(endereco, msg_rec))
            print("> ", end='')

    if msg_rec == "__FIM":
        tcp.send("__FIM".encode("ansi"))
        global g
        g = msg_rec
        return msg_rec

def handle_client(conexao, endereco):
    print("Nova conexão com a porta {}.".format(endereco))

    conectado = True
    while conectado:
        msg = conexao.recv(buffer_size).decode("ansi")
        if msg == "__solicitacao":
            msg2 = conexao.recv(buffer_size).decode("ansi")
            print("Vai abrir o arquivo {}...".format(msg2))
            try:
                arq = open(msg2, "rb")
            except:
                conexao.send("ERRO_ARQ".encode("ansi"))
                continue

            checksum_geral = hashlib.sha256(arq.read()).digest()
            print(checksum_geral)

            i = 1
            arq.seek(0, 0)
            info = arq.read(buffer_size)
            print("{} vs. {}".format(len(info), buffer_size))
            while len(info) == buffer_size:
                checksum = hashlib.sha256(info).digest()
                pacote = bytes(str(str(i) + " " + checksum.decode("ansi") + " "), "ansi")
                pacote += info
                conexao.send(pacote)

                msg2 = conexao.recv(buffer_size).decode("ansi")
                while msg2 == "":
                    msg2 = conexao.recv(buffer_size).decode("ansi")
                print(msg2)
                if msg2.split()[0] == "OK" and int(msg2.split()[1]) == i:
                    i += 1
                    info = arq.read(buffer_size)
                    flag_nok = 0
                else:
                    flag_nok = 1
                #elif msg2 == "NOK":

            #RETRANSMITIR ÚLTIMO PACOTE.
            checksum = hashlib.sha256(info).digest()
            pacote = bytes(str(str(i) + " " + checksum.decode("ansi") + " "), "ansi")
            pacote += info
            while 1 == 1:

                conexao.send(pacote)

                msg2 = conexao.recv(buffer_size).decode("ansi")
                while msg2 == "":
                    msg2 = conexao.recv(buffer_size).decode("ansi")
                print(msg2)
                if msg2.split()[0] == "OK" and int(msg2.split()[1]) == i:
                    info = arq.read(buffer_size)
                    break



            conexao.send("fim_arq".encode("ansi"))



        elif msg == "__desconectar":
            conectado = False

        elif msg == "__CHAT":
            #msg_rec = conexao.recv(buffer_size).decode("ansi")
            #t1 = Thread(target = input_com_thread, args=(conexao,))
            #t1.start()
            #while msg_rec != "__FIM":
            #    if msg_rec != "":
            #        print("[CLIENTE]: {}".format(msg_rec))
            #        print("> ", end='')
            #    msg_rec = conexao.recv(buffer_size).decode("ansi")

            t1 = Thread(target=escutar_cliente, args=(conexao,endereco))
            t1.daemon = True
            t1.start()
            print("Chat iniciado.")
            msg_env = ""
            while msg_env != "__FIM" and g != "__FIM":
                #print("GLOBAL = {}".format(g))
                msg_env = input("> ")
                if msg_env[0] == '#':
                    cont = 0
                    receptor = msg_env.split(sep=" ")[0][1:]
                    print("Procurando {}".format(receptor))
                    for elemento in enderecos:
                        print("{} vs {}".format(elemento[1], receptor))
                        if int(elemento[1]) == int(receptor):
                            s = " "
                            conexoes[cont].send(s.join(msg_env.split(sep=" ")[1:]).encode("ansi"))
                            break
                        else:
                            cont = cont + 1

                else:

                    for item in conexoes:
                        item.send(msg_env.encode("ansi"))
                    #conexao.send(msg_env.encode("ansi"))

            conexao.send("__FIM".encode("ansi"))

        #print("Mensagem recebida de {}: {}".format(endereco, msg))
        conexao.send(msg.encode("ansi"))




    conexao.close()

def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(destino)
    tcp.listen()

    while 1 == 1:
        conexao, endereco = tcp.accept()
        thread = threading.Thread(target=handle_client, args=(conexao, endereco))
        thread.start()
        conexoes.append(conexao)
        print("Conectado com {}.".format(endereco))
        enderecos.append(endereco)
        print("Conexões ativas: {}".format(threading.active_count() - 1))

if __name__ == "__main__":
    main()