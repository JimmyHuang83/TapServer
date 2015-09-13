import datetime
import tornado.web
import  tornado.gen
from const_tables.equipment_set import equipmentSetTable
from const_tables.gloabl_base_table import gloabalBase
from const_tables.hero_skill_table import heroSkillTableManager
from const_tables.level_table import levelTable
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.game_tools import GameTools
from models.message import MessageTools, MessData, ErrorCode


__author__ = 'Mike'
class GamePlayWinHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        cash = params.get('cash')                           # 金币
        level = params.get('level')                         # 关卡
        awave = params.get('wave')                          # 小乖波数


        tap_count = params.get('tap_count',15*40)
        tap_count = 15 * 40
        crital_count = params.get('crital_count',0)
        player = playerDataManager.getPlayerByToken(token)
        returnData = MessData()

        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
        else:
            # 玩家connect id检测
            connect_id = params.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            plevel = player.game_level
            pwave = player.game_wave

            if not  self.verifyLevelAndWave(plevel,pwave,level,awave):
                print('level wave not match')
                returnData = MessData(ErrorCode.levelandwaveLogicError)

            elif not  self.verifyPVEValue(level,awave,player,tap_count,crital_count,cash):
                print('monster not die')
                returnData = MessData(ErrorCode.monsterNotDie)
            else:
                player.addResource(ResourceType.cash, cash)
                if awave != -1:
                    player.passLevel(level,awave)
                    player.isBrush = 0

                player.waveStartTime = GameTools.datetime2string(datetime.datetime.now())
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)
        # return  returnData

    def verifyLevelAndWave(self,plevel,pwave,level,wave):
        return  True


    def verifyPVEValue(self,level,wave,player,tap_count,crital_count,cash):
        playerBuffs = player.pvpBuffs
        if wave != 10:
            return  True

        if player.isUseSkillNow():
            return True

        buffs = equipmentSetTable.getEquipmentSetBuff(player.equipments)


        partnerDPS = player.GetPartnerDPSSum()
        heroTapDMG = player.GetHeroDPS()
        logs = "partnerDPS:%s heroTapDMG:%s"%(partnerDPS,heroTapDMG )
        print(logs)
        critalIncreaseDMG = 0
        # waveStartTime = player.getWaveStartTime()
        # timeDelta = datetime.datetime.now() - waveStartTime
        # totalSeconds = timeDelta.total_seconds()
        # totalSeconds = int(totalSeconds)
        # print("totalSeconds%s" %totalSeconds)

        totalSeconds = 60  #   max fight time


#############################################
        skill4Level = player.getSkillInfo(4).skillLevel
        skill4Value = 0
        if skill4Level > 0:
            effectValue0 = heroSkillTableManager.getHeroSkill(4,skill4Level).effectvalue0
            skill4Value =  heroSkillTableManager.getHeroSkill(4,skill4Level).bufvalue


            #############################
            #hero skill 4 effect
            #############################
            oldValue = buffs.get(effectValue0,0)
            value = oldValue + skill4Value
            buffs[effectValue0] = value

            partnerDPS += partnerDPS * skill4Value / 100
#############################################

#############################################
        skill5level = player.getSkillInfo(5).skillLevel
        skill5value = 0
        if skill5level > 0:
            effectValue0 = heroSkillTableManager.getHeroSkill(5,skill5level).effectvalue0
            skill5value = heroSkillTableManager.getHeroSkill(5,skill5level).bufvalue
            #############################
            #hero skill 5 effect
            #############################
            oldValue = buffs.get(effectValue0,0)
            value = oldValue + skill4Value
            buffs[effectValue0] = value

            heroTapDMG += heroTapDMG * skill5value / 100

#############################################

#############################################
        skill3level = player.getSkillInfo(3).skillLevel
        skill3value = 0
        # if skill3level > 0:
            # effectValue0 = heroSkillTableManager.getHeroSkill(3,skill3level).effectvalue0
            # skill3value = heroSkillTableManager.getHeroSkill(3,skill3level).bufvalue
            # baseCritalDMG = gloabalBase.getValue("BaseCritalRate")
            #############################
            #hero skill 3 effect
            #############################
            # oldValue = buffs.get(effectValue0,0)
            # value = oldValue + skill4Value
            # buffs[effectValue0] = value

##############################################

        partnerBuffs = player.CountParterBuffs()

        for (buffid,value) in partnerBuffs.items():
            oldValue = buffs.get(buffid,0)
            value += oldValue
            buffs[buffid] = value

###############################################


        levelInfo = levelTable.getItem(level)
        coins = 0
        if wave == 10:
            coins = levelInfo.bosscoins
        else:
            coins = levelInfo.monstercoins

        coinsBuffValue = buffs.get(1,0)
        print("coin buff value : %s" %coinsBuffValue)
        coins += coins * (coinsBuffValue + 10) / 100

        heroDMGBuffValue = buffs.get(2,0)
        heroTapDMG += heroTapDMG * heroDMGBuffValue / 100

        partnerSpeedBuffValue = buffs.get(4,0)
        partnerDPS += partnerDPS * partnerSpeedBuffValue / 100

        partnerDPSBuffValue = buffs.get(5,0)
        partnerDPS += partnerDPS * partnerDPSBuffValue / 100


        critalDMG = 0
        if crital_count > tap_count * 0.9:
            # crital rate > 90 % error
            print("crital rate > 90 % error")
            return  False
        elif crital_count > 0:
            critalMin = gloabalBase.getValue("BaseCrital")
            critalMax = gloabalBase.getValue("CritalMax")
            #crital
            critalIncreaseDMG = 0
            critalbuffValue = buffs.get(10,0)
            critalbuffValue += critalMin
            critalbuffValue = min(critalbuffValue,critalMax)

            critalBaseRate = gloabalBase.getValue("BaseCritalRate")
            critalRate = critalBaseRate + critalbuffValue / 1000 *10
            critalDMG = heroTapDMG * critalRate * critalMax

        #coins = coins + coins  # tamplate
        # coins += coins
        # coins += coins
        if cash > coins:
            returnData = MessData(ErrorCode.coinOutOfRange)


        print("partnerBuffs:%s"%partnerBuffs)

        levelInfo = levelTable.getItem(level)
        monsterHP = levelInfo.monsterhp
        if wave == 10:
            monsterHP = levelInfo.bosshp

        partnerKillHp = partnerDPS * totalSeconds
        heroKillHp = heroTapDMG * tap_count
        killHP = partnerKillHp + heroKillHp + critalDMG



        if monsterHP > killHP:
            print('monsterHP > killHP')

        buff6Value = 0
        if len(playerBuffs) >= 6:
            buff6Value = playerBuffs[5]

        buff6Times = 1 + buff6Value / 1000


        if wave == 10:
            log_str = "heroKillHp:%s,partnerKillHp%s,critalDMG:%s"%(heroKillHp,partnerKillHp,critalDMG)
            MessageTools.log.info("hp:"+ log_str)
            return  killHP * 10 * buff6Times > monsterHP
        else:
            return  True

class GamePlayLootReviveHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        level = params.get('level')
        revive = params.get('revive')

        player = playerDataManager.getPlayerByToken(token)
        returnData = MessData()
        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
        else:
            # 玩家connect id检测
            connect_id = params.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            player.addResource(ResourceType.revial,revive)

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)

class PvELoostHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        level = params.get('level')
        wave = params.get('wave')

        player = playerDataManager.getPlayerByToken(token)
        returnData = MessData()
        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
        else:
            # 玩家connect id检测
            connect_id = params.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            player.waveStartTime = GameTools.datetime2string(datetime.datetime.now())
            if wave == 10:
                player.isBrush = 1
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)