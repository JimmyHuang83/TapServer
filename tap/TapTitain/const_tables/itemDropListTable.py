from managers.database_manager import db_Manager

__author__ = 'Mike'
class ItemList:
    def __init__(self,data):
        self.equiplistid = data[0]
        self.noequip_pow = data[1]
        self.equip1_id = data[2]
        self.equip1_levelid = data[3]
        self.equip1_weight = data[4]
        self.equip2_id = data[5]
        self.equip2_levelid = data[6]
        self.equip2_weight = data[7]
        self.equip3_id = data[8]
        self.equip3_levelid = data[9]
        self.equip3_weight = data[10]
        self.equip4_id = data[11]
        self.equip4_levelid = data[12]
        self.equip4_pow = data[13]
        self.equip5_id = data[14]
        self.equip5_levelid = data[15]
        self.equip5_weight = data[16]
        self.equip6_id = data[17]
        self.equip6_levelid = data[18]
        self.equip6_weight = data[19]
        self.equip7_id = data[20]
        self.equip7_levelid = data[21]
        self.equip7_pow = data[22]

        self.equipmentids = []
        self.needLevel = []

        self.needLevel.append(self.equip1_levelid)
        self.needLevel.append(self.equip2_levelid)
        self.needLevel.append(self.equip3_levelid)
        self.needLevel.append(self.equip4_levelid)
        self.needLevel.append(self.equip5_levelid)
        self.needLevel.append(self.equip6_levelid)
        self.needLevel.append(self.equip7_levelid)

        self.equipmentids.append(self.equip1_id)
        self.equipmentids.append(self.equip2_id)
        self.equipmentids.append(self.equip3_id)
        self.equipmentids.append(self.equip4_id)
        self.equipmentids.append(self.equip5_id)
        self.equipmentids.append(self.equip6_id)
        self.equipmentids.append(self.equip7_id)

    def verifyEquipment(self,equipmentid,level,isLuck = False):
        return True

class EquipListTable:
    def __init__(self):
        self.tableData = {}

    def initTable(self):
        self.tableData.clear()
        tableName = "table_equip_drop_list"
        fields = "droplistid,noequip_pow," \
                 "equip1_id,equip1_levelid,equip1_pow," \
                 "equip2_id,equip2_levelid,equip2_pow," \
                 "equip3_id,equip3_levelid,equip3_pow," \
                 "equip4_id,equip4_levelid,equip4_pow," \
                 "equip5_id,equip5_levelid,equip5_pow," \
                 "equip6_id,equip6_levelid,equip6_pow,"\
                 "equip7_id,equip7_levelid,equip7_pow"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = ItemList(oneData)
            self.tableData[item.equiplistid] = item

    def getItemList(self,equiplistid):
        return self.tableData[equiplistid]

equipListTable = EquipListTable()
