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
        timeNow = GameTools.getDatetimeNow()                            # ��ǰʱ��
        rank = rankManager.rank                                         # pvp����

        # ���·���ʱ��
        rankManager.lastSendRewardTime = timeNow
        for (rankNum, playerid) in rank.items():

            # ��ȡ������Ϣ
            pvpRankTimerReward = pvpRankTimerRewardTable.getRewardByRankNum(rankNum)
            rewardType = pvpRankTimerReward.type
            rewardValue = pvpRankTimerReward.value

            # ���ͽ���0
            playerDataManager.sendPVPReward(playerid,rewardType,rewardValue,rankNum)

            # ���ͽ���1
            type1 = pvpRankTimerReward.type1
            value1 = pvpRankTimerReward.value1
            if value1 > 0:
                playerDataManager.sendPVPReward(playerid,type1,value1,rankNum)

        self.write('send reward time : %s' %(timeNow))
        self.finish()
