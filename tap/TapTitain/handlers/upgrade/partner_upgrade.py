import tornado.web
import  tornado.gen
from managers.player_data_manager import playerDataManager
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Mike'
class Partner_upgradeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        partner_id = params.get('partner_id')
        to_level = params.get('to_level')
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

            errCode = player.partnerUpgrade(partner_id,to_level)
            if errCode != None:
                returnData = MessData(errCode)

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            player.updatePVPBuffs()
            playerDataManager.checkNeedSave2DB(player.player_id)





