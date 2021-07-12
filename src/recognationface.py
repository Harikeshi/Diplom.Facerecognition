import dlib
import cv2
import os
from skimage import io
from scipy.spatial import distance

## сделать фото

class RecognationFace:

    # TODO изменить на новый работает быстрее 
    def __init__(self):
        self.__sp = dlib.shape_predictor(r'src/cnn/shape_predictor_68_face_landmarks.dat')
        self.__facerec = dlib.face_recognition_model_v1(r'src/cnn/dlib_face_recognition_resnet_model_v1.dat')
        self.__detector = dlib.get_frontal_face_detector()

    def __get_img(self, img_path):
        return io.imread(img_path)

    def get_descriptor(self, path):
        img = self.__get_img(path)
        shape = 0
        dets = self.__detector(img, 1)
        for k, d in enumerate(dets):
            shape = self.__sp(img, d) #!
        return self.__facerec.compute_face_descriptor(img, shape)

    def get_descriptor_path(self, path):       
        desc = self.get_descriptor(path)
        a = []
        for i in range(desc.shape[0]):
            a.append(desc[i])
        return a

    def get_descriptor_img(self, img):
        cv2.imwrite('a.jpg',img)       
        desc = self.get_descriptor('a.jpg')

        # TODO с картинкой не раотает
        os.remove('a.jpg')
        a = []
        for i in range(desc.shape[0]):
            a.append(desc[i])
        return a

    def compare(self, desc1, desc2):
        dis = distance.euclidean(desc1, desc2)
        if dis <= 0.60:
            print("Определено: " + str(dis))
            return True
        else:
            return False