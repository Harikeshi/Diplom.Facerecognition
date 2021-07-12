import cv2
from src.timeconverter import timeConvert
import src.converter

class Transaction:    
    def __init__(self, id_, start="", stop="", photo="", client_id = 0):
        self.__trans_id = id_
        self.__start_date_time = start 
        self.__stop_date_time = stop
        self.__photo = photo
        self.__client_id = client_id

        self.__tc = timeConvert()
        
    def get_client_id(self):
        return self.__client_id

    def get_start(self):
        return self.__start_date_time

    def get_stop(self):
        return self.__stop_date_time

    def get_photo_string(self):
        return self.__photo    

    def start(self):
        self.__start_date_time=self.__tc.time_now()

    def complete(self):
        self.__stop_date_time = self.__tc.time_now()

    def get_id(self):
        return self.__trans_id

    def set_client_id(self, value):
        self.__client_id = value

    def get_photo(self):
        return src.converter.base64_to_img(self.__photo)

    def save_photo(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)        
        self.__photo = src.converter.img_to_base64(img)
  
    def __more_of_start(self, time):
        if self.__tc.string_to_time(self.__start_date_time) > self.__tc.string_to_time(time):
            return True
        else: return False

    def __less_of_stop(self, time):
        if self.__tc.string_to_time(self.__stop_date_time) < self.__tc.string_to_time(time):
            return True            
        else: return False

    def compare_date(self,after,before):
        if self.__more_of_start(after) and self.__less_of_stop(before):
            return True
        else: return False

class Client:
    def __init__(self, client_id = 0, client_name = "", photo = []):
        self.__id = client_id
        self.__client_name = client_name
        self.__photo = photo        

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__client_name
    
    def get_photo(self):
        return self.__photo
        
    def set_id(self, value):
        self.__id = value

    def set_name(self, value):
        self.__client_name = value
    
    def set_photo(self, value):
        self.__photo = value