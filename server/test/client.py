import socket
import time

TCP_IP = 'localhost'
TCP_PORT = 8889
BUFFER_SIZE = 1024

path = '1.jpg'

# Первый запрос Отправки фото второй для получения информации.
def send_photo(path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Отсылает фото ждет ответа строку.
        s.connect((TCP_IP, TCP_PORT))

        with open(path, 'rb') as f:
            while True:
                data = f.read(100*1024)
                while data:
                    s.send(data)
                    #print('data=%s', (data))
                    #data = f.read(BUFFER_SIZE)
                    if not data:          
                        break
            # получить ответ
                break
        d = str(s.recv(1024))
        print(d)
    # s.close()
                
    print('connection closed')

send_photo(path)
    

        

