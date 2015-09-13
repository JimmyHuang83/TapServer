from managers.database_manager import db_Manager

__author__ = 'Mike'


def getMaxRankNum():
    tableName = "id_info"
    fields = "rank_max_id"
    data = db_Manager.selectDataFromTable(tableName, fields)
    max_num = data[0][0]
    return max_num


def insertPlayerInOrder(playerid, ranknum):
    tableName = "player_ranking"
    fields = []
    fields.append('rank_num')
    fields.append('playerid')
    value = []
    value.append(ranknum)
    value.append(playerid)
    db_Manager.insertIntoTable(tableName, fields, value)


max_rankNum = 0


def insertNonrankID():
    global max_rankNum
    cmd = "SELECT\
        playerid\
        FROM\
        player_base_info \
        WHERE player_base_info.playerid not in (SELECT player_ranking.playerid from player_ranking)\
        "

    data = db_Manager.excuteQuery(cmd)

    for oneData in data:
        player_id = oneData[0]
        rankTable = "player_ranking"
        fields = []
        values = []
        fields.append('playerid')
        fields.append('rank_num')
        values.append(player_id)
        max_rankNum += 1
        values.append(max_rankNum)

        db_Manager.insertIntoTable(rankTable, fields,  values)


def updateMaxRankNum():
    tableName = "id_info"
    fields = []
    values = []
    fields.append('rank_max_id')
    values.append(max_rankNum)
    db_Manager.updateDataAtTable(tableName, fields, values)


db_Manager.openDB()
max_rankNum = getMaxRankNum()
insertNonrankID()
updateMaxRankNum()
