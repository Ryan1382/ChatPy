import socket
import threading
import os

host = '127.0.0.1'  #PARA FUNCIONAR NO 4G, LOGAR NO 4G PRIMEIRO E COLOCAR IPV4 NO HOST
porta = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, porta))
server.listen()

clientes = []
nicknames = []

def broadcast(mensagem):
    for cliente in clientes:
        cliente.send(mensagem)

def sair(cliente):
    index = clientes.index(cliente)
    nickname = nicknames[index]
    clientes.remove(cliente)
    cliente.close()
    print(f'Usuario: {nickname} desconectado do servidor.')
    broadcast(f'{nickname} saiu do chat.'.encode())
    nicknames.remove(nickname)

def privado(cliente, mensagem):

    mensagem_privada = mensagem.split(' ',3)
    
    destinatario = mensagem_privada[2]
    mensagem_para_enviar = mensagem_privada[3]

    if destinatario in nicknames:
        index_destinatario = nicknames.index(destinatario)
        cliente_destinatario = clientes[index_destinatario]
        mensagem_final = f"Mensagem privada de {nicknames[clientes.index(cliente)]}: {mensagem_para_enviar}"

        cliente_destinatario.send(mensagem_final.encode())
        cliente.send(f"Mensagem enviada para {destinatario}: {mensagem_para_enviar}".encode())
    else:
        cliente.send(f"Erro: O usuário {destinatario} não está online.".encode())


def cliente_servidor(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode()

            if "/privado" in mensagem:
                privado(cliente, mensagem)
            else:
                broadcast(mensagem.encode())
        except:
            sair(cliente)
            
            break

def receber_servidor():
    while True:
        cliente, address = server.accept()

        cliente.send('Apelido'.encode())
        nickname = cliente.recv(1024).decode()
        nicknames.append(nickname)
        clientes.append(cliente)

        print(f"Usuário '{nickname}' conectado: {address}")
        broadcast(f"Servidor -> {nickname}, está participando no chat!".encode())
        cliente.send('Conectou com sucesso no server!'.encode()) 


        receber_servidor_thread = threading.Thread(target=cliente_servidor, args=(cliente,))
        receber_servidor_thread.start()

#---- Inicio ----#
os.system('cls')
print("Inicializando Servidor ...")
print("Servidor está no ar!!")
receber_servidor()
