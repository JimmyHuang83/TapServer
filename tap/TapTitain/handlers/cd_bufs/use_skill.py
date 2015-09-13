import datetime
import tornado.web
import tornado.gen
from const_tables.hero_skill_table import heroSkillTableManager
from managers.player_data_manager import playerDataManager
from models.game_tools import GameTools
from models.message import MessageTools, MessData, ErrorCode


__author__ = 'Mike'


class PlayerUserSkill(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)

    def _process(self, params):
        token = params.get('token')
        skillID = params.get('skillid')
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

            playerSkillInfo = player.getSkillInfo(skillID)
            skillLevel = playerSkillInfo.skillLevel
            lastUseTimeStr = playerSkillInfo.last_use_time
            lastUseTime = GameTools.string2datetime(lastUseTimeStr)
            skillConstInfo = heroSkillTableManager.getHeroSkill(skillID,skillLevel)
            cd = skillConstInfo.cd
            errCode = player.useSkill(skillID)
            # if GameTools.getDatetimeNow() + datetime.timedelta(seconds = 90) >= lastUseTime + datetime.timedelta(seconds = cd):
            #     errCode = player.useSkill(skillID)
            # else:
            #     returnData = MessData(ErrorCode.skillincd)
                #in cd

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)