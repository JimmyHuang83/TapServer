import tornado
from const_tables.pvprank_timer_reward_table import pvpRankTimerRewardTable
from managers.player_data_manager import playerDataManager
from managers.rank_manger import rankManager
from models.game_tools import GameTools

__author__ = 'Mike'


class ResrushPVPTimeRewardHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        timeNow = GameTools.getDatetimeNow()                            # 当前时间
        rank = rankManager.rank                                         # pvp排行

        # 更新发送时间
        rankManager.lastSendRewardTime = timeNow
        for (rankNum, playerid) in rank.items():

            # 获取奖励信息
            pvpRankTimerReward = pvpRankTimerRewardTable.getRewardByRankNum(rankNum)
            rewardType = pvpRankTimerReward.type
            rewardValue = pvpRankTimerReward.value

            # 发送奖励0
            playerDataManager.sendPVPReward(playerid,rewardType,rewardValue,rankNum)

            # 发送奖励1
            type1 = pvpRankTimerReward.type1
            value1 = pvpRankTimerReward.value1
            if value1 > 0:
                playerDataManager.sendPVPReward(playerid,type1,value1,rankNum)

        self.write('send reward time : %s' %(timeNow))
        self.finish()
