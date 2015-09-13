#coding=utf-8
import tornado.web
import tornado.gen
from managers.player_data_manager import playerDataManager
from models.message import MessageTools, MessData, ErrorCode
from const_tables.open_server import openServerTable
from const_tables.item_tableF import  itemTable

__author__ = 'Ryan Zhu'


# 新手引导
class FinishedHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        params = MessageTools.decode(bodyData)

        token = params.get('token')
        step = params.get('step','')

        player = playerDataManager.getPlayerByToken(token)
        returnData = MessData()

        # 玩家登录检测
        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 玩家connect id检测
        connect_id = params.get('connect_id', '')    # 玩家连接id
        ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
        if ck_connectid[0] is False:
            returnData = MessData(ck_connectid[1])
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 步骤检测
        try:
            tutorial = getattr(player, step)
        except:
            returnData = MessData(ErrorCode.tutorialStepError)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 步骤状态检测
        if tutorial != 1:
            setattr(player, step, 1)
            if player != None:
                playerDataManager.checkNeedSave2DB(player.player_id)

        str = MessageTools.encode(returnData)
        self.write(str)
        self.finish()





