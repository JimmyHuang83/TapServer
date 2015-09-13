import tornado
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.game_tools import GameTools
from models.message import MessageTools, MessData, ErrorCode
from const_tables.pvp_shop_tableF import pvpShopTable
__author__ = 'Mike'

class ExchangeHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        shop_id = params.get('shop_id')
        value = params.get('value',0)
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

            error = pvpShopTable.playerShop(player,shop_id,value)
            if error != None:
                returnData = MessData(error)

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)