import tornado.web
import  tornado.gen
from managers.player_data_manager import playerDataManager
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Mike'
class Equipment_upgradeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        id = params.get('id')
        to_quality = params.get('to_quality')
        to_level = params.get('to_level')
        buffs = params.get('bufList')
        costValue = params.get('costValue')
        player = playerDataManager.getPlayerByToken(token)
        returnData = MessData()

        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)

        else:
            # ���connect id���
            connect_id = params.get('connect_id', '')    # �������id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            errorCode = player.equipmentUpgrade(id,to_quality,to_level,buffs,costValue)
            if errorCode != None:
                returnData = MessData(errorCode)
            else:
                player.updatePVPBuffs()
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)