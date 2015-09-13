import datetime
import tornado.web
import tornado.gen
import static
from const_tables.pickup_player_table import pickUpPlayersTable
from managers.player_data_manager import playerDataManager
from managers.rank_manger import rankManager
from models.game_enum import ResourceType
from models.game_tools import GameTools
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Mike'
class CleanChanllengeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        token = dictData.get('token')
        player = playerDataManager.getPlayerByToken(token)

        returnData = MessData()
        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
        elif player.getSkillInfo(7).skillLevel == 0 and player.getSkillInfo(0).skillLevel < static.pvp_level_limit:
            returnData = MessData(ErrorCode.pvpNOTUnlockNow)
        else:
            # ���connect id���
            connect_id = dictData.get('connect_id', '')    # �������id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            player_id = player.player_id
            if not rankManager.checkPlayerInRanking(player_id):
                rankManager.addRank(player_id)
            if player.costResource(ResourceType.gems,10):
                player.last_challenge_datetime = GameTools.datetime2string(GameTools.getDatetimeNow() - datetime.timedelta(minutes = 20))
            else:
                returnData = MessData(ErrorCode.resourceNotEnough)
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()