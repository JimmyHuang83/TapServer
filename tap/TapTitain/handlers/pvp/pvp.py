import tornado
import  tornado.web
import  tornado.gen
from const_tables.pvp_fight_reward import pvpFightRewardTable
from managers.database_manager import db_Manager
from managers.player_data_manager import playerDataManager
from managers.pvp_data_manager import pvpDataManger
from managers.rank_manger import rankManager
from models.game_enum import ResourceType
from models.message import MessageTools, MessData, ErrorCode
from const_tables.gloabl_base_table import gloabalBase
__author__ = 'Mike'

class PvPResultHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        token = dictData.get('token')
        result = dictData.get('result', 0)
        targetID = dictData.get('target_id')
        lowRank = dictData.get('lowRank',0)
        tap_count = dictData.get('tap_count')
        crital_count = dictData.get('crital_count')
        target_hp = dictData.get('target_hp',0)  # the data need verify.
        player = playerDataManager.getPlayerByToken(token)
        returnDict = {}
        returnData = MessData()



        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
        elif player.player_id == targetID:
            returnData = MessData(ErrorCode.cannotAttackYourself)
        elif not pvpDataManger.fightFinished(player.player_id,targetID):
                returnData = MessData(ErrorCode.fightTargetNotMatch)
        elif self.verifyPVPFight(tap_count,crital_count,player,target_hp):
            # 玩家connect id检测
            connect_id = dictData.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            if result == 1 and lowRank == 0:
                rankManager.pvpWin(player.player_id,targetID)
            else:
                pass
            fightRewards = pvpFightRewardTable.getPvpFightRewardByResult(result)
            for reward in fightRewards:
                type = reward.type
                value = reward.value
                player.addResource(type,value)

            rank_num = rankManager.getRankNumByPlayerid(player.player_id)
            target_num = rankManager.getRankNumByPlayerid(targetID)
            self.saveResult(player.player_id,targetID,result,rank_num,target_num,lowRank)
            rankList = rankManager.getRankList(rank_num)
            returnDict['rank_num'] = rank_num
            returnDict['rankList'] = rankList
            returnData.data = returnDict
        else:
            returnData = MessData(ErrorCode.pvpVerifyError)
        str = MessageTools.encode(returnData,False)
        self.write(str)
        self.finish()

    def saveResult(self,attackerid,targetid,result,attackerNum,targetNum,lowRank):
        tableNmae = "player_fight_result"
        fields = []
        fields.append('attacker_id')
        fields.append('target_id')
        fields.append('result')
        fields.append('attacker_num')
        fields.append('target_num')
        fields.append('fight_low')
        values = []
        values.append(attackerid)
        values.append(targetid)
        values.append(result)
        values.append(attackerNum)
        values.append(targetNum)
        values.append(lowRank)
        db_Manager.insertIntoTable(tableNmae,fields,values)


    def verifyPVPFight(self,tap_count,crital_count, playerInfo,target_hp):
        # if tap_count > 30 * 60:
        #     return  False
        tap_count = 15 * 40
        # if tap_count > 100 and crital_count > tap_count * 0.99 :
        #     return  False  # critall verify closed now !!!

        if playerInfo.isUseSkillNow():
            return True

        partnerDPS = playerInfo.GetPartnerDPSSum()
        heroTapDMG = playerInfo.GetHeroDPS()



        # 只做最简单的验证，
        playerBuffList = playerInfo.pvpBuffs
        playerBuffs = {}
        for index in range(len(playerBuffList)):
            playerBuffs[index] = playerBuffList[index]
        buff21Value = playerBuffs.get(21,0)  # 对BOSS伤害增加
        buff11Value = playerBuffs.get(11,0)  # 战斗时间增加
        buff4Value = playerBuffs.get(4,0)  # 小伙伴攻速
        timeSeconds = 30 * (1 + buff11Value / 1000)

        tap_count = 15 * (timeSeconds + 10)
        buff2Value = playerBuffs.get(2,0)  # 英雄点击伤害增加
        buff5Value = playerBuffs.get(5,0)  # 所有小伙伴攻击力
        # partnerDPS = player.GetPartnerDPSSum()
        # heroTapDMG = player.GetHeroDPS()

        critalMin = gloabalBase.getValue("BaseCrital")
        critalMax = gloabalBase.getValue("CritalMax")
        critalbuffValue = playerBuffs.get(10,0)
        critalbuffValue += critalMin
        critalbuffValue = min(critalbuffValue,critalMax)

        critalBaseRate = gloabalBase.getValue("BaseCritalRate")
        critalRate = critalBaseRate + critalbuffValue / 1000 *10
        critalDMG = heroTapDMG * critalRate * crital_count

        hertHp = heroTapDMG * (1 +buff2Value/ 1000) * tap_count + partnerDPS * \
                                                                  (1+ buff4Value / 1000) * (1+ buff5Value / 1000) * timeSeconds + critalDMG
        hertHp = hertHp *(1 + buff21Value / 1000)

        # return hertHp * 10 > target_hp #colose the pvp fight virify.
        return  True

