from managers.database_manager import db_Manager
from managers.player_data_manager import playerDataManager
from models.equipment import EquipmentBuf, EquipMent

__author__ = 'Mike'


class PvpPlayerInfoInRanking:
    def __init__(self,data):
        self.player_id = data[0]
        self.name = data[1]
        self.game_level = data[2]
        self.avatorid = data[3]
        self.rankNum = 0
        self.defenseBuffs = []
        self.playerLevel = 0
        self.equipments = {}

        self.loadDefenseBuffs()
        self.loadPlayerLevel()


    def loadDefenseBuffs(self):
        playerInfo = playerDataManager.getPlayerByPlayerid(self.player_id)
        if playerInfo == None:
            tableName = "player_pvp_buffs"
            fields = "buffstr"
            conditon = "playerid = %s" % self.player_id
            data = db_Manager.selectDataFromTable(tableName,fields,conditon)
            if len(data) == 0:
                self.defenseBuffs = []
            else:
                self.defenseBuffs.clear()
                buffStr = data[0][0]
                buffStrArr = buffStr.split(',')

                self.defenseBuffs = []
                for index in range(24):
                    if index < len(buffStrArr):
                        value = int(buffStrArr[index])
                        buff = EquipmentBuf(index + 1, value)
                        self.defenseBuffs.append(buff)
            self.loadPlayerLevel()
            self.loadEquipments()
        else:
            cacheBuff = playerInfo.pvpBuffs
            self.playerLevel = playerInfo.getSkillInfo(0).skillLevel
            for index in range(40):
                if index < len(cacheBuff):
                    value = cacheBuff[index]
                    buff = EquipmentBuf(index + 1, value)
                    if value > 0:
                        self.defenseBuffs.append(buff)
            self.equipments = playerInfo.equipments

    def loadPlayerLevel(self):
        tableName = "player_skill"
        fields = "level"
        conditon = "skill_id = 0 and player_id = '%s'" % self.player_id
        data = db_Manager.selectDataFromTable(tableName,fields,conditon)
        self.playerLevel = data[0][0]


    def loadEquipments(self):
        tableName = "player_equip"
        fields = "pos,equipmentid,equipment_quality,equipment_level,id,game_level,upgrade_cost," \
                 "buftype1,bufvalue1,buftype2,bufvalue2,buftype3,bufvalue3,buftype4,bufvalue4,buftype5,bufvalue5," \
                 "bufbasetype1,bufbasevalue1,bufbasetype2,bufbasevalue2,bufbasetype3,bufbasevalue3,bufbasetype4,bufbasevalue4,bufbasetype5,bufbasevalue5"
        conditon = "player_id = %s" % self.player_id
        data = db_Manager.selectDataFromTable(tableName,fields,conditon)

        for equipmentData in data:
            if equipmentData[1] == -1:
                continue
            equipment = EquipMent(data = equipmentData)
            equipPos = int(equipmentData[0])
            self.equipments[equipPos] = equipment












