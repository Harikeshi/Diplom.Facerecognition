import cv2
from numpy import ndarray
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from src.client import Transaction
from src.facedetector import *
from src.facecompare import *
from src.lbp import *
from src.database import *
from src.timeconverter import *

class ManageStream(QThread):
    
    # Сигналы
    sendClients = pyqtSignal(list)
    sendFrameToForm = pyqtSignal(ndarray)
    sendClientPhoto = pyqtSignal(ndarray)
    sendTransactions = pyqtSignal(list)

    commandToForm = pyqtSignal(str) # Transaction to form

    __min_rect = 150 # минимальный размер окна с лицом
    __face_tick = 90
    __some_tick = 12
    __client_on = False
    
    # Создание потока
    def __init__(self, camera):
        QThread.__init__(self)
    
        self.__transaction = 0 # Объект транзакция для передачи на форму
        self.__running = True
        self.__working = False     

        self.__noface_tick = 0
        self.__some_time = 0
        self.__img =[]

        self.__cam = FaceDetector(camera)
        self.__tt = timeConvert()
        self.__fc = FaceCompare()
        self.__lbp = LBP()
        self.__database = ClientsRepository(r"db/")

    def run(self):               
        self.sendClients.emit(self.__database.get_clients())
        print("Manage Thread Started!")
        h1 = []
        # Запускаем цикл при запуске программы
        while self.__running:
            # Рассчитываем лица
            # Вычисление и возврат длину faces
            length = self.__cam.calculate_length_faces()                    
            # Если программа запущена в работу
            if self.__working:
                if self.__noface_tick <= self.__face_tick:                                    
                    flag = self.__cam.calculate_max_rectangle(self.__min_rect) # Находим максимальный квадрат больший эталона и печатаем красные прямоугольники                
                    # Если лица не обнаружены или не обнаружено лицо нужного размера                
                    if length == 0 or flag == False:
                        # Если клиент был до этого, то возможно он ушел или не распозналось лицо
                        if self.__client_on == True:
                            # Инкрементируем счетчик пустых или ложных кадров.
                            self.__noface_tick += 1 
                  

                    # Если лица обнаружены на кадре
                    elif length > 0:
                        # Если ранее клиента не было               
                        if self.__client_on == False:                    
                            # Отрисовать прямоугольник клиента и надпись (синим)
                            self.__cam.add_blue_rect()                      
                            # Сохраняем не первый кадр
                            if self.__some_time < self.__some_tick:
                                self.__img = self.__cam.get_img()                            
                                self.__some_time += 1
                                id = self.__find_client_in_database(h1) #1 deleted
                                if self.__some_time == self.__some_tick - 1:
                                    self.__fc.calculate_from_img(self.__img) # но из массива фотографий или решающей фотографии
                                    #h1 = self.__fc.get_historgams()                                    
                                    h1 = self.__lbp.calculate(self.__img, 1, 8, 8)
                                    # Поиск клиента по базе данных
                                    id = self.__find_client_in_database(h1)
                                    self.__client_on = True
                                    self.__transaction_start(id)                                      
                        # Если клиент уже был ранее
                        elif self.__client_on == True:                            
                            ####                                    
                            #if not self.__fc.compare(h1, self.__cam.get_img()):
                            if not self.__lbp.Compare(h1, self.__cam.get_img(), 1, 8, 8):           
                                self.__noface_tick += 5
                            
                                self.__cam.add_red_rect()                                
                            # Если эта фотография совпадает с клиентом
                            else:
                                # TODO Отправляем клиента, но на форме проверка есть ли время останова и вывещиваем на форме фото.                            
                                # Отрисовать прямоугольник клиента и надпись                            
                                self.__cam.add_client_rect(self.__database.get_last_transaction_id() + 1)
                                self.__noface_tick = 0
                    # Добавить печать буквы [R]
                    self.__cam.print_R()
                    # Возвращаем frame
                    self.pictToForm(self.__cam.get_frame())               
                else:
                    self.__transaction_complete()
                    self.__cancel_client_name()                          
            else:
                    # Возвращаем frame
                self.pictToForm(self.__cam.get_frame())
        self.__cam.release()


    def get_running(self):
        return self.__running
    
    def set_running(self, value):
        self.__running == value

    # Пересылка Кадра на форму
    def pictToForm(self, frame):
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        
        self.sendFrameToForm.emit(rgbImage)
    
    @pyqtSlot(str)
    def get_new_client(self, name):
        client = Client()
        img = self.__lbp.get_face(self.__cam.get_frame())
        h = self.__lbp.calculate(img, 1, 8, 8)
        client.set_photo(h)
        client.set_name(name)
        client.set_id(self.__database.get_last_client_id() + 1)
        self.__database.add_client(client)
        print("Клиент добавлен.")

    @pyqtSlot(list)
    def get_date_list(self, lst):
        transactions = self.__database.find_transactions_by_date(lst[0], lst[1])
        self.sendTransactions.emit(transactions)

    # Пересылка фотографии на форму после сохранения
    def send_photo_by_save(self, frame):
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        self.sendClientPhoto.emit(rgbImage)

    def __transaction_start(self, id):
        # Инициализируем объект транзации сохраняем фото в виде base64 время начала
        self.__transaction = Transaction(self.__database.get_last_transaction_id() + 1)
        self.__transaction.set_client_id(id)
        self.__transaction.save_photo(self.__img)
        self.__transaction.start()
        # Отсылаем фото на форму
        self.send_photo_by_save(self.__img)                                 
        # Отправляем начальный объект на форму
        self.commandToForm.emit("["+ str(self.__tt.time_now()) +"]Transaction  #"+str(self.__transaction.get_id())+" for client #"+ str(self.__transaction.get_client_id())+" started at "+ str(self.__transaction.get_start()))                                                              

    def __transaction_complete(self):
        self.__noface_tick = 0
        self.__client_on = False
        self.__some_time = 0
        self.__transaction.complete()
        self.commandToForm.emit("["+ str(self.__tt.time_now()) +"]Transaction  #"+str(self.__transaction.get_id())+" for client #"+ str(self.__transaction.get_client_id())+" complete at "+ str(self.__transaction.get_stop()))                            
        self.__database.add_transaction(self.__transaction)  

    def __find_client_in_database(self, h1):
        clients = self.__database.get_clients()
        id = 0
        for i in range(0, len(clients)):
            if self.__lbp.CompareHistorgamms(h1, clients[i].get_photo(),30):
                id = clients[i].get_id()  
                self.client_name_to_frame(clients[i].get_name())
            else: self.client_name_to_frame(" ")
        return id

    def __cancel_client_name(self):
        self.client_name_to_frame(" ")


    def client_name_to_frame(self, name):
        self.__cam.set_client_name(name)

    def get_client(self):
        return self.__transaction
    
    def complete_and_get_client(self):
        self.__transaction.complete()
        return self.__transaction

    # Методы для приостановки вычислений в потоке
    def start_work(self):
        self.__working = True
    
    def stop_work(self):
        self.__working = False