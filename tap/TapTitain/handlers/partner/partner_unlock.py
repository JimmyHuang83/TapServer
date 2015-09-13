
import tornado
from const_tables.hero_table import heroTable
from const_tables.hero_unlock import heroUnlockTable
from const_tables.level_table import levelTable
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.message import MessageTools, ErrorCode, MessData

__author__ = 'Mike'
class UnlockPartnerHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        partner_id = params.get('partner_id')
        order_num = params.get('order_num',1)

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

            errorCode = self.unlockPartner(player,partner_id,order_num)
            returnData = MessData(errorCode)

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)


    def unlockPartner(self,player,partner_id,order_num):
        partner = player.getPartner(partner_id)
        costType = 3
        costValue = 0
        heroInfo = heroTable.GetHeroInfoByid(partner_id)
        if partner.hadBeenUnlocked == 1:
            costType = ResourceType.cash

            costValue = heroUnlockTable.getHeroUnlockInfoByOrder(order_num).cost

        else:

            costType = heroInfo.costType
            costValue = heroInfo.costValue

            if costType == ResourceType.cash:
                costValue = heroUnlockTable.getHeroUnlockInfoByOrder(order_num).cost

        if player.costResource(costType, costValue):
            partner.hadBeenUnlocked = 1
            partner.partner_level = max(1,partner.partner_level)
            partner.order = order_num
            partner.sleep = 0
            partner.hp = heroInfo.max_hp
        else:
            return ErrorCode.resourceNotEnough


