#coding=utf-8
import datetime
import tornado.web
import tornado.gen
from const_tables.gloabl_base_table import gloabalBase
from const_tables.illegal_word_manager import illegalWordManager
from managers.database_manager import db_Manager
from managers.player_data_manager import playerDataManager
from managers.pvp_data_manager import pvpDataManger
from models.game_tools import GameTools
from models.message import MessageTools, MessData, ErrorCode
from models.offline_cash import OfflineCash
import managers.account_cdkey_manage as AccountCDkey

__author__ = 'Mike'


# 登录
class LoginHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        udid = dictData['udid']
        returnData = None
        player = None

        playerID = self.getPlayeridByudid(udid)                         # 使用udid从数据库读取玩家ID
        if playerID == -1:
            returnData = MessData(ErrorCode.have_not_sign)              # 玩家未注册
        else:
            returnData = MessData()
            player = playerDataManager.getPlayerByPlayerid(playerID)    # 登录成功，使用playerid获取玩家信息

            if player == None:                                         # 玩家信息未在内存中从数据库读取
                player = playerDataManager.loginUseUidd(udid)
                player.connect_id = playerDataManager.create_connect_id(player.player_id)       # 重新生成连接ID
                returnData.data = player
                player.server_date_time = GameTools.getDateTimeNowString()
            else:
                player.connect_id = playerDataManager.create_connect_id(player.player_id)       # 重新生成连接ID
                returnData.data = player
                player.server_date_time = GameTools.getDateTimeNowString()


        if player != None:
            player.calculateOfflineResource()                           # 结算离线奖励

        message = MessageTools.encode(returnData,False)

        if player != None:                                             # 重置离线奖励
            player.offlineCash = 0

        self.write(message)
        self.finish()

    # 使用udid从数据库读取玩家ID
    def getPlayeridByudid(self,udid):
        tableName = 'player_base_info'
        fields = 'playerid'
        condition = "udid = '%s'"% udid
        data = db_Manager.selectDataFromTable(tableName,fields,condition)
        if len(data) == 0:
            return  -1
        else:
            return  data[0][0]

# 注册
class SignHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        udid = dictData['udid']
        name = dictData['name']
        cdkey = dictData.get('cdkey', '')
        returnData = MessData()
        player = None
        open_activate = True

        # 账户验证
        name = name.strip()
        contains = name.find(';') >= 0 or name.find(' ') > 0 or len(name) == 0
        charCount = len(name)
        max_length = gloabalBase.getValue('MAX_LENGTH_OF_NAME')
        max_length = int(max_length)

        # CDKEY验证
        if open_activate is True:
            cdkey = cdkey.lower()
            if not cdkey:
                returnData = MessData(ErrorCode.have_not_activate_cdkey)
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            cdkey_obj = AccountCDkey.get_cdkey(cdkey=cdkey)
            if not cdkey_obj:
                returnData = MessData(ErrorCode.activate_cdkey_error)
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            if cdkey_obj.is_use is True:
                returnData = MessData(ErrorCode.activate_cdkey_error)
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

        # 长度验证
        if contains or charCount > max_length:
            returnData = MessData(ErrorCode.name_illegal)

        # 非法字符验证
        elif illegalWordManager.ContainIllegalWord(name):
            returnData = MessData(ErrorCode.name_illegal)

        # 是否已被使用验证
        elif not playerDataManager.isSign(udid):
            if playerDataManager.isNameUsed(name):
                returnData = MessData(ErrorCode.name_used)
            else:
                playerDataManager.createAccount(udid,name)
                player = playerDataManager.loginUseUidd(udid)
                player.connect_id = playerDataManager.create_connect_id(player.player_id)       # 重新生成连接ID
                player.revial = 1
                returnData.data = player
                player.server_date_time = GameTools.getDateTimeNowString()

        # 通过
        else:
            player = playerDataManager.loginUseUidd(udid)
            player.server_date_time = GameTools.getDateTimeNowString()
            player.connect_id = playerDataManager.create_connect_id(player.player_id)       # 重新生成连接ID
            returnData.data = player
            player.calculateOfflineResource()

        message = MessageTools.encode(returnData,False)

        if player != None:                          # 重置离线奖励
            player.offlineCash = 0

            # 使用cdkey
            if open_activate is True:
                cdkey_obj.is_use = True
                cdkey_obj.usedtime = datetime.datetime.now()
                cdkey_obj.use_udid = udid
                cdkey_obj.save()

        self.write(message)
        self.finish()





