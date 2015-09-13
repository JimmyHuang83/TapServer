import socket
import tornado.web
import tornado.gen
from managers.player_data_manager import playerDataManager
from models.game_enum import ResourceType
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Mike'
class GM_KickofPlayerHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        client_IP = self.request.remote_ip
        localIP = socket.gethostbyname(socket.gethostname())
        print("client_IP:%s" %client_IP)
        print("localIP:%s" %localIP)
        if client_IP == localIP or client_IP == "127.0.0.1":

            bodyData = self.request.body
            playerid = bodyData.decode('utf-8')#to string
            self._process(playerid)

        self.finish()
    def _process(self, params):
        playerid = params
        playerid = int(playerid)
        player = playerDataManager.getPlayerByPlayerid(playerid)
        if player !=None:
            tokens = []
            tokens.append(player.token)
            playerDataManager.kickOfTokens(tokens)

        str = 'ok'
        print('ok')
        self.write(str)