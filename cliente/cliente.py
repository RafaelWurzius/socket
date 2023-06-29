import socket
import time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect(('localhost', 6969))
    print('Conectado!\n')

    operacao = str(input('Digite 1 para fazer upload de um arquivo ou 2 para fazer download de um arquivo:'))
    namefile = str(input('Nome do arquivo:'))

    cliente.send(operacao.encode())

    if operacao == "1":
        cliente.send(namefile.encode())
        with open(namefile, 'rb') as file:

            file_size = len(file.read())

            # Bytes enviados
            sent_bytes = 0

            # Reinicia a posição do arquivo
            file.seek(0)

            # Inicia a contagem do tempo
            start_time = time.time()


            for data in file.readlines():
                cliente.send(data)
                sent_bytes += len(data)
                tempo_decorrido = time.time() - start_time
                if (tempo_decorrido == 0):
                    taxa_transferencia = 0
                else:
                    taxa_transferencia = sent_bytes / tempo_decorrido
                porcentagem =  (sent_bytes / file_size) * 100
           
                print("\r" + 'Taxa de transferência: {:.2f} Bytes/s'.format(taxa_transferencia) + '\nPorcentagem transferida: {:.2f}%'.format(porcentagem) + "\033[F", end="", flush=True)


            print("\n\n" + f'{namefile} enviado!\n')

            #Encerra a conexão com o servidor
            cliente.close()
            print("Conexão encerrada!")
    elif operacao == "2":
            
        cliente.send(namefile.encode())

        # Recebe o tamanho do arquivo do servidor
        file_size = int(cliente.recv(1024).decode())

        # Recebe o conteúdo do arquivo do servidor
        received_bytes = 0

        with open(namefile, 'wb') as file:
            # Inicia a contagem do tempo
            start_time = time.time()

           # print("\n \n")
            while 1:
                data = cliente.recv(1024)
                if not data:    
                    break
                file.write(data)
                received_bytes += len(data)
                tempo_decorrido = time.time() - start_time
                if (tempo_decorrido == 0):
                    taxa_transferencia = 0
                else:
                    taxa_transferencia = received_bytes / tempo_decorrido
                porcentagem =  (received_bytes / file_size) * 100

                print("\r" + 'Taxa de transferência: {:.2f} Bytes/s'.format(taxa_transferencia) + '\nPorcentagem transferida: {:.2f}%'.format(porcentagem) + "\033[F", end="", flush=True)

        print("\n\n" + f'{namefile} recebido!')
        #Encerra a conexão com o servidor
        cliente.close()
        print("Conexão encerrada!")
