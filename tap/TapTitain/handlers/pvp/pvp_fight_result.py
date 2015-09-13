import tornado.web
import tornado.gen
import static
from const_tables.pickup_player_table import pickUpPlayersTable
from managers.database_manager import db_Manager
from managers.player_data_manager import playerDataManager
from managers.rank_manger import rankManager
from models.game_enum import ResourceType
from models.message import MessageTools, MessData, ErrorCode


class FightResult:
    def __init__(self,data):
        self.id = data[0]
        self.attack_id = data[1]
        self.target_id = data[2]
        self.result = data[3]
        self.attacker_num = data[4]
        self.target_num = data[5]
        self.lowRank = data[6]
        self.attack_name = data[7]
        self.target_name = data[8]

__author__ = 'Mike'
class PVPFightResultListHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData  = self.request.body
        dictData = MessageTools.decode(bodyData)
        token = dictData.get('token')
        player = playerDataManager.getPlayerByToken(token)

        returnData = MessData()
        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
        elif player.getSkillInfo(7).skillLevel == 0 and player.getSkillInfo(0).skillLevel < static.pvp_level_limit:
            returnData = MessData(ErrorCode.pvpNOTUnlockNow)
        else:
            # 玩家connect id检测
            connect_id = dictData.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            player_id = player.player_id
            cmd ="SELECT\
                result.id,\
                result.attacker_id,\
                result.target_id,\
                result.result,\
                result.attacker_num,\
                result.target_num ,\
                result.fight_low,\
                player1.`name`,\
                player2.`name`\
                FROM\
                player_fight_result as result ,player_base_info as player1,player_base_info as player2\
                WHERE (result.attacker_id = %s or result.target_id = %s )and result.attacker_id = player1.playerid and result.target_id = player2.playerid\
                ORDER BY result.id\
                DESC\
                LIMIT 5" %(player_id,player_id)


            data = db_Manager.excuteQuery(cmd)
            returnData.data = []
            for resultData in data:
                fightResult = FightResult(resultData)
                returnData.data.append(fightResult)
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()