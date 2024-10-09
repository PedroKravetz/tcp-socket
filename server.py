import socket
import threading
import os
import hashlib

# Função para calcular o hash SHA-256 de um arquivo
def calcular_hash_arquivo(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Função que lida com as requisições do cliente
def handle_client(conn, addr):
    print(f"Conexão de {addr} estabelecida.")
    while True:
        # Receber a requisição do cliente
        request = conn.recv(1024).decode()
        
        if not request:
            break
        
        # Tratamento para a requisição de "Sair"
        if request.lower() == "sair":
            print(f"Cliente {addr} desconectado.")
            break
        
        # Tratamento para a requisição de "Arquivo + NOME.EXT"
        elif request.startswith("arquivo"):
            _, nome_arquivo = request.split(" ")
            if os.path.exists(nome_arquivo):
                # Abrir o arquivo, calcular o hash, e enviar informações
                tamanho_arquivo = os.path.getsize(nome_arquivo)
                hash_arquivo = calcular_hash_arquivo(nome_arquivo)

                # Enviar nome, tamanho e hash
                conn.send(f"{nome_arquivo}\n{tamanho_arquivo}\n{hash_arquivo}\n".encode())

                # Enviar o arquivo em blocos
                with open(nome_arquivo, "rb") as f:
                    while (data := f.read(4096)):
                        conn.send(data)
                conn.send(b"FIM")
            else:
                conn.send("Arquivo inexistente\n".encode())

        # Tratamento para o "Chat"
        elif request.lower() == "chat":
            print(f"[Chat] {addr}: {request}")
            resposta = input("Servidor: ")
            conn.send(resposta.encode())

    conn.close()

# Configuração do servidor
def start_server():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("0.0.0.0", 12345))
    servidor.listen(5)
    print("Servidor iniciado. Aguardando conexões...")

    while True:
        conn, addr = servidor.accept()
        # Criar uma thread para cada cliente
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Clientes ativos: {threading.active_count() - 1}")

start_server()
