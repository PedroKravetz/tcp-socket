import socket
import hashlib

# Função para verificar o hash do arquivo recebido
def verificar_hash_arquivo(file_path, hash_servidor):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest() == hash_servidor

# Cliente TCP
def start_client():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("127.0.0.1", 12345))

    while True:
        # Enviar a requisição para o servidor
        request = input("Digite a requisição ('Sair', 'Arquivo nome.txt', 'Chat'): ")
        request.strip()
        cliente.send(request.encode())
        
        if request == "Sair":
            print("Desconectando do servidor...")
            break
        
        elif request.startswith("arquivo"):
            # Receber nome, tamanho e hash do arquivo
            nome_arquivo = cliente.recv(1024).decode().strip()
            tamanho_arquivo = int(cliente.recv(1024).decode().strip())
            hash_arquivo = cliente.recv(1024).decode().strip()
            
            # Receber os dados do arquivo
            with open(nome_arquivo, "wb") as f:
                while True:
                    data = cliente.recv(4096)
                    if data == b"FIM":
                        break
                    f.write(data)
            
            # Verificar a integridade do arquivo
            if verificar_hash_arquivo(nome_arquivo, hash_arquivo):
                print(f"Arquivo {nome_arquivo} recebido e verificado com sucesso.")
            else:
                print("Erro: hash do arquivo não corresponde.")
        
        elif request == "Chat":
            # Enviar e receber mensagens de chat
            resposta = cliente.recv(1024).decode()
            print(f"Servidor: {resposta}")

    cliente.close()

start_client()
