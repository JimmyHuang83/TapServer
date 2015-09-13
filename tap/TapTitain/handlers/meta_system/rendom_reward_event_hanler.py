import tornado.web
import  tornado.gen
from const_tables.gloabl_base_table import gloabalBase
from const_tables.random_reward_table import randomRewardManager
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Mike'
class RandomRewardHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        reward_type = params.get('reward_type')
        addValue = params.get('add_value')
        addValue = int (addValue)
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

            value = randomRewardManager.getValue(reward_type)
            # verify addValue at here!

            value = addValue
            max_time = gloabalBase.getValue('RandomRewardDailyMaxTimes')
            player.refreshTimeData()
            if player.random_reward_num < max_time:

                if reward_type ==1 or reward_type == 3:
                    player.addResource(ResourceType.cash,value)
                elif reward_type == 2 or reward_type == 4:
                    player.addResource(ResourceType.gems,value)
                player.random_reward_num += 1

            else:
                returnData = MessData(ErrorCode.resourceNotEnough)
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)