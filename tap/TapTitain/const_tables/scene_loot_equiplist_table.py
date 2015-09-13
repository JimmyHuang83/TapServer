from const_tables.itemDropListTable import equipListTable
from managers.database_manager import db_Manager

__author__ = 'Mike'

class SceneCostInfo:
    def __init__(self,data):
        self.sceneid = data[0]
        self.equiplistid = data[1]
        self.big_luck_num = data[2]
        self.small_luck_num = data[3]
        self.big_luck_id = data[4]
        self.small_luck_id = data[5]



class SceneLootEquipTable:
    def __init__(self):
        self.tableData = {}

    def getSceneConstInfo(self,sceneid):
        return self.tableData[sceneid]

    def initTable(self):
        self.tableData.clear()
        tableName = "table_scene_loot_equiplist"
        fields = "id,lootid,big_luck_num,small_luck_num,big_luck_id,small_luck_id"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            info = SceneCostInfo(oneData)
            self.tableData[info.sceneid] = info

    def verifyEquipment(self,sceneid,equipmentid,level,isLuck):
        equipmentlistid = self.tableData[sceneid].equiplistid
        itemList = equipListTable.getItemList(equipmentlistid)
        ret = itemList.verifyEquipment(equipmentid,level,isLuck)
        return  ret

sceneLootEquipTable = SceneLootEquipTable()