import datetime
import tornado
from const_tables.draw_reward_table import drawRewardManager
from const_tables.gloabl_base_table import gloabalBase
from const_tables.item_tableF import itemTable
from managers.draw_history_manager import drawHistoryManager

from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.game_tools import GameTools
from models.message import MessageTools, ErrorCode, MessData

__author__ = 'Mike'
class DrawRewardHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        drawtimes = params.get('drawtimes',1)
        free_draw = params.get('free_draw',0)
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

            if free_draw == 1:
                if GameTools.getDatetimeNow() < GameTools.string2datetime(player.last_free_draw_datetime)  + datetime.timedelta(hours = 23):
                    returnData = MessData(ErrorCode.skillincd)
                    str = MessageTools.encode(returnData)

                    self.write(str)
                    self.finish()
                    if player != None:
                        playerDataManager.checkNeedSave2DB(player.player_id)
                    return
            cost = 0
            if drawtimes == 1:
                if free_draw == 0:
                    cost = int(gloabalBase.getValue('draw1cost'))
            else:
                cost = int(gloabalBase.getValue('draw10cost'))

            if player.costResource(ResourceType.gems,cost):
                if free_draw == 1:
                    player.last_free_draw_datetime = GameTools.getDateTimeNowString()

                rewards = []
                if drawtimes == 1:
                    rewards = drawRewardManager.draw1Reward(player.game_level)
                else:
                    rewards = drawRewardManager.draw10Reward(player.game_level)

                for resourceAndVlue in rewards:
                    itemid = resourceAndVlue.itemid
                    value = resourceAndVlue.value
                    item = itemTable.getItemConstInfo(itemid)
                    resourceId = item.buftype
                    player.addResource(resourceId,value)

                    if item.quliaty > 3:
                        drawHistoryManager.pushIntoHistory(player.name,resourceAndVlue)
                returnData.data = rewards
            else:
                returnData = MessData(ErrorCode.resourceNotEnough)
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)


