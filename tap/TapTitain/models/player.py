#coding=utf-8
import base64
import datetime
import json
import time
from const_tables.buff_table import buffTable
from const_tables.const_value import ConstValue
from const_tables.equipment_set import equipmentSetTable
from const_tables.equipment_upgrade_table import equipmentUpgradeTable
from const_tables.gloabl_base_table import gloabalBase
from const_tables.hero_skill_table import heroSkillTableManager
from const_tables.hero_table import heroTable
from const_tables.hero_unlock import heroUnlockTable
from const_tables.level_table import levelTable
from const_tables.scene_loot_equiplist_table import sceneLootEquipTable
from const_tables.table_eqp_quality_upgrade import equipmentQtyUpgradeTable
from const_tables.upgrade_hero_table import heroUpgradeTable
from const_tables.upgrade_parter_table import partnerUpgradeTable
from managers.database_manager import db_Manager
from models.equipment import EquipMent
from models.game_enum import ResourceType
from models.game_tools import GameTools
from models.hero_skill import HeroSkillData
from models.message import ErrorCode
from models.offline_cash import OfflineCash
from models.partner import Partner
from models.player_scene_model import PlayerSceneInfo

__author__ = 'Mike'
class PlayerInfo:
    def __init__(self,data):
        self.player_id = data[0]                    # ID
        self.name = data[1]                         # 昵称
        self.pvp_medal = int(data[2])               #
        self.gems = int(data[3])                    # 钻石
        self.revial = int(data[4])                  # 复活币
        self.cash = int(data[5])                    # 金币
        self.game_level = data[6]                   # 游戏关卡
        self.game_wave = data[7]                    # 游戏波数
        self.change_date = data[8]                  # 修改日期
        self.chanllenge_num = data[9]               # 剩余挑战次数
        self.avatorid = data[10]                    #
        self.lootEquipLevel = data[11]
        self.isBrush = data[12]

        self.offlineCash = 0
        if data[13] == None or data[13] == '':
            self.last_cmd_time = GameTools.getDateTimeNowString()
        else:
            self.last_cmd_time = data[13]

        self.random_reward_num = data[14]
        self.random_rweard_date= data[15]
        self.last_timed_reward_datetime = data[16]
        self.last_timed_reward_ranknum = data[17]
        self.last_challenge_datetime = data[18]
        self.buy_del_challenge_cd_num = data[19]
        self.daily_datetime = data[20]
        self.add_chanllenge_num = data[21]
        self.awake_spell_num = data[22]
        self.last_free_draw_datetime = data[23]
        self.recharge_total_num = data[24]
        self.recharge_get_gifts_status = json.loads(data[25])
        self.last_login_date = "%s" %data[26]
        self.login_num = data[27]
        self.login_get_gifts_status = json.loads(data[28])

        self.udid = data[29]

        self.server_date_time = GameTools.getDateTimeNowString()

        self.token = self.getToken(self.player_id)

        self.waveStartTime = GameTools.getDateTimeNowString()

        self.scenesInfo = {}

        self.connect_id = ''

        #equipment
        self.equipments = {}# pos --> equipment
        self.skills = []
        self.partners = []
        self.selected_partners = []
        self.buffsValue = {} # buf count

        self.loadEqument()
        self.loadSkills()
        self.loadPartners()
        self.loadSelectPartners()
        self.loadSceneInfo()
        self.refreshTimeData()
        self.pvpBuffs = []
        self.loadRankTimedRewardInfo()
        self.loadPvpBuffs()
        self.updateDailyData()

    def updateDailyData(self):
        dateTimeNow = GameTools.getDatetimeNow()
        lastDateTimeNow = GameTools.string2datetime(self.daily_datetime)
        if dateTimeNow.year != lastDateTimeNow.year or dateTimeNow.month != lastDateTimeNow.month or dateTimeNow.day != lastDateTimeNow.day:
            self.daily_datetime = GameTools.getDateTimeNowString()

            self.chanllenge_num = int(gloabalBase.getValue('daily_challenge_num'))
            self.buy_del_challenge_cd_num = 0
            self.add_chanllenge_num = 0
            self.random_reward_num = 0

    def loadRankTimedRewardInfo(self):
        tableName = "player_base_info"
        fields = "lastTimedRewardDatetime,last_timed_reward_ranknum"
        conditon = "playerid = %s" % self.player_id
        data = db_Manager.selectDataFromTable(tableName,fields,conditon)
        if len(data) > 0:
            self.last_timed_reward_datetime = data[0][0]
            self.last_timed_reward_ranknum = data[0][1]

    def loadPvpBuffs(self):
        tableName = "player_pvp_buffs"
        fields = "buffstr"
        conditon = "playerid = %s" % self.player_id
        data = db_Manager.selectDataFromTable(tableName,fields,conditon)
        maxBuffID = 40
        if len(data) == 0:
            self.pvpBuffs = []
            for index in range(maxBuffID):
                self.pvpBuffs.append(0)
            self.insertPvpBuffs()
        else:
            self.pvpBuffs.clear()
            buffStr = data[0][0]
            buffStrArr = buffStr.split(',')

            self.pvpBuffs = []
            for index in range(maxBuffID):
                if index < len(buffStrArr):
                    value = int(buffStrArr[index])
                    self.pvpBuffs.append(value)
                else:
                    self.pvpBuffs.append(0)

    def savePvpBuffs(self):
        buffs = self.pvpBuffs
        saveStr = ''
        for index in range(len(buffs)):
            buff = buffs[index]
            if index == 0:
               saveStr = "%s" % buff
            else:
                saveStr = "%s,%s"%(saveStr,buff)
        tableName = 'player_pvp_buffs'
        fields = []
        fields.append('buffstr')
        values = []
        values.append(saveStr)
        condition = "playerid = '%s'" % self.player_id
        db_Manager.updateDataAtTable(tableName,fields,values,condition)

    def insertPvpBuffs(self):
        buffs = self.pvpBuffs
        saveStr = ''
        for index in range(len(buffs)):
            buff = buffs[index]
            if index == 0:
               saveStr = "%s" % buff
            else:
                saveStr = "%s,%s"%(saveStr,buff)
        tableName = 'player_pvp_buffs'
        fields = []
        fields.append('buffstr')
        fields.append('playerid')
        values = []
        values.append(saveStr)
        values.append(self.player_id)
        db_Manager.insertIntoTable(tableName,fields,values)

    def refreshTimeData(self):
        if self.random_rweard_date == None or self.random_rweard_date == "":
            self.random_reward_num = 0
            self.random_rweard_date= GameTools.getDateTimeNowString()
        rr_date = GameTools.string2datetime(self.random_rweard_date)
        time_now = GameTools.getDatetimeNow()
        if rr_date.year != time_now.year or rr_date.month != time_now.month or rr_date.day != time_now.day:
            self.random_reward_num = 0
            self.random_rweard_date= GameTools.getDateTimeNowString()

    def getPartner(self,partner_id):
        for partner in self.partners:
            if partner.partner_id == partner_id:
                return  partner

    def getWaveStartTime(self):
        time = GameTools.string2datetime(self.waveStartTime)
        return  time

    def GetPartnerDPS(self,partnerID):
        for partner in self.partners:
            if partnerID == partner.partner_id:
                partnerLevel = partner.partner_level
                if partnerLevel == 0:
                    return  0
                heroInfo  = heroTable.GetHeroInfoByid(partnerID)
                partnerDPS = partnerUpgradeTable.GetPartnerUpgradeInfo(partnerLevel).effValue
                partnerDPS *= heroInfo.propmodify
                skills = heroInfo.skillsid
                for skillID in skills:
                    if skillID == 0:
                        continue
                    heroSkill = heroSkillTableManager.getHeroSkill(skillID,1)
                    unlockLevel = heroSkill.unlock_level
                    if partnerLevel >= unlockLevel:

                        buffType0 = heroSkill.effectvalue0
                        buffValue0 = heroSkill.effectvalue0
                        if buffType0 == 3:
                            partnerDPS += partnerDPS * buffValue0 / 100
                return  partnerDPS
        return 0

    def updatePVPBuffs(self):
        buffs = self.getEqpAndPartnersBuffs()
        self.pvpBuffs = []
        for index in range(24):
            value = buffs.get(index + 1,0)
            self.pvpBuffs.append(value)

    def getEqpAndPartnersBuffs(self):
        equipmentBuffs = {}
        for(pos, equipment) in self.equipments.items():
            if pos == 10:
                continue
            quality = equipment.equipment_quality
            for index in range(len(equipment.bufList)) :
                if index < quality:
                    equipmentBuf = equipment.bufList[index]
                    oldValue = equipmentBuffs.get(equipmentBuf.bufType,0)
                    newValue = oldValue + equipmentBuf.bufValue
                    equipmentBuffs[equipmentBuf.bufType] = newValue

        setBuffs = equipmentSetTable.getEquipmentSetBuff(self.equipments)

        partnerBuffs = self.CountParterBuffs()

        for (bufftype,buffValue) in setBuffs.items():
            oldValue = equipmentBuffs.get(bufftype,0)
            equipmentBuffs[bufftype] = oldValue + buffValue

        for (bufftype,buffValue) in partnerBuffs.items():
            oldValue = equipmentBuffs.get(bufftype,0)
            equipmentBuffs[bufftype] = oldValue + buffValue

        return  equipmentBuffs

    def GetHeroDPS(self):
        level = self.getSkillInfo(0).skillLevel
        heroInfo  = heroTable.GetHeroInfoByid(50000)
        heroDPS = heroUpgradeTable.getHeroUpgradeInfo(level).effValue
        heroDPS *= heroInfo.propmodify
        return heroDPS

    def GetPartnerDPSSum(self):
        dps_sum = 0
        for partner in self.partners:
            if partner.partner_level > 0:
                dps_sum += self.GetPartnerDPS(partner.partner_id)
        return  dps_sum

    def calculateOfflineResource(self):
        self.calculateOfflineCash()                 # 离线金币结算
        self.calculOfflinePartnersHP()              # 离线小伙伴体力结算

    # 离线小伙伴体力结算
    def calculOfflinePartnersHP(self):
        lastCMDTime = self.last_cmd_time
        lastCMDTime = GameTools.string2datetime(lastCMDTime)
        timeNow =  GameTools.getDatetimeNow()
        if timeNow  < lastCMDTime + datetime.timedelta(seconds  = ConstValue.tokenEffectTime):
            return
        deltaTime = timeNow - lastCMDTime
        totalSeconds = deltaTime.total_seconds()
        totalSeconds = int(totalSeconds)
        if totalSeconds <=50:
            return
        else:
            print('calculOfflinePartnersHP add hp ')
        for partner in self.partners:
            partnerID = partner.partner_id
            heroInfo = heroTable.GetHeroInfoByid(partnerID)
            add_hp = totalSeconds * heroInfo.add_hp
            max_hp = heroInfo.max_hp
            partner.hp += add_hp
            partner.hp = min(partner.hp,max_hp)
            if partner.hp == max_hp:
                partner.sleep = 0

    # 离线金币结算
    def calculateOfflineCash(self):
        playerLevel = self.getSkillInfo(0).skillLevel                   # 主角技能
        playerRevial = self.getSkillInfo(7).skillLevel                  # 重生技能

        # 玩家获取离线奖励技能检测
        if playerLevel == 0 and playerRevial == 0:
            self.offlineCash = 0
            return

        timeLast = GameTools.string2datetime(self.last_cmd_time)        # 最后操作时间
        timeNow =  GameTools.getDatetimeNow()                           # 当前时间

        # 玩家获取离线奖励时间检测
        if timeNow > timeLast + datetime.timedelta(seconds = ConstValue.tokenEffectTime):
            time = timeNow - timeLast
            time = time.total_seconds()
            gold = OfflineCash.calculateOfflineCash(self.game_level,time)           # 获取奖励金币
            self.offlineCash = gold
            self.cash += gold
        else:
            self.offlineCash = 0

    def getBufsValue(self,buffid):
        bufsValue = {}

    def loadSceneInfo(self):
        tableName = "player_scene"
        fields = "scene_id,big_luck_num,small_luck_num"
        conditon = "player_id = %s" % self.player_id
        data = db_Manager.selectDataFromTable(tableName,fields,conditon)
        sceneids = []
        for aData in data:
            sceneInfo = PlayerSceneInfo(aData)
            sceneID = sceneInfo.sceneid
            sceneids.append(sceneID)
            self.scenesInfo[sceneID] = sceneInfo

        for index in range(ConstValue.scenesCount):
            if index not in sceneids:
                sceneInfo = sceneLootEquipTable.getSceneConstInfo(index)
                aData = []
                aData.append(index)
                aData.append(sceneInfo.big_luck_num)
                aData.append(sceneInfo.small_luck_num)
                sceneInfoc = PlayerSceneInfo(aData)
                sceneID = sceneInfoc.sceneid
                self.scenesInfo[sceneID] = sceneInfoc

                fields = []
                fields.append("player_id")
                fields.append("scene_id")
                fields.append("big_luck_num")
                fields.append("small_luck_num")

                values = []
                values.append(self.player_id)
                values.append(index)
                values.append(sceneInfo.big_luck_num)
                values.append(sceneInfo.small_luck_num)
                db_Manager.insertIntoTable(tableName,fields,values)

    # def loadRankInfo(self):
    #     tableName = "player_ranking"
    #     fields = "rank_num"
    #     conditon = "playerid = %s" % self.player_id
    #     data = db_Manager.selectDataFromTable(tableName,fields,conditon)
    #     self.rankNum = data[0][0]

    def CountBufs(self):
        self.buffsValue.clear()
        for buffType in buffTable.tableData.keys():
            self.buffsValue[buffType] = 0

        self.CountEquipmentBuffs()
        self.CountHeroSkillBuffs()
        self.CountParterBuffs()

    def CountEquipmentBuffs(self):
        for(pos, equipment) in self.equipments.items():
            for equipmentBuf in equipment.bufList:
                self.buffsValue[equipmentBuf.buffType] += equipmentBuf.bufValue

    def CountHeroSkillBuffs(self):
        for skillID in range(len(self.skills)):
            if skillID != 0 and skillID != 7: # 0level 7 revival
                skillLevel = self.skills[skillID]
                if skillLevel == 0:
                    continue
                heroSkill = heroSkillTableManager.getHeroSkill(skillID,skillLevel)
                buffType0 = heroSkill.effecttype0
                buffValue0 = heroSkill.effectvalue0
                # buffType1 = heroSkill.effecttype1
                # buffValue1 = heroSkill.effectvalue1
                spawnnewid = heroSkill.spawnnewid

                # self.buffsValue[buffType0] += buffValue0
                # self.buffsValue[buffType1] += buffValue1

    def CountParterBuffs(self):
        buffs = {}
        for parter in self.partners:
            parterid = parter.partner_id
            if not parterid in self.selected_partners:
                continue
            level = parter.partner_level
            if level > 0:
                skills = heroTable.GetHeroInfoByid(parterid).skillsid
                for skillID in skills:
                    if skillID == 0:
                        continue
                    heroSkill = heroSkillTableManager.getHeroSkill(skillID,1)
                    unlockLevel = heroSkill.unlock_level
                    if level >= unlockLevel:

                        buffType0 = heroSkill.effectvalue0
                        buffValue0 = heroSkill.effectvalue0

                        value = buffs.get(buffType0,0)
                        buffs[buffType0] = buffValue0 + value

                        spawnnewid = heroSkill.spawnnewid
        return  buffs

    def passLevel(self,levelID,waveID):
        if levelID > self.game_level:
            self.game_level = levelID
            self.game_wave = waveID
        elif levelID == self.game_level and waveID > self.game_wave:
            self.game_level = levelID
            self.game_wave = waveID

    def addResource(self,type,num):
        if type == ResourceType.cash:
            self.cash += num
        elif type == ResourceType.revial:
            self.revial += num
        elif type == ResourceType.gems:
            self.gems += num
        elif type == ResourceType.pvp_medal:
            self.pvp_medal += num
        elif type == ResourceType.chanllengeNum:
            self.chanllenge_num += num
        elif type == ResourceType.awake_spell:
            self.awake_spell_num += num

    def getResourceValue(self,type):
        if type == ResourceType.cash:
            return self.cash
        elif type == ResourceType.revial:
            return self.revial
        elif type == ResourceType.chanllengeNum:
            return self.chanllenge_num

    def isUseSkillNow(self):
        for index in range(1,7):
            skillInfo = self.skills[index]
            if skillInfo.IsEffectNow():
                return  True
        return False

    def costResource(self,type,num):
        num = int(num)

        if type == ResourceType.pvp_medal:
            if self.pvp_medal  >= num:
                self.pvp_medal -= num
            else:
                return  False


        if type == ResourceType.cash:
            if self.cash * 1.3 >= num:
                self.cash -= num
                if self.cash < 0:
                    self.cash = 0
            else:
                return  False
        elif type == ResourceType.revial:
            if self.revial >= num:
                self.revial -= num
            else:
                return  False
        elif type == ResourceType.chanllengeNum:
            if self.chanllenge_num >= num:
                self.chanllenge_num -= num
            else:
                return False
        elif type == ResourceType.gems:
            if self.gems >= num:
                self.gems -= num
            else:
                return False
        elif type == ResourceType.awake_spell:
            if self.awake_spell_num >= num:
                self.awake_spell_num -= num
            else:
                return  False
        return True

    def loadEqument(self):
        tableName = "player_equip"
        fields = "pos,equipmentid,equipment_quality,equipment_level,id,game_level,upgrade_cost," \
                 "buftype1,bufvalue1,buftype2,bufvalue2,buftype3,bufvalue3,buftype4,bufvalue4,buftype5,bufvalue5," \
                 "bufbasetype1,bufbasevalue1,bufbasetype2,bufbasevalue2,bufbasetype3,bufbasevalue3,bufbasetype4,bufbasevalue4,bufbasetype5,bufbasevalue5"
        conditon = "player_id = %s" % self.player_id
        data = db_Manager.selectDataFromTable(tableName,fields,conditon)
        posList = []

        for pos in range(12):
        # for pos in range(6):
            posList.append(pos)
        posList
        # posList.append(10)

        for equipmentData in data:
            posList.remove(equipmentData[0])
            if equipmentData[1] == -1:
                continue
            equipment = EquipMent(data = equipmentData)
            equipPos = int(equipmentData[0])
            self.equipments[equipPos] = equipment

        for pos in posList:
            fields = []
            fields.append('player_id')
            fields.append('pos')

            values = []
            values.append(self.player_id)
            values.append(pos)

            db_Manager.insertIntoTable(tableName,fields,values)

    def skillUpgrade(self,skill_id,to_level):
        heroLevel = 0
        for skill in self.skills:
            if skill.skillID == 0:
                heroLevel = skill.skillLevel
                break

        for skill in self.skills:
            if skill.skillID == skill_id:
                if skill.skillLevel >= to_level:
                    return None
                else:
                    cost = 0
                    if skill_id == 0:
                        for level in range(skill.skillLevel +1, to_level + 1):
                            cost += heroUpgradeTable.getHeroUpgradeInfo(level).cost
                    else:

                        searchLevel = to_level

                        # skillInfo = heroSkillTableManager.getHeroSkill(skill.skillID,searchLevel)
                        # unlockLevel = skillInfo.unlock_level
                        # if heroLevel < unlockLevel:
                        #     return ErrorCode.notunlocknow
                        cost = 0
                        for level in range(skill.skillLevel +1, to_level + 1):
                            if skill_id != 7:
                                cost += heroSkillTableManager.getHeroSkill(skill_id,level).upcost

                    if self.costResource(ResourceType.cash,cost):
                        skill.skillLevel = to_level
                        #ok pass
                        break
                    else:
                        return (1111,"nowLevel:%s toLevel:%s own:%s need:%s"%(skill.skillLevel,to_level,self.cash,cost))

        for skill in self.skills:
            if skill.skillID == skill_id:
                skill.skillLevel = to_level
                if skill_id == 7:
                    self.relife()
                return None

        return None

    def relife(self):
        self.cash = 0
        self.lootEquipLevel = 0
        for skill in self.skills:
            if skill.skillID == 7:
                pass
            elif skill.skillID == 0:
                skill.skillLevel = 1
            else:
                skill.skillLevel = 0
        for parter in self.partners:
            parter.partner_level = 0
        levelInfo = levelTable.getItem(self.game_level)
        gotRevialNum = levelInfo.relivegold
        self.addResource(ResourceType.revial,gotRevialNum)
        self.game_level = 1
        self.game_wave = 0
        self.selected_partners = []

    def useSkill(self,skillID):
        playerSkillInfo = self.getSkillInfo(skillID)
        playerSkillInfo.last_use_time = GameTools.getDateTimeNowString()

    def partnerUpgrade(self,partner_id,to_level):
        the_partner =None

        for partner in self.partners:
            if partner.partner_id == partner_id:
                heroConstInfo = heroTable.GetHeroInfoByid(partner.partner_id)
                if partner.partner_level == 0:

                    return ErrorCode.notunlocknow
                if partner.partner_level >= to_level:
                    return None
                else:
                    costSum = 0
                    order = partner.order
                    fromLevel = max(2,partner.partner_level + 1)
                    for level in range(fromLevel, to_level + 1):
                        cost = partnerUpgradeTable.GetPartnerUpgradeInfo(level).cost
                        cost *= heroConstInfo.upgradeCostModify

                        if heroConstInfo.costType == ResourceType.cash:
                            modifyValue = heroUnlockTable.getHeroUnlockInfoByOrder(order).modify
                            cost *= modifyValue

                        cost = int(cost)
                        costSum += cost

                    if self.cash >= costSum:
                        self.cash -= costSum
                        partner.partner_level = to_level

                        return None
                    else:
                        return (300,"resource not enough.nowLevel:%s toLevel:%s own:%s need:%s"%(partner.partner_level,to_level,self.cash,costSum))

    def getEquipmentByID(self,id):
        for _, equipment in self.equipments.items():
            if equipment.id == id:
                return  equipment
        return  None

    def equipmentUpgrade(self,id,to_quality,to_level,buffs,costValue):
        equipMent = self.getEquipmentByID(id)
        if equipMent == None:
            return ErrorCode.upgradeEqp_notHaveEqp

        if to_quality < equipMent.equipment_quality:
            return  None

        if to_quality == equipMent.equipment_quality and to_level <= equipMent.equipment_level:
            return  None

        nowLevel40 = (equipMent.equipment_quality - 1) * 10 + equipMent.equipment_level
        tolevel40 = (to_quality - 1) * 10 + to_level
        if to_quality > equipMent.equipment_quality:

            levelCost = self.equipmentUpgradeCost(nowLevel40,tolevel40,equipMent.game_level)
            # equipQtyUpgradeInfo = equipmentQtyUpgradeTable.getEqpQualityUpgradeInfo(to_quality)
            if self.revial >= levelCost:
                qualityCost = 0
                for nexQuality in range(equipMent.equipment_quality +1, to_quality +1):
                    equipQtyUpgradeInfo = equipmentQtyUpgradeTable.getEqpQualityUpgradeInfo(nexQuality)
                    qualityCost += equipQtyUpgradeInfo.costValue
                selfCostValue = self.getResourceValue(equipQtyUpgradeInfo.costType)
                if levelCost > costValue *3:
                    return ErrorCode.costNotMatch
                # qualityCost = 0
                if costValue > selfCostValue:
                    return  ErrorCode.resourceNotEnough
                result = equipMent.upGradeToLevel(to_quality,to_level,buffs)
                if not result :
                    return ErrorCode.toQltyBuffVerifyERROR

                self.costResource(ResourceType.cash,costValue)
                equipMent.upgradeCost += costValue
                equipMent.upgradeCost = int(equipMent.upgradeCost)
                self.costResource(equipQtyUpgradeInfo.costType,qualityCost)

            else:
                return  ErrorCode.resourceNotEnough

            if not self.costResource(ResourceType.revial,levelCost):
                return ErrorCode.resourceNotEnough
            # upgrade quality
        else:

            levelCost = self.equipmentUpgradeCost(nowLevel40,tolevel40,equipMent.game_level)
            levelCost = int(levelCost)
            if levelCost > costValue *3:
                    return ErrorCode.costNotMatch
            if self.revial >= costValue:
                result = equipMent.upGradeToLevel(to_quality,to_level,buffs)
                if not result :
                    return ErrorCode.toQltyBuffVerifyERROR

                self.costResource(ResourceType.revial,costValue)
                equipMent.upgradeCost += costValue
                equipMent.upgradeCost = int(equipMent.upgradeCost)
            else:
                return  ErrorCode.resourceNotEnough
            # upgrade level

        return  None

    def equipmentUpgradeCost(self,nowLevel,tolevel,game_level):
        totalCost = 0
        if game_level < 1:
            game_level = 1
        if game_level > 1000:
            game_level = 1000
        levelConstInfo = levelTable.getItem(game_level)
        levelAddCost = levelConstInfo.eqmUpgradeAddCost
        for nexLevel in range(nowLevel + 1,tolevel +1):
            equipmentLevelUpInfo = equipmentUpgradeTable.getEuipmentLevelUpInfo(nexLevel)
            baseCost = equipmentLevelUpInfo.baseCost
            nextLevelCost = baseCost * levelAddCost
            totalCost += nextLevelCost
        return totalCost

    def equip_equipment(self,id,pos):
        equipmentInSlot = None
        for eq in self.equipments:
            if self.equipments[eq].id == id:
                equipmentInSlot = self.equipments[eq]
                break
        equipmentInPos = self.equipments.get(pos)

        if equipmentInPos != None and equipmentInPos.id == id: # already exchange pos
            return  None

        if equipmentInSlot == None :
            return ErrorCode.equipment_pos10empty

        if equipmentInSlot.id != id:
            return  ErrorCode.equipment_pos10idnotmatch

        changeEquipmentOldPos = equipmentInSlot.pos
        if equipmentInPos == None:
            self.equipments[pos] = equipmentInSlot
            equipmentInSlot.pos = pos
            del self.equipments[changeEquipmentOldPos]
        else:
            self.equipments[changeEquipmentOldPos] = equipmentInPos
            equipmentInPos.pos = changeEquipmentOldPos
            self.equipments[pos] = equipmentInSlot
            equipmentInSlot.pos = pos
        return None

    def takeOffEquipment(self,pos,id):
        # position empty check
        if self.equipments.get(pos):
            return  ErrorCode.takeoff_pos10NotEmpyty

        takeOffEquipment = None
        for eq in self.equipments:
            if self.equipments[eq].id == id:
                takeOffEquipment = self.equipments[eq]
                break
        changeEquipmentOldPos = takeOffEquipment.pos
        del self.equipments[changeEquipmentOldPos]

        takeOffEquipment.pos = pos
        self.equipments[pos] = takeOffEquipment

        # if pos == 10:
        #     return  ErrorCode.takeoffFromPosIs10
        #
        # equipment = self.equipments.get(pos)
        # equipment10 = self.equipments.get(10)
        # if equipment10 != None:
        #     if equipment10.id == id:
        #         return  None
        #     print('takeOffEquipment error:-->no. 10 slot not empty')
        #     return  ErrorCode.takeoff_pos10NotEmpyty
        #
        # if equipment == None:
        #     print('takeOffEquipment error:-->slot not empty')
        #     return  ErrorCode.takeoff_frompos_empty
        #
        # self.equipments[10] = equipment
        # del self.equipments[pos]

    def wearEquipment(self, from_pos, to_pos):
        wearEquipment = self.equipments[from_pos]               # 穿的装备
        takeOffEquipment = self.equipments.get(to_pos, None)    # 被替换的装备

        # wear
        self.equipments[to_pos] = wearEquipment
        wearEquipment.pos = to_pos
        del self.equipments[from_pos]

        if takeOffEquipment:
            self.equipments[from_pos] = takeOffEquipment
            takeOffEquipment.pos = from_pos

    def saleEquipment(self,pos,id,useGem,saleCost):
        # equipment = self.equipments.get(pos)
        equipment = None
        for eq in self.equipments:
            if self.equipments[eq].id == id:
                equipment = self.equipments[eq]
                break

        if equipment != None and equipment.id == id:
            # gemsNum = gloabalBase.getValue('equipment_fullrecycle_cost')
            gemsNum = saleCost
            if not useGem :
                gemsNum = 0

            if self.costResource(ResourceType.gems,gemsNum):
                del self.equipments[equipment.pos]
            else:
                return  ErrorCode.resourceNotEnough
        else:
            return  ErrorCode.logicError

    def delEquipment(self, equipment):
        del self.equipments[equipment.pos]

    def loadPartners(self):
        tableName = "player_partner"
        fields = "partner_id,level,hadBeenUnlocked,hp,sleep,order_num"
        conditon = "player_id = %s" % self.player_id
        data = db_Manager.selectDataFromTable(tableName,fields,conditon)
        partners = []
        for partnerData in data:
            partner = Partner(partnerData)
            self.partners.append(partner)
            partners.append(partner.partner_id)

        partnersCount = heroTable.getPartnersCount()
        for index in range(partnersCount):
            partnerxx = index + 1
            if not partnerxx in partners:
                fields = []
                fields.append('player_id')
                fields.append('partner_id')
                fields.append('level')
                fields.append('hp')
                fields.append('sleep')
                values = []
                values.append(self.player_id)
                values.append(partnerxx)
                values.append(0) #level
                heroInfo = heroTable.GetHeroInfoByid(partnerxx)
                max_hp = heroInfo.max_hp
                values.append(max_hp)#hp
                values.append(0)#sleep

                db_Manager.insertIntoTable(tableName,fields,values)

                partnerData = []
                partnerData.append(partnerxx)
                partnerData.append(0)
                partnerData.append(0)
                partnerData.append(max_hp)
                partnerData.append(0)
                partnerData.append(0)
                partnerData.append(1)
                partner = Partner(partnerData)
                self.partners.append(partner)

    def loadSkills(self):
        tableName = "player_skill"
        fields = "skill_id,level,last_use_time"
        conditon = "player_id = %s" % self.player_id
        data = db_Manager.selectDataFromTable(tableName,fields,conditon)
        skillids = []
        for skillData in data:
            heroSkill = HeroSkillData(skillData)
            if heroSkill.skillID == 0 and heroSkill.skillLevel < 1:
                heroSkill.skillLevel = 1

            skillids.append(heroSkill.skillID)
            self.skills.append(heroSkill)

        for skillidInTable in range(8):
            if not skillidInTable in skillids:
                fields = []
                fields.append('player_id')
                fields.append('skill_id')
                fields.append('level')
                fields.append('last_use_time')
                values = []
                values.append(self.player_id)
                values.append(skillidInTable)
                if skillidInTable == 0:
                    values.append(1)
                else:
                    values.append(0)

                t_now =  GameTools.getDatetimeNow()
                t_ok = t_now- datetime.timedelta(days = 1)
                t_now_string = GameTools.datetime2string(t_ok)
                values.append(t_now_string)
                db_Manager.insertIntoTable(tableName,fields,values)

                skillData = []
                skillData.append(skillidInTable)
                if skillidInTable == 0:
                    skillData.append(1)
                else:
                    skillData.append(0)
                skillData.append(t_now_string)
                heroSkill = HeroSkillData(skillData)
                self.skills.append(heroSkill)

    def loadSelectPartners(self):
        tableName = "player_selected_partner"
        fields = "`0`,`1`,`2`,`3`,`4`,`5`,`6`,`7`,`8`,`9`"

        conditon = "player_id = %s" % self.player_id
        data = db_Manager.selectDataFromTable(tableName,fields,conditon)

        for seletedData in data:
            for id in seletedData:
                self.selected_partners.append(id)

        if len(data) == 0:
            fields = []
            fields.append('player_id')
            values = []
            values.append(self.player_id)
            for index in range(10):
                fields.append("%s" %index)
                values.append(-1)
                self.selected_partners.append(-1)
            db_Manager.insertIntoTable(tableName, fields,values ,None)

    def addEquipment(self,newEquipMent):
        pos = newEquipMent.pos
        self.equipments[pos] = newEquipMent

    def offLine(self):
        self.saveData2DB()
        # tableName = 'player_base_info'
        # fields = []
        # fields.append('is_online')
        # values = []
        # values.append(0)
        # conditions = "playerid = '%s'" % self.player_id
        # db_Manager.updateDataAtTable(tableName, fields,values,conditions)

    def saveData2DB(self):

        self.login_days_check()
        tableName = 'player_base_info'
        fields = []
        fields.append('playerid')
        fields.append('pvp_medal')
        fields.append('gem')
        fields.append('revive')
        fields.append('cash')
        fields.append('game_level')
        fields.append('game_wave')
        fields.append('chanllenge_date')
        fields.append('chanllenge_num')
        fields.append('avatorid')
        fields.append('lootEquipLevel')
        fields.append('is_brush')
        fields.append('last_cmd_time')
        fields.append('random_reward_num')
        fields.append('random_reward_date')
        fields.append('lastTimedRewardDatetime')
        fields.append('last_timed_reward_ranknum')
        fields.append('buy_del_challenge_cd_num')
        fields.append('daily_datetime')
        fields.append('add_chanllenge_num')
        fields.append('awake_spell_num')
        fields.append('last_free_draw_datetime')
        fields.append('recharge_total_num')
        fields.append('recharge_get_gifts_status')
        fields.append('last_login_date')
        fields.append('login_num')
        fields.append('login_get_gifts_status')
        values = []
        values.append(self.player_id)
        values.append(self.pvp_medal)
        values.append(self.gems)
        values.append(self.revial)
        values.append(self.cash)
        values.append(self.game_level)
        values.append(self.game_wave)
        values.append(self.change_date)
        values.append(self.chanllenge_num)
        values.append((self.avatorid))
        values.append(self.lootEquipLevel)
        values.append(self.isBrush)
        values.append(self.last_cmd_time)
        values.append(self.random_reward_num)
        values.append(self.random_rweard_date)
        values.append(self.last_timed_reward_datetime)
        values.append(self.last_timed_reward_ranknum)
        values.append(self.buy_del_challenge_cd_num)
        values.append(self.daily_datetime)
        values.append(self.add_chanllenge_num)
        values.append(self.awake_spell_num)
        values.append(self.last_free_draw_datetime)
        values.append(self.recharge_total_num)
        values.append(json.dumps(self.recharge_get_gifts_status))
        values.append(self.last_login_date)
        values.append(self.login_num)
        values.append(json.dumps(self.login_get_gifts_status))
        conditions = "playerid = '%s'" % self.player_id
        db_Manager.updateDataAtTable(tableName, fields,values,conditions)

        self.saveEquipments()
        self.saveSkill()
        self.savePartner()
        self.saveSceneInfo()
        self.savePvpBuffs()

    def saveSceneInfo(self):

        for sceneid,sceneInfo in self.scenesInfo.items():
            tableName = "player_scene"
            fields = []
            fields.append("big_luck_num")
            fields.append("small_luck_num")

            values = []
            values.append(sceneInfo.big_luck_num)
            values.append(sceneInfo.small_luck_num)

            condition = "player_id = '%s' and scene_id = '%s'"%(self.player_id,sceneid)
            db_Manager.updateDataAtTable(tableName,fields,values,condition)

    def getSkillInfo(self,skillid):
        for skillInfo in self.skills:
            if skillInfo.skillID == skillid:
                return  skillInfo

    def saveSkill(self):

        for skill in self.skills:
            tableName = "player_skill"
            fields = []
            fields.append('level')
            fields.append('last_use_time')

            values = []
            values.append(skill.skillLevel)
            values.append(skill.last_use_time)

            condition = "player_id = '%s' and skill_id = '%s'"%(self.player_id,skill.skillID)
            db_Manager.updateDataAtTable(tableName,fields,values,condition)

    def savePartner(self):
        for partner in self.partners:
            tableName = "player_partner"
            fields = []
            fields.append('level')
            fields.append('hadBeenUnlocked')
            fields.append('hp')
            fields.append('sleep')
            fields.append('order_num')
            values = []
            values.append(partner.partner_level)
            values.append(partner.hadBeenUnlocked)
            values.append(partner.hp)
            values.append(partner.sleep)
            values.append(partner.order)
            condition = "player_id = '%s' and partner_id = '%s'"%(self.player_id,partner.partner_id)
            db_Manager.updateDataAtTable(tableName,fields,values,condition)

        # selected partner
        tableName = "player_selected_partner"
        fields = []
        values = []
        condition = "player_id = '%s'" % self.player_id
        for index in range(10):
            fields.append("%s" % index)
            if len(self.selected_partners) -1 < index:
                values.append(-1)
            else:
                values.append(self.selected_partners[index])
        db_Manager.updateDataAtTable(tableName,fields,values,condition)

    def saveEquipments(self):
        posList = []
        for index in range(12):
        # for index in range(6):
            posList.append(index)
        # posList.append(10)

        for pos,equipment in self.equipments.items():
            posList.remove(pos)
            tableName = "player_equip"
            fields = []
            fields.append('equipmentid')
            fields.append('equipment_quality')
            fields.append('equipment_level')
            fields.append('id')
            fields.append('game_level')
            fields.append('upgrade_cost')
            fields.append('buftype1')
            fields.append('bufvalue1')
            fields.append('buftype2')
            fields.append('bufvalue2')
            fields.append('buftype3')
            fields.append('bufvalue3')
            fields.append('buftype4')
            fields.append('bufvalue4')
            fields.append('buftype5')
            fields.append('bufvalue5')

            fields.append('bufbasetype1')
            fields.append('bufbasevalue1')
            fields.append('bufbasetype2')
            fields.append('bufbasevalue2')
            fields.append('bufbasetype3')
            fields.append('bufbasevalue3')
            fields.append('bufbasetype4')
            fields.append('bufbasevalue4')
            fields.append('bufbasetype5')
            fields.append('bufbasevalue5')

            values = []
            values.append(equipment.equipmentid)
            values.append(equipment.equipment_quality)
            values.append(equipment.equipment_level)
            values.append(equipment.id)
            values.append(equipment.game_level)
            values.append(equipment.upgradeCost)

            for buf in equipment.bufList:
                values.append(buf.bufType)
                values.append(buf.bufValue)

            for buf in equipment.bufBaseList:
                values.append(buf.bufType)
                values.append(buf.bufValue)

            condition = "player_id = %s and pos = %s " %(self.player_id, pos)
            db_Manager.updateDataAtTable(tableName, fields, values, condition)

        for emptyPos in posList:
            tableName = "player_equip"
            fields = []
            values = []

            fields.append('equipmentid')
            values.append(-1)
            condition = "player_id = %s and pos = %s " %(self.player_id, emptyPos)
            db_Manager.updateDataAtTable(tableName, fields, values, condition)

    def getToken(self, idfa):
        uuid = "%s %s %s"%(idfa,datetime.datetime.now(),"tap")
        bjsonStr = bytes(uuid, encoding = "utf8")
        base64b = base64.encodebytes(bjsonStr)
        base64s = base64b.decode(encoding='UTF-8')
        base64s = base64s.rstrip()
        return base64s

    def synchronizationPartenrHP(self,partners_hp,sleeps):

        for partner in self.partners:
            partnerID = partner.partner_id
            if len(partners_hp) + 1 >= partnerID:
                hp = partners_hp[partnerID - 1]
                partner.hp = hp
                partner.sleep = sleeps[partnerID - 1]

    def login_days_check(self):
        if time.strftime('%Y-%m-%d') != self.last_login_date:
            self.last_login_date = time.strftime('%Y-%m-%d')
            self.login_num += 1

            # 封测活动奖励
            #self.addResource(ResourceType.gems, 500)

