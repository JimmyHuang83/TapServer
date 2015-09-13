import datetime
import tornado.web
import tornado.gen
from const_tables.hero_skill_table import heroSkillTableManager
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.game_tools import GameTools
from models.message import MessageTools, MessData, ErrorCode


__author__ = 'Mike'


class CleanSkillCDHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        skillID = params.get('skill_id')
        cost = params.get('costValue')
        cost = int(cost)
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

            if player.costResource(ResourceType.gems,cost):
                heroSkillData = player.getSkillInfo(skillID)
                heroSkillData.last_use_time = GameTools.datetime2string(GameTools.getDatetimeNow() - datetime.timedelta(days=1))
            else:
                returnData = MessData(ErrorCode.resourceNotEnough)

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)

