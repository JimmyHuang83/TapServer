
import tornado
from const_tables.hero_table import heroTable
from const_tables.hero_unlock import heroUnlockTable
from const_tables.level_table import levelTable
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.message import MessageTools, ErrorCode, MessData

__author__ = 'Mike'
class AwakePartnerHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        partner_id = params.get('partner_id')

        playerInfo = playerDataManager.getPlayerByToken(token)
        returnData = MessData()

        if playerInfo == None:
            returnData = MessData(ErrorCode.tokenOutData)
        else:
            # 玩家connect id检测
            connect_id = params.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=playerInfo, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            partnerInfo = playerInfo.getPartner(partner_id)
            heroConstInfo = heroTable.GetHeroInfoByid(partner_id)
            awakeCost = heroConstInfo.awakeCost
            if playerInfo.costResource(ResourceType.awake_spell,awakeCost):
                partnerInfo.hp = heroConstInfo.max_hp
                partnerInfo.sleep = 0
            else:
                returnData = MessData(ErrorCode.resourceNotEnough)

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if playerInfo != None:
            playerDataManager.checkNeedSave2DB(playerInfo.player_id)