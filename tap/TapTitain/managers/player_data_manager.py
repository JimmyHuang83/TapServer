import datetime
import random
import hashlib
import config
from const_tables.const_value import ConstValue
from managers.database_manager import db_Manager
from models.game_tools import GameTools
from models.player import PlayerInfo
from models.message import ErrorCode

__author__ = 'Mike'
class PlayerDataManager:

    offlineInterval = datetime.timedelta(minutes = 5)
    def __init__(self):
        self.server_id = 0
        self.player_max_id = 0

        self.playerid2player = {}
        self.token2player = {}
        self.token2time = {}
        self.playerid2saveTime = {}
        self.lastCheckOutDateTime = 0

    def initData(self):
        tableName = 'id_info'
        fileds = 'server_id,player_max_id'
        data = db_Manager.selectDataFromTable(tableName, fileds)
        self.server_id = data[0][0]
        self.player_max_id = data[0][1]
        self.checkOutDateTime = datetime.datetime.now()

    def checkTokenOutDate(self):
        if datetime.datetime.now() > self.lastCheckOutDateTime + datetime.timedelta(seconds = ConstValue.tokenEffectTime):
            outDateTokens = []
            for (token,tokenTime) in self.token2time.items():
                if datetime.datetime.now() > tokenTime + datetime.timedelta(seconds = ConstValue.tokenEffectTime):
                    outDateTokens.append(token)

            self.kickOfTokens(outDateTokens)

    def kickOfTokens(self,tokens):
        for token in tokens:
            player = self.token2player.get(token)
            if player != None:
                playerid = player.player_id
                del self.playerid2player[playerid]
                del self.token2player[token]
                del self.token2time[token]
                del self.playerid2saveTime[playerid]
                player.saveData2DB()

    def isPlayerOnline(self,player_id):
        return  player_id in self.playerid2player.keys()

    def getPlayerByToken(self,token):
        if token in self.token2time:
            tokenTime = self.token2time[token]
            if GameTools.getDatetimeNow() > tokenTime + datetime.timedelta(seconds = ConstValue.tokenEffectTime):
                outDateTokens = []
                outDateTokens.append(token)
                self.kickOfTokens(outDateTokens)
                return  None
            else:
                player = self.token2player.get(token)
                if player != None:
                    self.updatePlayerTokenTime(player)
                    player.login_days_check()
                return  player


        return  None

    def getPlayerByPlayerid(self,player_id):
        player= self.playerid2player.get(player_id,None)
        if player != None:
            token = player.token
            tokenTime = self.token2time[token]
            if GameTools.getDatetimeNow() > tokenTime + datetime.timedelta(seconds = ConstValue.tokenEffectTime):
                outDateTokens = []
                outDateTokens.append(token)
                self.kickOfTokens(outDateTokens)
                return  None
            else:
                self.updatePlayerTokenTime(player)


        return player

    def isSign(self,udid):
        tableName = 'player_base_info'
        fileds = 'udid'
        condiction = "udid = '%s'"%udid
        data = db_Manager.selectDataFromTable(tableName, fileds, condiction)
        return len(data) > 0

    def isNameUsed(self,name):
        tableName = 'player_base_info'
        fileds = 'playerid'
        condiction = "name = '%s'" %name
        data = db_Manager.selectDataFromTable(tableName, fileds, condiction)
        return len(data) > 0

    def loginUseUidd(self,udid):
        tableName = 'player_base_info'
        fileds = 'playerid, name, pvp_medal, gem, ' \
                 'revive, cash, game_level, game_wave, ' \
                 'chanllenge_date, chanllenge_num, avatorid, lootequiplevel, is_brush, ' \
                 'last_cmd_time, random_reward_num, random_reward_date, ' \
                 'lastTimedRewardDatetime, last_timed_reward_ranknum, last_challenge_datetime, buy_del_challenge_cd_num,' \
                 'daily_datetime, add_chanllenge_num, awake_spell_num, last_free_draw_datetime, recharge_total_num, recharge_get_gifts_status,' \
                 'last_login_date, login_num, login_get_gifts_status, tutorial, udid'
        condiction = "udid = '%s'" %udid
        data = db_Manager.selectDataFromTable(tableName, fileds, condiction)
        player = PlayerInfo(data[0])
        self.playerid2player[player.player_id] = player
        self.token2player[player.token] = player
        self.token2time[player.token] = GameTools.getDatetimeNow()
        self.playerid2saveTime[player.player_id] = GameTools.getDatetimeNow()
        player.login_days_check()
        return player

    def checkNeedSave2DB(self,playerid):
        if GameTools.getDatetimeNow() > self.playerid2saveTime[playerid] + datetime.timedelta(minutes = 1):
            player = self.playerid2player[playerid]
            player.saveData2DB()
            self.playerid2saveTime[playerid] = GameTools.getDatetimeNow()

    def updatePlayerTokenTime(self,player):
        self.updateTokenTime(player.token)

    def updateTokenTime(self, token):
        self.token2time[token] = GameTools.getDatetimeNow()
        player = self.token2player[token]
        player.last_cmd_time = GameTools.getDateTimeNowString()

    def createAccount(self,udid,name):
        tableName = 'player_base_info'
        fields = []
        values = []
        fields.append('playerid')
        fields.append('udid')
        fields.append('name')
        fields.append('last_cmd_time')
        self.player_max_id += 1
        playerid = self.server_id + self.player_max_id
        values.append(playerid)
        values.append(udid)
        values.append(name)
        timeNowStr = GameTools.datetime2string(datetime.datetime.now())
        values.append(timeNowStr)
        db_Manager.insertIntoTable(tableName,fields,values)
        self.updatePlayerMaxID(self.player_max_id)
        # self.initNewPlayerSkill(playerid)
        # self.initNewPlayerPartner(playerid)
    #     self.createPlayerRankInfo(playerid)
    #
    # def createPlayerRankInfo(self,playerid):
    #     tableName = 'player_base_info'
    #     fields = "count( player_base_info.playerid)"
    #     data = db_Manager.selectDataFromTable(tableName,fields)
    #     playerCount = data[0][0]
    #     rankNum = playerCount
    #
    #     tableName = "player_ranking"
    #     fields = []
    #     values = []
    #     fields.append('rank_num')
    #     fields.append('playerid')
    #     values.append(rankNum)
    #     values.append(playerid)
    #     db_Manager.insertIntoTable(tableName,fields,values)
    #     rankManager.addRank(rankNum,playerid)

    def initNewPlayerSkill(self,player_id):

        tableName = "player_skill"

        for skillid in range(6):
            fields = []
            fields.append('player_id')
            fields.append('skill_id')
            fields.append('level')

            values = []
            values.append(player_id)
            values.append(skillid)
            values.append(0)
            db_Manager.insertIntoTable(tableName,fields,values,None)

    def initNewPlayerPartner(self,player_id):
        tableName = "player_partner"
        fields = []
        fields.append('player_id')
        fields.append('partner_id')
        fields.append('level')

        for partnerid in range(30):
            values = []
            values.append(player_id)
            values.append(partnerid)
            values.append(0)
            db_Manager.insertIntoTable(tableName,fields,values,None)

    def updatePlayerMaxID(self,maxID):
        tableName = 'id_info'
        fields = []
        values = []
        fields.append('player_max_id')
        fields.append('server_id')
        values.append(self.player_max_id)
        values.append(self.server_id)
        condition = "server_id = '%s'" % self.server_id
        db_Manager.updateDataAtTable(tableName,fields,values,condition)

    def sendPVPReward(self,playerid,type,value,rankNum):
        if value <= 0:
            value = -value
        value = int(value)
        player = self.playerid2player.get(playerid,None)
        if player == None:
            self.addNocachePlayerResource(playerid,type,value,rankNum)
        else:
            player.addResource(type,value)
            player.last_timed_reward_datetime = GameTools.getDateTimeNowString()
            player.last_timed_reward_ranknum = rankNum

    def setGetRewardInfo(self,rankNum,dateTime):
        pass

    def addNocachePlayerResource(self,playerid,type,value,rankNum):
        tableName = "player_base_info"
        filedName = "cash"
        if type == 1:
            filedName = "pvp_medal"
        elif type == 2:
            filedName = "gem"
        elif type == 3:
            filedName = "revive"
        elif type == 4:
            filedName = "cash"

        else:
            print("not conifg this resource %s"%type)
            return
        selectField = filedName
        condition = "playerid = %s" %playerid
        data = db_Manager.selectDataFromTable(tableName,selectField,condition)
        oldValue = int(data[0][0])
        newValue = oldValue + value

        insertField = []
        insertField.append(filedName)
        insertField.append('lastTimedRewardDatetime')
        insertField.append('last_timed_reward_ranknum')
        insertValue = []
        insertValue.append(newValue)
        insertValue.append(GameTools.getDateTimeNowString())
        insertValue.append(rankNum)
        db_Manager.updateDataAtTable(tableName,insertField,insertValue,condition)

    def create_connect_id(self, playerid):
        rand = random.randint(1000,9999)
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sum_data = "%d%s%d%s" %(playerid,time_str, rand, config.SECRET_KEY)
        return hashlib.md5(sum_data.encode('utf-8')).hexdigest()

    def check_connect_id(self, obj, post_connect_id):
        if obj.connect_id != post_connect_id:
            return False, ErrorCode.connect_id_error
        return True, 'success'
#
# save player data
    def savePlayerData2DB(self,num):
        playerDic = dict( (k,v) for k,v in self.playerid2player.items() if k % 60 == num)
        for player in playerDic.values():
            player.saveData2DB()


playerDataManager = PlayerDataManager()