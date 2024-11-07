import _thread
import socket
import hashlib
import math
import time
from threading import Thread

def custom_round(f):
    if f - math.floor(f) > 0.9999999999:
        return math.floor(f) + 1
    else:
        return math.floor(f)

ip = socket.gethostbyname(socket.gethostname())
porta = 5000
destino = (ip, porta)
buffer_size = 4096
buffer = []
msg_rec = "a"
conectado = False

def escutar_servidor(tcp):
    msg_rec = ""
    while msg_rec != "__FIM":
        #print("Escutando o servidor...")
        msg_rec = tcp.recv(buffer_size).decode("ansi")
        if msg_rec != '':
            print("[SERVIDOR]: {}".format(msg_rec))
            print("> ", end='')

def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(destino)
    conectado = True
    msg2 = ""

    while conectado:
        print("Digite: (1) Entrar em modo de chat;\n(2) Para solicitar um arquivo;\n(99) Para sair.")
        msg = input("> ")

        if msg == "1":

            t1 = Thread(target=escutar_servidor, args=(tcp,))
            t1.daemon = True
            t1.start()
            tcp.send("__CHAT".encode("ansi"))
            print("Chat iniciado.")
            while msg2 != "__FIM":

                msg2 = input("> ")
                tcp.send(msg2.encode("ansi"))

                #msg_rec = tcp.recv(buffer_size).decode("ansi")
                #if msg_rec != '':
                #    print("[SERVIDOR]: {}".format(msg_rec))


        elif msg == "2":

            tcp.send("__solicitacao".encode("ansi"))
            print("Digite o endereço do arquivo: ")
            nome_arq = input()
            print("Digite o nome do arquivo a ser criado: ")
            nome_novo = input()
            tcp.send(nome_arq.encode("ansi"))
            msg2 = tcp.recv(buffer_size+40).decode("ansi")
            print("[SERVIDOR]: {}".format(msg2))
            if msg2 == "ERRO_ARQ":
                print("Erro na abertura do arquivo.")
                continue

            #msg2 = tcp.recv(buffer_size+40).decode("ansi")
            i = 1
            while msg2 != "fim_arq":
                hash = hashlib.sha256(msg2[custom_round(math.log(i,10))+35:].encode("ansi")).digest().decode("ansi")
                if hash == msg2[custom_round(math.log(i,10))+2:custom_round(math.log(i,10))+34]:
                    tcp.send(str("OK " + str(i)).encode("ansi"))


                    buffer.append(msg2[custom_round(math.log(i,10))+35:].encode("ansi"))
                    i += 1
                    #print(msg2[custom_round(math.log(i,10))+35:])
                else:
                    tcp.send(str("NOK " + str(i)).encode("ansi"))
                    print(hash)
                    print(msg2[custom_round(math.log(i,10))+2:custom_round(math.log(i,10))+32])
                    time.sleep(1)


                msg2 = tcp.recv(buffer_size+40).decode("ansi")

            print("Recepção concluída com sucesso.")

            arq_novo = None
            try:
                arq_novo = open(nome_novo, "wb")
            except:
                print("Erro na criação do arquivo novo.")
                continue

            for item in buffer:
                arq_novo.write(item)

            arq_novo.close()


        elif msg == "__desconectar" or msg == "99":
            conectado = False

if __name__ == "__main__":
    main()