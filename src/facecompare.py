import numpy as np
import cv2

# В работе данный класс применяется для сравнения двух лиц

class FaceCompare:

    def get_face(path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
        faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)

        for x, y, h, w in faces:
            img = gray[y:y + h, x: x + w]

        return img

    def __init__(self):
        self.__recognizer = cv2.face.LBPHFaceRecognizer_create()

    def get_historgams(self):
        return(self.__recognizer.getHistograms()[0][0])

    # высчитываем дескриптор пока будет с одной картинкой
    def calculate_from_array(self, imgs):
        pass

    def calculate_from_img(self, face_img):
        x_train =[]
        x_train.append(face_img)
        self.__recognizer.train(x_train,np.array(0))
    
    def __xi_square(self, h1, h2):
        result = 0
        l = len(h1)
        for i in range(0, l):
            if (h1[i] + h2[i]) == 0:
                continue
            result += (h1[i]-h2[i])*(h1[i]-h2[i])/(h1[i]+h2[i])            
        return result;

    def compare(self, h1, img):
        self.calculate_from_img(img)
        h2 = self.get_historgams()
        
        res = self.__xi_square(h1, h2)        
        if res <= 20:
            print(res)
            return True
        else:
            print(res)
            return False