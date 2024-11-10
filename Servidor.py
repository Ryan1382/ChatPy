import socket
import threading
import os

host = '127.0.0.1'
porta = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, porta))
server.listen()

clientes = []
nicknames = []

def broadcast(mensagem):
    for cliente in clientes:
        cliente.send(mensagem)

        

def cliente_servidor(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024)

            if mensagem.decode() == "/sair":
                index = clientes.index(cliente)
                nickname = nicknames[index]
                clientes.remove(cliente)
                cliente.close()
                print(f'Usuario: {nickname} desconectado do servidor.')
                broadcast(f'{nickname} saiu do chat.'.encode())
                nicknames.remove(nickname)
                break
            
            broadcast(mensagem)
        except:
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            print(f'Usuario: {nickname} desconectado do servidor.')
            nickname = nicknames[index]
            broadcast('{} Saiu do Chatpy!'.format(nickname).encode(''))
            nicknames.remove(nickname)
            break

def receber_servidor():
    while True:
        cliente, address = server.accept()

        cliente.send('NICK'.encode())
        nickname = cliente.recv(1024).decode()
        nicknames.append(nickname)
        clientes.append(cliente)

        print("Usuário '{}' conectado: {}".format(nickname, str(address)))
        broadcast("{}, está participando no chat!".format(nickname).encode())
        cliente.send('Conectou com sucesso no server!'.encode()) 

        receber_servidor_thread = threading.Thread(target=cliente_servidor, args=(cliente,))
        receber_servidor_thread.start()

#---- Inicio ----#
os.system('cls')
print("Inicializando Servidor ...")
print("Servidor  está no ar!!")
receber_servidor()