#coding=utf-8
import logging
import tornado.httpserver
from tornado.options import define
from config import serverConfigManager
from handlers.account.clientlife import ClientActiveHandler, ClientCloseHandler
from handlers.account.login import LoginHandler, SignHandler
from handlers.cd_bufs.clean_skill_cd import CleanSkillCDHandler
from handlers.cd_bufs.use_skill import PlayerUserSkill
from handlers.config.partner_config import Partner_ConfigHandler
from handlers.configs.config_handler import ConfigHandler
from handlers.meta_system.draw_reward_handler import DrawRewardHandler
from handlers.gm_tool.gm_tool_player import GM_KickofPlayerHandler
from handlers.meta_system.get_draw_history import GetDrawRewardHistoryHandler
from handlers.meta_system.rendom_reward_event_hanler import RandomRewardHandler
from handlers.partner.awake_partner import AwakePartnerHandler
from handlers.partner.partner_unlock import UnlockPartnerHandler
from handlers.pve.pve import GamePlayWinHandler, PvELoostHandler
from handlers.pve.pve_equipment import EquipEquipmentHandler, SaleEquipmentHandler, GamePlayLootEquipmentHandler, TakeOffEquipmentHandler
from handlers.pvp.add_chanllenge_num import AddChanllengeNumHandler
from handlers.pvp.clean_chanllenge_cd import CleanChanllengeHandler
from handlers.pvp.get_canfight_rank import  GetTargetPlayersHandler
from handlers.pvp.pvp import   PvPResultHandler
from handlers.pvp.pvp_attack import PVPAttackHandler
from handlers.pvp.pvp_fight_result import PVPFightResultListHandler
from handlers.pvp.pvp_rank_list import GetTopRankHandler
from handlers.pvp.pvp_timed_reward_handler import PVPTimedRewardHandler
from handlers.shop.gems2cash import Gems2CashHandler
from handlers.shop.iap import IapBuySuccessfullHandler
from handlers.shop.PlayerExchange import ExchangeHandler
from handlers.synchronization.synchronization_partner_hp import Synchronization_Partner_hpHandler
from handlers.time_event.pvp_time_reward import   ResrushPVPTimeRewardHandler
from handlers.upgrade.equipment_upgrade import Equipment_upgradeHandler
from handlers.upgrade.partner_upgrade import  Partner_upgradeHandler
from handlers.upgrade.skill_upgrade import Skill_upgradeHandler
from managers.const_table_manager import ConstTableManager
from managers.database_manager import db_Manager
from managers.player_data_manager import playerDataManager
from managers.rank_manger import rankManager
from models.log_config import LogConfing
from handlers.opevent.cumulative_recharge_accept import CumulativeRechargeAcceptHandler
from handlers.opevent.login_rewords_accept import LogoinRewordsAcceptHandler
from handlers.shop.recharge import RechargeHandler
from handlers.tutorial.finished import FinishedHandler
from handlers.partner.use_skill import UseSkillHandler
from handlers.cdkey.gift_use import GiftUseHandler

__author__ = 'Mike'

def init_game_data():
    db_Manager.openDB()
    playerDataManager.initData()
    rankManager.initData()
    ConstTableManager.loadConstTable()

    log = logging.getLogger("taptitan")
    server_init_ok = "server init ok: server id:%s port:%s"%(playerDataManager.server_id,serverConfigManager.getPort())
    logging.info(server_init_ok)
    print(server_init_ok)

def inifLogfile():
    LogConfing.initConfig()

def clear_server():
    import tools.clear_server

def create_robot():
    import tools.create_robot

def main():

    tornado.options.parse_command_line()
    inifLogfile()
    application = tornado.web.Application([
        (r"/account/login/?", LoginHandler),            # 登录
        (r"/account/signup/?"  , SignHandler),          # 注册

        (r"/client/active/?", ClientActiveHandler),     # 客户端还是活跃状态，每隔一定时间发一次
        (r"/client/close/?", ClientCloseHandler),       # 客户端主动退出

        (r"/pve/win/?", GamePlayWinHandler),            # pve胜利
        (r"/pve/loost/?", PvELoostHandler),             # pve失败

        (r"/equip/loot_equipment/?", GamePlayLootEquipmentHandler),     # 掉落或者买装备
        (r"/equip/equip_equipment/?", EquipEquipmentHandler),           # 把控槽位的装备装备到身上
        (r"/equip/sale_equipment/?", SaleEquipmentHandler),             # 卖装备
        (r"/equip/takeoff_equipment/?", TakeOffEquipmentHandler),      # 脱掉装备

        (r"/upgrade/equipment/?", Equipment_upgradeHandler),            # 装备升级
        (r"/upgrade/partner/?", Partner_upgradeHandler),                # 小伙伴升级
        (r"/upgrade/skill/?", Skill_upgradeHandler),                    # 技能升级

        (r"/partner/unlock/?", UnlockPartnerHandler),                   # 解锁小伙伴
        (r"/partner/awake/?", AwakePartnerHandler),                     # 小伙伴唤醒
        (r"/partner/useskill/?", UseSkillHandler),                      # 小伙伴使用技能

        (r"/use/skill/?", PlayerUserSkill),                             # 英雄使用技能
        (r"/clean/skillCD/?", CleanSkillCDHandler),                     # 清楚技能CD

        (r"/pvp/getTargetPlayers/?", GetTargetPlayersHandler),        # 获取pvp可攻打列表
        (r"/pvp/getTopRank/?", GetTopRankHandler),                     # 获取pvp前几名的列表
        (r"/pvp/attack/?", PVPAttackHandler),                          # 攻打某人
        (r"/pvp/result/?", PvPResultHandler),                          # 攻打结果
        (r"/pvp/getPVPTimedReward/?", PVPTimedRewardHandler),         # 领取pvp定时奖励，（现在是9点到12点每半小时领一次奖励）
        (r"/pvp/fight_result_list/?", PVPFightResultListHandler),     # 和自己相关的战斗记录列表，(也叫战斗日志)

        (r"/pvp/add_challenge_num/?", AddChanllengeNumHandler),      # 加每日的挑战次数
        (r"/pvp/clean_challenge_cd/?", CleanChanllengeHandler),      # 清楚挑战的cd

        (r"/shop/buy/?", ExchangeHandler),                            # 商店买东西，换东西
        (r"/shop/gems2cash/?", Gems2CashHandler),                    # 宝石换金币

        (r"/iap/buysuccessful/?", IapBuySuccessfullHandler),         # 内购(钻石)成功
        (r"/iap/recharge/?", RechargeHandler),                       # 购买成功
        (r"/config/partners/?", Partner_ConfigHandler),              # 配置上场的小伙伴

        # synchronization
        (r"/synchronization/partnershp/?", Synchronization_Partner_hpHandler),  # 同步小伙伴体力

        (r"/timer_server/refreshPVPReward/?", ResrushPVPTimeRewardHandler),    # 刷新pvp定时奖励，这个url开放给本地，不是客户端调用的

        (r"/gm/kickof/?", GM_KickofPlayerHandler),                               # gm 工具 把某人信息从内存中T掉
        (r"/reloaded/config/?", ConfigHandler),                                 # gm 工具， 重新读取策划配表

        # meta system
        (r"/reward/random_reward/?", RandomRewardHandler),                     # 随机奖励（tap tatian里面是小仙女奖励）
        (r"/reward/draw_reward/?", DrawRewardHandler),                         # 抽奖
        (r"/reward/better_draw_history/?", GetDrawRewardHistoryHandler),      # 抽到好东西的记录

        # opevent
        (r"/opevent/cumulative_Recharge_reward/?", CumulativeRechargeAcceptHandler),         # 累计充值活动奖励
        (r"/opevent/login_reward_accept/?", LogoinRewordsAcceptHandler),                      # 累计登录活动奖励

        # tutorial
        (r"/tutorial/finished/?", FinishedHandler),                                             # 完成新手引导

        # gift
        (r"/cdkey/gift_use/?", GiftUseHandler),            # 使用礼包码

        # for gm tools
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(serverConfigManager.getPort())
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    init_game_data()
    main()
    # create_robot()
    # clear_server()







