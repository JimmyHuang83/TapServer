#coding=utf-8
import tornado
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.message import MessageTools, ErrorCode, MessData
from const_tables.open_server import openServerTable

__author__ = 'Mike'
class IapBuySuccessfullHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        self._process(dictData)

    # 购买钻石
    def _process(self, params):
        token = params.get('token')                             # token验证
        got_gems_num = params.get('got_gems_num')              # 添加钻石数量
        got_rmb_num = params.get('got_rmb_num')                # 使用RMB数量
        got_gems_num = int(got_gems_num)
        got_rmb_num = int(got_rmb_num)
        player = playerDataManager.getPlayerByToken(token)      # 根据token获取玩家信息
        returnData = MessData()                                 # 初始化返回信息

        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)       #玩家未登陆
        else:
            # 玩家connect id检测
            connect_id = params.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            player.addResource(ResourceType.gems,got_gems_num)  # 添加资源

            # 更新玩家充值总数
            player.recharge_total_num += got_rmb_num

        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)    # 写入数据库