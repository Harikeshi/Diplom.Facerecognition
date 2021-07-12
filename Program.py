import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSlot
from gui.ui_Detector import *
from src.managestream import *

class App(QtWidgets.QMainWindow):

    __camera_id = 0
    __transaction_on = False

    sendNewClient = pyqtSignal(str)#str
    sendDateList = pyqtSignal(list)
    
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)       
       
        # Buttons
        self.ui.startButton.clicked.connect(self.on_clicked_start)
        self.ui.stopButton.clicked.connect(self.on_clicked_stop)
        self.ui.makePhotoButton.clicked.connect(self.on_clicked_make_photo_button)
        self.ui.dateFindButton.clicked.connect(self.on_clicked_find_button)

        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+A"), self)
        self.shortcut.activated.connect(self.on_clicked_start)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(self.on_clicked_stop)       
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"),self)
        self.shortcut.activated.connect(self.space_button_push)

        # Actions
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.onAbout)
        self.ui.actionStart.triggered.connect(self.on_clicked_start)
        self.ui.actionStop.triggered.connect(self.on_clicked_stop)
        self.ui.actionProperties.triggered.connect(self.add_client_from_photo)
        
        # Threads
        self.th = ManageStream(self.__camera_id)       
        self.th.sendFrameToForm.connect(self.set_image)
        self.th.commandToForm.connect(self.command_event)
        self.th.sendClients.connect(self.load_clients)
        self.th.sendClientPhoto.connect(self.get_client_photo)
        self.th.sendTransactions.connect(self.get_transactions)

        self.sendNewClient.connect(self.th.get_new_client)
        self.sendDateList.connect(self.th.get_date_list)
        self.th.start(6)
        print("Full System Loaded!")

    def space_button_push(self):
        if self.th.get_running() == True:
            self.th.set_running(False)
            print(self.th.get_running())
        if self.th.get_running() == False:
            self.th.set_running(True)
            print("start")
 
    # Сигналы    
    @pyqtSlot(ndarray)
    def set_image(self, image):      
        self.__img = image
        p = self.jpg_to_pixmap(image, 700,540)
        self.ui.videoSteam.setPixmap(QtGui.QPixmap.fromImage(p))

    @QtCore.pyqtSlot(list)
    def load_clients(self, clients): 
        self.ui.ourClientWidget.clear()       
        self.ui.ourClientWidget.setRowCount(len(clients))

        for i in range(0,len(clients)):
            label0 = QtWidgets.QLabel(str(clients[i].get_id()))
            label0.setAlignment(Qt.AlignHCenter)
            self.ui.ourClientWidget.setCellWidget(i, 0, label0)            
            
            label2 = QtWidgets.QLabel(clients[i].get_name())
            label2.setAlignment(Qt.AlignHCenter)
            self.ui.ourClientWidget.setCellWidget(i, 2, label2)

    @QtCore.pyqtSlot(str) 
    def command_event(self, command):
        # Вывести сообщения, здесь же команда на банкомат
        self.ui.textBrowser.append(command)        
        if self.__transaction_on:
            self.__transaction_on = False            
            print("ATM TRANSACTION CLOSE!")
        else:
            print("ATM TRANSACTION OPEN!")
            self.__transaction_on = True
        
    @pyqtSlot(ndarray)
    def get_client_photo(self, img):
        self.ui.label_3.setPixmap(QtGui.QPixmap.fromImage(self.jpg_to_pixmap(img,200,100)))

    @pyqtSlot(list)
    def get_transactions(self, transactions):
        self.ui.findResult.setRowCount(len(transactions))
        self.ui.findResult.setColumnCount(5)

        for i in range(0, len(transactions)):
            label0 = QtWidgets.QLabel(str(transactions[i].get_id()))
            label0.setAlignment(Qt.AlignHCenter)
            self.ui.findResult.setCellWidget(i,0,label0)            
            label1 = QtWidgets.QLabel("")
            label1.setAlignment(Qt.AlignHCenter)
            p=QtGui.QPixmap.fromImage(self.jpg_to_pixmap(transactions[i].get_photo(),150,75))
            label1.setPixmap(p)               
                
            self.ui.findResult.setCellWidget(i, 1, label1)                                
            label2 = QtWidgets.QLabel(transactions[i].get_start())
            label2.setAlignment(Qt.AlignHCenter)
                
            self.ui.findResult.setCellWidget(i,2,label2)
            label3 = QtWidgets.QLabel(transactions[i].get_stop())
            label3.setAlignment(Qt.AlignHCenter)

            self.ui.findResult.setCellWidget(i,3,label3)
            label4 = QtWidgets.QLabel(str(transactions[i].get_client_id()))
            label4.setAlignment(Qt.AlignHCenter)
        
    def on_clicked_make_photo_button(self):      
        try:        
            name, ok = QtWidgets.QInputDialog.getText(window, "Фотография нового клиента", "Введите имя и фамилию клиента", text="")
            if ok:           
                self.ui.textBrowser.setText("Client #" + " - " + name + " saved, OK!")                                
        except:
            self.ErrorMessage("Неверный ввод", "Проверьте ввод, поля не должны быть пустыми.")
        self.sendNewClient.emit(name)           

    def on_clicked_find_button(self):
        lst = [self.ui.dateTimeFrom.text(), self.ui.dateTimeTo.text()]        
        try:
            self.sendDateList.emit(lst)
        except ValueError as e:
            self.ErrorMessage("Ошибка ввода даты","Неверный формат даты и времени.")

    def add_client_from_photo(self):
        # перевести на форму
        pass

    def on_clicked_start(self):
        self.th.start_work()

    def on_clicked_stop(self):                
        self.th.stop_work()

    def onAbout(self):
        QtWidgets.QMessageBox.about(window,'О программе', 'Программа детектор')
        
    def ErrorMessage(self, title, msg):
        QtWidgets.QMessageBox.critical(window, title, msg, defaultButton=QtWidgets.QMessageBox.Ok)

    def jpg_to_pixmap(self, image, height, width):        
        h, w, ch = image.shape
        bytesPerLine = ch * w
        convertToQtFormat = QtGui.QImage(image.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        p = convertToQtFormat.scaled(height, width , Qt.KeepAspectRatio)            
        return p

# window.btnQuit.clicked.connect(app.quit)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())