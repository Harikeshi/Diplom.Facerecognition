from datetime import *

class timeConvert:
    def time_to_string(self, date_time):
        return date_time.strftime('%d/%m/%y %H:%M:%S')
    
    def string_to_time(self,date_time_string):        
        return datetime.strptime(date_time_string, '%d/%m/%y %H:%M:%S')
    
    def time_now(self):
        today = datetime.today()
        return today.strftime('%d/%m/%y %H:%M:%S')