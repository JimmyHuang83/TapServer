import tornado.web
import  tornado.gen
from managers.player_data_manager import playerDataManager
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Mike'
class SendMessageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)
        self.finish()
    def _process(self, params):
        token = params.get('token')
        pos = params.get('pos')
        equipment_id = params.get('equipmentid')
        to_quality = params.get('to_quality')
        to_level = params.get('to_level')
        player = playerDataManager.getPlayerByToken(token)
        returnData = MessData()

        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)

        elif  player.equipmentUpgrade(pos,equipment_id,to_quality,to_level) != 0:
            returnData = MessData(ErrorCode.equipmentUpgradeError)

        # 玩家connect id检测
        connect_id = params.get('connect_id', '')    # 玩家连接id
        ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
        if ck_connectid[0] is False:
            returnData = MessData(ck_connectid[1])
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)