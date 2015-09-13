#coding=utf-8
import tornado.web
import tornado.gen
from managers.player_data_manager import playerDataManager
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Mike'


# 客户端还是活跃状态，每隔一定时间发一次
class ClientActiveHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        token = dictData.get('token','')
        returnData = None

        player = playerDataManager.getPlayerByToken(token)          # 刷新在线时间
        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
        else:
            # 玩家connect id检测
            connect_id = dictData.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            returnData = MessData()


        message = MessageTools.encode(returnData)
        self.write(message)
        self.finish()

# 客户端主动退出
class ClientCloseHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        token = dictData.get('token')
        udid = dictData['udid']

        returnData = MessData()
        player = playerDataManager.getPlayerByToken(token)

        if player != None:
            # 玩家connect id检测
            connect_id = dictData.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            tokens = []
            tokens.append(token)
            playerDataManager.kickOfTokens(tokens)

        message = MessageTools.encode(returnData)
        self.write(message)
        self.finish()