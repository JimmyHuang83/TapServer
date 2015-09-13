import tornado.web
import tornado.gen
import static
from const_tables.pickup_player_table import pickUpPlayersTable
from managers.player_data_manager import playerDataManager
from managers.rank_manger import rankManager
from models.game_enum import ResourceType
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Mike'
class AddChanllengeNumHandler(tornado.web.RequestHandler):
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
            # 玩家connect id检测
            connect_id = dictData.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            addChanllengeNum = player.add_chanllenge_num
            addChanllengeNum += 1

            costGems = addChanllengeNum * 10

            if player.costResource(ResourceType.gems, costGems):
                player.add_chanllenge_num = addChanllengeNum
                player.chanllenge_num += 1
            else:
                returnData = MessData(ErrorCode.resourceNotEnough)
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()