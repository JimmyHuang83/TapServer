#coding=utf-8
import tornado.web
import tornado.gen
from managers.player_data_manager import playerDataManager
from models.message import MessageTools, MessData, ErrorCode
from const_tables.gloabl_base_table import gloabalBase

__author__ = 'Ryan Zhu'

# 释放技能
class UseSkillHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        params = MessageTools.decode(bodyData)
        token = params.get('token')

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

        # 钻石检测
        cost = gloabalBase.getValue('use_skill_cost')
        if player.gems < cost:
            returnData = MessData(ErrorCode.resourceNotEnough)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        player.gems -= cost

        str = MessageTools.encode(returnData)
        self.write(str)
        self.finish()

        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)