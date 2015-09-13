from managers.rank_manger import rankManager

__author__ = 'Mike'
import tornado.web
import tornado.gen
import static
from managers.player_data_manager import playerDataManager
from models.message import MessageTools, MessData, ErrorCode

class Skill_upgradeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        skillid = params.get('skill_id')
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

            errorCode = player.skillUpgrade(skillid,to_level)
            if errorCode != None:
                returnData = MessData(errorCode)

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)
            if skillid == 0:
                unlockPVPlEVEL = static.pvp_level_limit
                if to_level >= unlockPVPlEVEL and to_level < unlockPVPlEVEL + 3:
                    self.add2PVPRanking(player.player_id)

    def add2PVPRanking(self,playerID):
        if rankManager.checkPlayerInRanking(playerID):
            return
        else:
            rankManager.addRank(playerID)