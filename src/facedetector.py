# -*- coding: utf-8 -*-
import cv2

class FaceDetector:

    __client_name = ""
    
    def __init__(self, camera_id):        
        # TODO 1 Выделить в кадр 
        self.__cap = cv2.VideoCapture(camera_id)  # 1
        self.__face_cascade = cv2.CascadeClassifier(r'src/haarcascade_frontalface_alt2.xml')
        
        self.__x, self.__y, self.__w, self.__h = 0, 0, 0, 0
        
        self.__img = []
        self.__frame = []
        self.__faces = []
        self.__gray = 0
    # Вычисление лиц, возвращает (faces, frame) TODO в отдельный класс по идее
    def calculate_length_faces(self):
        ret, self.__frame = self.__cap.read() 
        self.__gray = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2GRAY)

        self.__faces = self.__face_cascade.detectMultiScale(self.__gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        return len(self.__faces)
    
    def calculate_max_rectangle(self, length):
        # length Длина прямоугольника, можно вынести в конструктор thread          
        self.__w, self.__h, self.__x, self.__y = 0, 0, 0, 0
        flag = False
        for (x, y, w, h) in self.__faces:
            if self.__w < w and w >= length:
                self.__w, self.__h, self.__x, self.__y, flag = w, h, x, y, True
            else:
                # Добавляеет красные прямоугольники, если не клиент
                cv2.rectangle(self.__frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
            self.__img = self.__gray[self.__y:self.__y + self.__h, self.__x:self.__x + self.__w]                                   
        return flag

    def add_client_rect(self, transaction):        
        font = cv2.FONT_HERSHEY_TRIPLEX # FONT_HERSHEY_DUPLEX
        cv2.rectangle(self.__frame, (self.__x, self.__y), (self.__x + self.__w, self.__y + self.__h), (0, 255, 0), 3)
        cv2.putText(self.__frame, "Transaction " + str(transaction) +" "+ self.__client_name, (self.__x + 6, self.__y - 6),font, 0.5, (255, 0, 0), 1)
   
    def add_red_rect(self):
        cv2.rectangle(self.__frame, (self.__x, self.__y), (self.__x + self.__w, self.__y + self.__h), (0, 0, 255), 3)

    def add_blue_rect(self):
        cv2.rectangle(self.__frame, (self.__x, self.__y), (self.__x + self.__w, self.__y + self.__h), (255, 0, 0), 3)

    def print_R(self):        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.__frame, "R", (50, 100), font, 2, (0, 0, 255), 3)
    
    def get_frame(self):
        return self.__frame

    def set_client_name(self, value):
        self.__client_name = value

    def get_img(self):
        return self.__img

    def cam_release(self):
        self.__cap.release()