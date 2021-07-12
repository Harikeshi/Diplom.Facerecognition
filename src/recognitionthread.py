from PyQt5 import QtCore
from src.client import *
import src.recognationface
from numpy import ndarray
from database import *

# RecognitionThread

class RecognitionThread(QtCore.QThread):
    
    # TODO Объединить классы клентов в один файл и подгружать нужного клиента.
    # TODO Workers?
    __rd = src.recognationface.RecognationFace()  

    # TODO Фабрика сигналов
    clientDescToForm = QtCore.pyqtSignal(list)
    clientStringToStream = QtCore.pyqtSignal(str)
    clientIdToForm = QtCore.pyqtSignal(int)
    getClients = QtCore.pyqtSignal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.__current_desc = 0

    def run(self):
        self.exec_() # Запускаем цикл обработки сигналов        

    @QtCore.pyqtSlot(ndarray)
    def calculate(self, frame):        
        desc = self.__rd.get_descriptor_img(frame)
        self.clientDescToForm.emit(desc)
    
    @QtCore.pyqtSlot(ndarray)
    def calculate_and_save(self, frame):        
        desc = self.__rd.get_descriptor_img(frame)
        self.__current_desc = desc
        self.getClients.emit(id)
    
    @QtCore.pyqtSlot(list)
    def get_clients(self, clients):        
        # сравнить и результат выслать
        name = "Unknow client."
        id = 0 # -1
        try:
            for i in clients:
                if self.__rd.compare(i.get_photo(), self.__current_desc):
                    name = i.get_name()
                    id = i.get_id()
                    break
            self.clientStringToStream.emit(name)
            self.clientIdToForm.emit(id)
        except:
            print("[Error] Не распознано лицо на изображении.")
            self.clientStringToStream.emit(name)
            self.clientIdToForm.emit(id)
    