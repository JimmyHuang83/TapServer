from managers.database_manager import db_Manager

__author__ = 'Mike'

class EquipmentDeputBuffsTableManager:
    def __init__(self):
        self.tableData = []

    def initTable(self):
        self.tableData.clear()
        tableName = "table_eqp_deputbuffs"
        fields = "bufftype,rate"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            if oneData[1] > 0:
                self.tableData.append(oneData[0])


    def GetDeputBuffList(self):
        return self.tableData



eqpDeputBuffsTableManager = EquipmentDeputBuffsTableManager()