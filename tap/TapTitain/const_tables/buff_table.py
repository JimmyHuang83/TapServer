from managers.database_manager import db_Manager

__author__ = 'Mike'
class Buff:
    def __init__(self,data):
        self.bufftype = data[0]
        self.caltype = data[1] #calculate type
        self.discount = data[2]
        self.levelModify = float(data[3])
        self.baseValue = data[4]
class BuffTable:
    def __init__(self):
        self.tableData = {}

    def initTable(self):
        self.tableData.clear()
        tableName = "table_buffs"
        fields = "bufftype,caltype,discount,levelmodifiy,buffbasevalue"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = Buff(oneData)
            self.tableData[item.bufftype] = item

    def getBuffConstInfo(self, buffType):
        return  self.tableData[buffType]


buffTable = BuffTable()