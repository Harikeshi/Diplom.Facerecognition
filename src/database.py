import json
from src.client import Client, Transaction

class ClientsRepository:
    
    __transactions = []
    __clients = []
    
    def __init__(self, path):
        self.__path = path
        self.__first_time = 0
        self.__last_time = 0
        self.__last_client_id = 0
        self.__last_transaction_id = 0
        self.__load()
        print("Database Loaded!")       

    def __load(self):              
        self.__load_clients()
        self.__load_transactions()
    
    def __load_transactions(self):
        transactions = {}
        try:
            with open(self.__path + "trans.json", "r") as f:                
                transactions = json.load(f)
        except:            
            with open(self.__path + "trans.json", "w+") as f:
                json.dump(transactions, f)

        if len(transactions) == 0:
            self.__last_transaction_id = 0
            return 0

        for key in transactions.keys():
            self.__transactions.append(Transaction(int(key), transactions[key][0], transactions[key][1], transactions[key][2], transactions[key][3]))            
            
        self.__last_transaction_id = self.__transactions[self.__transactions.__len__()-1].get_id()
        self.__first_time = self.__transactions[0].get_start()
        self.__last_time = self.__transactions[len(self.__transactions) - 1].get_stop()

    def __load_clients(self):
        clients = {}
        try:
            with open(self.__path + "clients.json", "r") as f:                
                clients = json.load(f)
        except:
            with open(self.__path + "clients.json", "w+") as f:
                json.dump(clients, f)

        if len(clients) == 0:
            self.__last_client_id = 0           
            return 0
        
        for key in clients.keys():
            self.__clients.append(Client(int(key), clients[key][0], clients[key][1]))

        self.__last_client_id = self.__clients[len(self.__clients)-1].get_id()
            
    # Добавить клиента в базу
    def add_client(self, client):        
        clients = {}
        with open(self.__path + "clients.json","r+") as f:
            clients = json.load(f)

        id = client.get_id()
        name = client.get_name()
        photo = client.get_photo()

        clients.update({id : [name, photo]})
        with open(self.__path + "clients.json", "w") as f:
            json.dump(clients, f)    

        self.__last_client_id = id
        self.__clients.append(client)

    # Добавить транзакцию в базу путем дописывания файла.    
    def add_transaction(self, trans):
        id = trans.get_id()
        date1 = trans.get_start()
        date2 = trans.get_stop()
        photo = trans.get_photo_string()
        client_id = trans.get_client_id()

        s = ', "' + str(id) + '": ["' + str(date1) + '", "' + str(date2) + '", "' + str(photo) + '", "' + str(client_id) + '"]}'
        
        if self.__last_transaction_id == 0:
            s = '"' + str(id) + '": ["' + str(date1) + '", "' + str(date2) + '", "' + str(photo) + '", "' + str(client_id) + '"]}'

        with open(self.__path + "trans.json","rb+") as write_file:
            write_file.seek(-1, 2)
            write_file.write(bytearray(s.encode()))

        self.__last_transaction_id += 1
        self.__transactions.append(trans)

    def get_client(self, id):        
        return self.__clients[id]
    
    def get_transaction(self, id):
        return self.__transactions[id]
    
    # отобрать клиентов по дате и времени
    def find_transactions_by_date(self, after, before):
        result = []
        # если больше after но меньше before
        for i in range(0,len(self.__transactions)):
            if self.__transactions[i].compare_date(after, before):
                result.append(self.__transactions[i])
        return result    
    
    def get_last_client_id(self):
        return self.__last_client_id

    def get_last_transaction_id(self):
        return self.__last_transaction_id

    def get_path(self):
        return self.__path
    
    def get_clients(self):
        return self.__clients
    
    def get_last_time(self):
        return self.__last_time
    
    def get_first_time(self):
        return self.__first_time