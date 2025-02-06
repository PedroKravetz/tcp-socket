import socket
import hashlib
import time

ip = socket.gethostbyname(socket.gethostname())
porta = 5000
destino = (ip, porta)
buffer_size = 4096
conectado = False

def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(destino)
    conectado = True
    msg2 = ""

    while conectado:
        print("Digite: (1) Entrar em modo de chat;\n(2) Para solicitar um arquivo;\n(3) Para sair.")
        msg = input("> ")
        buffer = []

        if msg == "1":
            tcp.send("__CHAT".encode("cp860"))
            print("Chat iniciado.")
            while msg2 != "__FIM":

                msg2 = input("> ")
                tcp.send(msg2.encode("cp860"))
                print(tcp.recv(buffer_size).decode("cp860"))


        elif msg == "2":

            tcp.send("__solicitacao".encode("cp860"))
            print("Digite o endereço do arquivo: ")
            nome_arq = input()
            print("Digite o nome do arquivo a ser criado: ")
            nome_novo = input()
            tcp.send(nome_arq.encode("cp860"))
            msg2 = tcp.recv(buffer_size+40).decode("cp860")

            if msg2 == "ERRO_ARQ":
                print("Erro na abertura do arquivo.")
                continue

            i = 1
            while msg2 != "fim_arq":
                hash = hashlib.sha256(msg2[msg2.find(" ")+1+32+1:].encode("cp860")).digest().decode("cp860")
                if hash == msg2[msg2.find(" ")+1:msg2.find(" ")+1+32]:
                    tcp.send(str("OK " + str(i)).encode("cp860"))

                    buffer.append(msg2[msg2.find(" ")+1+32+1:].encode("cp860"))
                    i += 1
                else:
                    tcp.send(str("NOK " + str(i)).encode("cp860"))
                    print(hash)
                    print(msg2[msg2.find(" ")+1:msg2.find(" ")+1+32])
                    time.sleep(1)


                msg2 = tcp.recv(buffer_size+40).decode("cp860")

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


        elif msg == "3":
            conectado = False

if __name__ == "__main__":
    main()