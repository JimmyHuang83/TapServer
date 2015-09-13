#coding=utf-8
import tornado.web
import tornado.gen
from managers.player_data_manager import playerDataManager
from models.message import MessageTools, MessData, ErrorCode
from const_tables.open_server import openServerTable
from const_tables.item_tableF import  itemTable

__author__ = 'Ryan Zhu'


# 登录
class LogoinRewordsAcceptHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        params = MessageTools.decode(bodyData)

        token = params.get('token')
        gift_no = params.get('gift_no',0)

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

        #奖励检测
        rewords = openServerTable.getOpeventServer(2, int(gift_no))
        if not rewords:
            returnData = MessData(ErrorCode.opeventLoginRewordsError)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 玩家礼包类型检测
        gift_status = player.login_get_gifts_status.get('%d' %rewords.condition, False)
        if gift_status is False:
            returnData = MessData(ErrorCode.opeventLoginRewordsTypeError)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 是否领取检测
        if int(gift_status) !=0:
            returnData = MessData(ErrorCode.opeventLoginRewordsStatusError)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 是否达到条件检测
        if player.login_num < rewords.condition:
            returnData = MessData(ErrorCode.opeventLoginRewordsCompletedError)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 添加奖励
        if rewords.item1>0:
            player.addResource(rewords.item1,rewords.num1)

        # 修改礼包状态
        player.login_get_gifts_status['%d' %rewords.condition] = 1

        str = MessageTools.encode(returnData)
        self.write(str)
        self.finish()

        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)




