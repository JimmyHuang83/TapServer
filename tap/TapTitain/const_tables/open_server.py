from managers.database_manager import db_Manager

__author__ = 'Mike'
class OpenServer:
    def __init__(self,data):
        self.id = data[0]
        self.type = data[1]
        self.condition = data[2]
        self.item1 = int(data[3])
        self.name1 = data[4]
        self.num1 = data[5]
        self.item2 = data[6]
        self.name2 = data[7]
        self.num2 =data[8]
        self.item3 = data[9]
        self.name3 = data[10]
        self.num3 = data[11]

class OpenServerTable:
    def __init__(self):
        self.tables = {}


    def initData(self):
        self.tables.clear()
        tableName = "table_open_server"
        fields = "`id`, `type`, `condition`, `item1`, `name1`, `num1`, `item2`, `name2`, `num2`, `item3`, `name3`, `num3`"
        data = db_Manager.selectDataFromTable(tableName,fields)
        for openserver in data:
            os = OpenServer(openserver)
            if not os.type in self.tables:
                self.tables[os.type] = {}
            self.tables[os.type][os.id] = os

    def getOpeventServer(self,typeId,id):
        try:
            return  self.tables[typeId][id]
        except:
            return None

openServerTable = OpenServerTable()