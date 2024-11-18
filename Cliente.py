import socket
import threading
import os

os.system('cls')

print(">---- Menu de função ----<")
print(">> /privado")
print(">> /Sair")
print(">------------------------<")
nickname = input("Inserá seu apelido: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

def receber_cliente():
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            if mensagem == 'Apelido':
                cliente.send(nickname.encode())
            else:
                print(mensagem)

                escrever_cliente_thread = threading.Thread(target=escrever_cliente)
                escrever_cliente_thread.start()

        except:
            print("Erro! Desconectando...")
            cliente.close()
            break

def escrever_cliente():
    while True:
        mensagem = '{}: {}'.format(nickname, input(''))

        if "/sair" in mensagem:
            print("Saindo do chat...")
            cliente.send("/sair".encode()) 
            cliente.close()
            break 

        cliente.send(mensagem.encode())

os.system('cls')

receber_cliente()