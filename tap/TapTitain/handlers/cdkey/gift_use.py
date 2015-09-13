#coding=utf-8
import tornado.web
import tornado.gen
import hashlib
import config
import requests
import json
from managers.player_data_manager import playerDataManager
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Ryan Zhu'


# 登录
class GiftUseHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        params = MessageTools.decode(bodyData)

        token = params.get('token')
        cdkey = params.get('cdkey','')

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

        # 使用cdkey
        cdkey_data = {}
        cdkey_data['cdkey'] = cdkey.strip()
        cdkey_data['udid'] = player.udid
        cdkey_data['server_id'] = config.serverConfigManager.server_id
        sum_data = "%s%s%d%s" %(cdkey_data['cdkey'], cdkey_data['udid'], cdkey_data['server_id'], config.SECRET_KEY)
        cdkey_data['sign'] = hashlib.md5(sum_data.encode('utf-8')).hexdigest()

        url = 'http://121.41.120.248/gift/use_cdkey/'
        req = requests.post(url, data=json.dumps(cdkey_data))
        req = json.loads(req.text)
        if req.get('error', False):
            returnData = MessData((820, "%s" % req['error']['data']['message']))
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # add tools
        for t in req['data']:
            player.addResource(t['tool_id'],t['count'])

        returnData.data = req['data']
        str = MessageTools.encode(returnData,False)
        self.write(str)
        self.finish()

        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)




