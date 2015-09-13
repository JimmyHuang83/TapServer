from managers.database_manager import db_Manager

__author__ = 'Mike'
class EquipQtyUpgradeInfo:
    def __init__(self,data):
        self.qty =data[0]
        self.costType = data[1]
        self.costValue = data[2]



class EquipmentQtyUpgradeTable :
    def __init__(self):
        self.tableData = {}

    def getEqpQualityUpgradeInfo(self,qty):
        return self.tableData[qty]

    def initTable(self):
        self.tableData.clear()
        tableName = "table_eqp_quality_upgrade"
        fields = "quality,costtype,costvalue"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            info = EquipQtyUpgradeInfo(oneData)
            self.tableData[info.qty] = info


equipmentQtyUpgradeTable = EquipmentQtyUpgradeTable()