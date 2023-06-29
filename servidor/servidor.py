import socket, sys, traceback;
from threading import Thread;

BLOCO = 1024;

def processar_requisicao(addr, conn):
    with conn:
        print('Conexão recebida: ', addr);
        operacao = conn.recv(BLOCO).decode()

        if operacao == "1":
            namefile = conn.recv(BLOCO).decode()

            with open(namefile, 'wb') as file:

                while 1:
                    data = conn.recv(BLOCO)
                    if not data:    
                        break
                    file.write(data)

            print(f'{namefile} recebido!')
            #Encerra a conexão com o cliente
            conn.close()
            print("Conexão encerrada:", addr)
        elif operacao == "2":
                
            namefile = conn.recv(BLOCO).decode()
            print('Nome do arquivo informado:', namefile)
            with open(namefile, 'rb') as file:
                file_size = len(file.read())

                # Envia o tamanho do arquivo para o cliente
                conn.send(str(file_size).encode())

                # Reinicia a posição do arquivo
                file.seek(0)

                #sent_bytes = 0
                for data in file.readlines():
                    conn.send(data)

                print('Arquivo enviado')
            #Encerra a conexão com o cliente
            conn.close()
            print("Conexão encerrada:", addr)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 6969));
        s.listen(100);
        while True:
            try:
                conn, addr = s.accept();
                t = Thread(target=processar_requisicao, args=(addr, conn, ));
                t.start();
            except KeyboardInterrupt:
                sys.exit(1);
            except:
                traceback.print_exc();

if __name__ == '__main__':
    main();