import tornado.web
import tornado.gen
import static
from const_tables.pickup_player_table import pickUpPlayersTable
from managers.player_data_manager import playerDataManager
from managers.rank_manger import rankManager
from models.message import MessageTools, MessData, ErrorCode
from managers.pvp_data_manager import  pvpDataManger
__author__ = 'Mike'
class GetTargetPlayersHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        bodyData = self.get_argument('data')
        print('data:%s' % bodyData)
        dictData = MessageTools.decode(bodyData)
        token = dictData.get('token')
        player = playerDataManager.getPlayerByToken(token)

        returnData = MessData()
        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
        elif player.getSkillInfo(7).skillLevel == 0 and player.getSkillInfo(0).skillLevel < static.pvp_level_limit:
            returnData = MessData(ErrorCode.pvpNOTUnlockNow)
        else:
            # 玩家connect id检测
            connect_id = dictData.get('connect_id', '')    # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            player_id = player.player_id
            if not rankManager.checkPlayerInRanking(player_id):
                rankManager.addRank(player_id)

            rank_num = rankManager.getRankNumByPlayerid(player_id)

            rankList = rankManager.getRankList(rank_num)
            pvpDataManger.addTargetList(player_id,rankList)
            # for pvpPlayerInfoInRanking in rankList:
            #     if pvpPlayerInfoInRanking.player_id == player_id:
            #         rankList.remove(pvpPlayerInfoInRanking)

            rankData = {}
            rankData['rank_num'] = rank_num
            rankData['rankList'] = rankList
            returnData.data = rankData
        str = MessageTools.encode(returnData,False)

        self.write(str)
        self.finish()



