from managers.database_manager import db_Manager

__author__ = 'Mike'
class EquipmentSetInfo:
    def __init__(self,data):
        self.id = data[0]
        self.partCount = data[1]
        self.equipment1 = data[2]
        self.equipment2 = data[3]
        self.equipment3 = data[4]
        self.equipment4 = data[5]
        self.equipment5 = data[6]
        self.equipment6 = data[7]
        self.effType1 = data[8]
        self.effValue1 = data[9]
        self.effType2  = data[10]
        self.effValue2 = data[11]
        self.effType3 = data[12]
        self.effvalue3 = data[13]
        self.effType4 = data[14]
        self.effValue4 = data[15]
        self.effType5 = data[16]
        self.effValue5 = data[17]
        self.effType6 = data[18]
        self.effValue6 = data[19]
        self.skill1 = data[20]
        self.skill2 = data[21]
        self.greenRate =  float(data[22])
        self.bluerate = float(data[23])
        self.violetRate = float(data[24])
        self.goldenRate = float(data[25])

        self.parts = []
        self.parts.append(self.equipment1)
        self.parts.append(self.equipment2)
        self.parts.append(self.equipment3)
        self.parts.append(self.equipment4)
        self.parts.append(self.equipment5)
        self.parts.append(self.equipment6)

        self.buffTypes = []
        self.buffValues = []
        self.buffTypes.append(self.effType1)
        self.buffTypes.append(self.effType2)
        self.buffTypes.append(self.effType3)
        self.buffTypes.append(self.effType4)
        self.buffTypes.append(self.effType5)
        self.buffTypes.append(self.effType6)

        self.buffValues.append(self.effValue1)
        self.buffValues.append(self.effValue2)
        self.buffValues.append(self.effvalue3)
        self.buffValues.append(self.effValue4)
        self.buffValues.append(self.effValue5)
        self.buffValues.append(self.effValue6)

        self.rates = []
        self.rates.append(self.greenRate)
        self.rates.append(self.bluerate)
        self.rates.append(self.violetRate)
        self.rates.append(self.goldenRate)

class EquipmentSetTable():
    def __init__(self):
        self.tableData = {}


    def initTable(self):
        self.tableData.clear()
        tableName = "table_set_equipment"
        fields = "id,partcount,equip1,equip2,equip3," \
                 "equip4,equip5,equip6,efftype1,effvalue1," \
                 "efftype2,effvalue2,efftype3,effvalue3," \
                 "efftype4,effvalue4,efftype5,effvalue5,efftype6,effvalue6," \
                 "skill1," \
                 "skill2,bluerate,greenrate,violetrate,goldenrate"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = EquipmentSetInfo(oneData)
            self.tableData[item.id] = item

    def getSetInfo(self,setID):
        return self.tableData[setID]

    def getEquipmentSetBuff(self,equipments):
        buffs = {}
        for _,equipmentSetInfo in self.tableData.items():
            partCount = 0
            minQuality = 1
            for pos,equipMent in equipments.items():
                if pos == 10:
                    continue

                equipID = equipMent.equipmentid
                if equipID in equipmentSetInfo.parts:
                    partCount += 1
                    minQuality = min(minQuality,equipMent.equipment_quality)
            if partCount == 0:
                continue
            if partCount > 6:
                partCount = 6
            for index in range(partCount):
                buffType = equipmentSetInfo.buffTypes[index]
                if buffType != -1:
                    value = buffs.get(buffType,0)
                    buffs[buffType] =int(value + equipmentSetInfo.buffValues[index] * equipmentSetInfo.rates[minQuality])

        print("equipment set buffs : %s" %str(buffs))
        return  buffs


equipmentSetTable = EquipmentSetTable()