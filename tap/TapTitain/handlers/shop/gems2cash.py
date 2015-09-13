import tornado
from const_tables.level_table import levelTable
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.message import MessageTools, ErrorCode, MessData

__author__ = 'Mike'
class Gems2CashHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        game_level = params.get('game_level')
        got_gems_num = params.get('revial_num')
        add_cash = params.get('add_cash')
        add_cash = int(add_cash)

        got_gems_num = int(got_gems_num)
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

            if not self.verifyLevelInfo(game_level,got_gems_num,player,add_cash):
                returnData = MessData(ErrorCode.shopVerifyError)
            else:
                if player.costResource(ResourceType.gems,100):
                    player.addResource(ResourceType.cash,add_cash)
                else:
                    returnData = MessData(ErrorCode.resourceNotEnough)
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)

    def verifyLevelInfo(self,game_level,revial_num,player,add_cash):
        levelInfo = levelTable.getItem(game_level)
        monsterCash  = levelInfo.monstercoins
        if monsterCash * 5000 + 10 < add_cash:
            return False

        if game_level <= player.game_level + 1:
            return True

        if revial_num == player.getSkillInfo(7).skillLevel - 1 and player.game_level == 1:
            return True

        return False
