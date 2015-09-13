#coding=utf-8
import tornado, json
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.message import MessageTools, ErrorCode, MessData
from const_tables.open_server import openServerTable
from handlers.account.login import LoginHandler
from managers.database_manager import db_Manager

__author__ = 'Ryan zhu'
class RechargeHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = eval(self.request.body.decode('utf-8'))
        data = {}
        data['udid'] = bodyData.get('udid', False)
        data['price'] = bodyData.get('price', False)
        self._process(data)

    # 购买钻石
    def _process(self, data):
        if data['udid'] is False or data['price'] is False:
            self.write({'result':-1, 'msg':'params error'})
            self.finish()
            return

        playerID = self.getPlayeridByudid(data['udid'])
        if playerID == -1:
            self.write({'result':-1, 'msg':'udid does not existd'})
            self.finish()
            return

        player = playerDataManager.getPlayerByPlayerid(playerID)
        if player == None:                                         # 玩家信息未在内存中从数据库读取
            player = playerDataManager.loginUseUidd(data['udid'])

        got_rmb_num = int(data['price'])               # 使用RMB数量
        got_gems_num = got_rmb_num*10                   # 添加钻石数量

        got_gems_num = int(got_gems_num)
        got_rmb_num = int(got_rmb_num)

        player.addResource(ResourceType.gems,got_gems_num)  # 添加资源

        # 更新玩家充值总数
        player.recharge_total_num += got_rmb_num

        self.write({'result':1, 'msg':got_gems_num})
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)    # 写入数据库


    def getPlayeridByudid(self,udid):
        tableName = 'player_base_info'
        fields = 'playerid'
        condition = "udid = '%s'"% udid
        data = db_Manager.selectDataFromTable(tableName,fields,condition)
        if len(data) == 0:
            return  -1
        else:
            return  data[0][0]