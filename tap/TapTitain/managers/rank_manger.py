import datetime
from const_tables.pickup_player_table import pickUpPlayersTable
from managers.database_manager import db_Manager
from managers.player_data_manager import playerDataManager
from models.game_tools import GameTools

from models.pvp.player_info_pvp import PvpPlayerInfoInRanking

__author__ = 'Mike'

class RankingManager:
    def __init__(self):
        self.rank_max_num = 0
        self.rank = {}
        self.lastSendRewardTime = GameTools.getDatetimeNow() - datetime.timedelta(days = 1)
        print('init rank')

    def checkPlayerInRanking(self,playerID):
        return playerID in self.rank.values()

    def pvpWin(self,attackerID,targetID):
        attackerNum = self.getRankNumByPlayerid(attackerID)
        targetNum = self.getRankNumByPlayerid(targetID)

        self.rank[attackerNum] = targetID
        self.rank[targetNum] = attackerID

        tableName = "player_ranking"
        fileds = []
        fileds.append('playerid')
        values = []
        values.append(targetID)
        condition = "rank_num = '%s'" % attackerNum
        db_Manager.updateDataAtTable(tableName,fileds,values,condition)

        values = []
        values.append(attackerID)
        condition = "rank_num = '%s'" % targetNum
        db_Manager.updateDataAtTable(tableName,fileds,values,condition)


    def initData(self):
        tableName = "player_ranking"
        fields = 'rank_num,playerid'

        data = db_Manager.selectDataFromTable(tableName,fields)
        for aData in data:
            self.rank[aData[0]] = aData[1]

        tableName = "id_info"
        fields = "rank_max_id"
        data = db_Manager.selectDataFromTable(tableName,fields)
        self.rank_max_num = data[0][0]

    def addRank(self, playerid):
        self.rank_max_num += 1
        self.rank[self.rank_max_num] = playerid
        tableName = "player_ranking"
        fields = []
        values = []
        fields.append('rank_num')
        fields.append('playerid')
        values.append(self.rank_max_num)
        values.append(playerid)
        db_Manager.insertIntoTable(tableName,fields,values)
        self.updateRankMaxNum()

    def updateRankMaxNum(self):
        from managers.player_data_manager import playerDataManager
        tableName = "id_info"
        fields = []
        values = []
        fields.append('rank_max_id')
        values.append(self.rank_max_num)
        condition = "server_id = '%s'" % playerDataManager.server_id
        db_Manager.updateDataAtTable(tableName,fields,values,condition)

    def getTopRankList(self):
        rankNums = []
        for index in range(1,51):
            rankNums.append(index)
        return  self.getPlayerListByRankNums(rankNums)

    def getRankNumByPlayerid(self,player_id):
        for (num,aplayerid) in self.rank.items():
            if player_id == aplayerid:
                return  num

    def getRankList(self,rankNum):
        rankNumList = pickUpPlayersTable.pickUpNum(rankNum)
        return  self.getPlayerListByRankNums(rankNumList)

    def getPlayerListByRankNums(self,rankNumList):
        playerIDList = []
        notInRankList = []
        for num in rankNumList:
            playerid = self.rank.get(num,None)
            if playerid == None:
                notInRankList.append(num)
                continue
            playerIDList.append(playerid)

        for remNum in notInRankList:
            rankNumList.remove(remNum)
        playerid2player = {}

        tableName = "player_base_info"
        fileds = "playerid,name,game_level,avatorid"
        if len(playerIDList) == 0:
            return  []
        players = []
        offlinePlayersid = []
        for playerid in playerIDList:
            playerInfo = playerDataManager.getPlayerByPlayerid(playerid)
            if playerInfo == None:
                offlinePlayersid.append(playerid)
            else:
                infos = []
                infos.append(playerid)
                infos.append(playerInfo.name)
                infos.append(playerInfo.game_level)
                infos.append(playerInfo.avatorid)
                pvpplayer = PvpPlayerInfoInRanking(infos)
                playerid2player[playerid] = pvpplayer

        if len(offlinePlayersid) > 0:#offline player
            playerIDList = str(offlinePlayersid)
            playerIDList = playerIDList[1:-1]
            condition = "playerid in (%s)" % playerIDList

            data = db_Manager.selectDataFromTable(tableName,fileds,condition)
            for aaData in data:
                player = PvpPlayerInfoInRanking(aaData)
                playerid2player[player.player_id] = player

        for num in rankNumList:
            playerid = self.rank[num]
            player = playerid2player[playerid]
            player.rankNum = num
            players.append(player)
        return  players

    def whetherRankChange(self,playerid,rankNum):
        return  self.rank[rankNum] != playerid

rankManager = RankingManager()




