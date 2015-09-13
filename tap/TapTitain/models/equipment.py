from const_tables.equipment_upgrade_table import equipmentUpgradeTable

__author__ = 'Mike'
import types
class EquipMent:
    def __init__(self,data):
        self.pos = 0
        self.equipmentid = 0
        self.equipment_quality = 1
        self.equipment_level = 0
        self.id = 0
        self.game_level = 1
        self.upgradeCost = 0
        self.bufList = []
        self.bufBaseList = []
        if data != None:
            if type(data) is type([]):
                self.initData(data)
            elif type(data) is type((0,0)):
                self.initData(data)
            elif type(data) is type({}):
                listData = self.dict2List(data)
                self.initData(listData)

    def dict2List(self,dictData):
        data = []
        pos = dictData.get('pos')
        id = dictData.get('id')
        equipmentid = dictData.get('equipmentid')
        equipment_quality = dictData.get('equipment_quality',1)
        equipment_level = dictData.get('equipment_level',0)
        gamelevel = dictData.get('game_level')
        upgradeCost = 0
        bufs = dictData.get('bufList')

        data.append(pos)
        data.append(equipmentid)
        data.append(equipment_quality)
        data.append(equipment_level)
        data.append(id)
        data.append(gamelevel)
        data.append(upgradeCost)

        for buf in bufs:
            bufType = buf.get('bufType')
            data.append(bufType)
            bufValue = buf.get('bufValue')
            data.append(bufValue)

        for buf in bufs:
            bufType = buf.get('bufType')
            data.append(bufType)
            bufValue = buf.get('bufValue')
            data.append(bufValue)

        return data

    def initData(self,data):
        self.pos = data[0]
        self.equipmentid = data[1]
        self.equipment_quality = data[2]
        self.equipment_level = data[3]
        self.id = data[4]
        self.game_level = data[5]
        self.upgradeCost = data[6]
        self.bufList = []
        self.bufBaseList = []
        for index in range(5):
            buf = EquipmentBuf(data[index *2 + 7] ,data[index *2 + 8] )
            self.bufList.append(buf)

        for index in range(5):
            buf = EquipmentBuf(data[index *2 + 17] ,data[index *2 + 18] )
            self.bufBaseList.append(buf)

    def upGradeToLevel(self,quality,level,buffs):
        tolevel30  = (quality - 1) * 10 + level
        nowLevel30 = (self.equipment_quality -1) * 10 + self.equipment_level
        distanceLevel = tolevel30 - nowLevel30

        if distanceLevel < 0:
            return  True
        elif distanceLevel == 0:
            self.equipment_quality = quality
            self.equipment_level = level
            return  True

        equipmentUpgradeConstInfo = equipmentUpgradeTable.getEuipmentLevelUpInfo(tolevel30)
        buffAdd = equipmentUpgradeConstInfo.buffAdd
        times = (1 + buffAdd)

        times += 0.5# rong cuo

        for buff in buffs:
            buffType = buff.get('bufType')
            buffToValue = buff.get('bufValue')
            nowValue = self.getBuffBaseValue(buffType)
            if nowValue == 0:
                return False
            if buffToValue > nowValue * times:
                return False

        for equipmentBuf in self.bufList:
            buffType = equipmentBuf.bufType
            newValue = equipmentBuf.bufValue
            for buff in buffs:
                if buff.get('bufType') == buffType:
                    newValue = buff.get('bufValue')
            equipmentBuf.bufValue = newValue
        self.equipment_quality = quality
        self.equipment_level = level
        return  True

    def getBuffValue(self,buffType):
        for equipmentBuf in self.bufList:
            if equipmentBuf.bufType == buffType:
                return  equipmentBuf.bufValue
        return 0

    def getBuffBaseValue(self,buffType):
        for equipmentBuf in self.bufBaseList:
            if equipmentBuf.bufType == buffType:
                return  equipmentBuf.bufValue
        return 0
class EquipmentBuf:
    def __init__(self,type,value):
        self.bufType = type
        self.bufValue = value

