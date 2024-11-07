import socket
import threading
from threading import Thread

ip = socket.gethostbyname('localhost')
porta = 8088
destino = (ip, porta)
buffer_size = 4096
arq = None
conexoes = []
enderecos = []

def handle_client(conexao, endereco):
    rd = conexao.recv(buffer_size).decode("ansi")
    print(rd)
    return
    cortes = rd.split()
    try:
        arq = open("C:/Users/nitro5/PycharmProjects/Web Server/.venv/misc" + cortes[1], "rb")
    except:
        print("ERRO: Página não encontrada.")
        dados = "HTTP/1.1 404"
        conexao.sendall(dados.encode("ansi"))
        conexao.shutdown(socket.SHUT_WR)
        return

    if (len(cortes) > 0): print("C:/Users/Tiago/PycharmProjects/Web Server/.venv/misc" + cortes[1])
    dados = "HTTP/1.1 200 OK\r\n"
    dados += "Server: Microsoft-IIS/4.0\r\nDate: Mon, 3 Jan 2016 17:13:34 GMT\r\n"
    cortes2 = cortes[1].split(sep=".")
    if cortes2[1] == "html":
        dados += "Content-Type: text/html; charset=utf-8\r\n"
    elif cortes2[1] == "jpeg":
        dados += "Content-Type: image/jpeg\r\n"
    elif cortes2[1] == "jpg":
        dados += "Content-Type: image/jpeg\r\n"
    elif cortes2[1] == "png":
        dados += "Content-Type: image/png\r\n"
    elif cortes2[1] == "mp3":
        dados += "Content-Type: audio/mpeg\r\n"
    elif cortes2[1] == "mp4":
        dados += "Content-Type: video/mp4\r\n"
    elif cortes2[1] == "pdf":
        dados += "Content-Type: application/pdf\r\nContent-Disposition: inline\r\n"
    elif cortes2[1] == "ico":
        dados += "Content-Type: image/x-icon\r\n"
    dados += "Last-Modified: Mon, 11 Jan 2016 17:24:42 GMT\r\n"
    #dados = dados.encode("ansi")
    linhas = None
    #dados += "<html><body>Hello World</body></html>\r\n\r\n"
    try:
        linhas = arq.readlines()
    except:
        print("Erro na leitura do arquivo.")
    i = 0
    for item in linhas:
        linhas[i] = item.decode("ansi")
        i += 1
    s = ""
    if (linhas is not None):
        dados += "Content-Length: " + str(len(s.join(linhas))) + "\r\n\r\n"
        dados += s.join(linhas)
    conexao.sendall(dados.encode("ansi"))
    conexao.shutdown(socket.SHUT_WR)




    conexao.close()

def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(destino)
    tcp.listen(5)

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