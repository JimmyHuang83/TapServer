from managers.database_manager import db_Manager

__author__ = 'Mike'



class GloableBase:
    def __init__(self):
        self.tableData = {}

    def initTable(self):
        self.tableData.clear()
        tableName = "table_global_base"
        fields = "id,value"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            self.tableData[oneData[0]] = oneData[1]


    def getValue(self,key):
        return self.tableData.get(key,0)


gloabalBase = GloableBase()