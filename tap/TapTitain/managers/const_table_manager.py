from const_tables.buff_table import buffTable
from const_tables.draw_reward_table import drawRewardManager
from const_tables.eqp_deputbuff_table import eqpDeputBuffsTableManager
from const_tables.equipment_set import equipmentSetTable
from const_tables.equipment_upgrade_table import equipmentUpgradeTable
from const_tables.gloabl_base_table import gloabalBase
from const_tables.hero_skill_table import heroSkillTableManager
from const_tables.hero_table import heroTable
from const_tables.hero_unlock import heroUnlockTable
from const_tables.illegal_word_manager import illegalWordManager
from const_tables.itemDropListTable import equipListTable
from const_tables.item_tableF import itemTable
from const_tables.level2sceneid_table import level2sceneManager
from const_tables.level_table import levelTable
from const_tables.pickup_player_table import pickUpPlayersTable
from const_tables.pvp_fight_reward import pvpFightRewardTable
from const_tables.pvprank_timer_reward_table import pvpRankTimerRewardTable
from const_tables.random_reward_table import randomRewardManager
from const_tables.scene_loot_equiplist_table import sceneLootEquipTable
from const_tables.table_eqp_quality_upgrade import equipmentQtyUpgradeTable
from const_tables.upgrade_hero_table import heroUpgradeTable
from const_tables.upgrade_parter_table import partnerUpgradeTable
from const_tables.pvp_shop_tableF import pvpShopTable
from const_tables.open_server import openServerTable

__author__ = 'Mike'
class ConstTableManager:

    @staticmethod
    def loadConstTable():

        gloabalBase.initTable()
        heroSkillTableManager.initData()
        buffTable.initTable()
        itemTable.initTable()
        equipListTable.initTable()
        sceneLootEquipTable.initTable()
        heroUpgradeTable.initData()
        partnerUpgradeTable.initData()
        heroTable.initTable()
        heroUnlockTable.initTable()
        levelTable.initData()
        equipmentSetTable.initTable()
        level2sceneManager.initData()
        equipmentQtyUpgradeTable.initTable()
        equipmentUpgradeTable.initTable()
        eqpDeputBuffsTableManager.initTable()
        illegalWordManager.initTable()
        randomRewardManager.initData()
        pickUpPlayersTable.initData()
        pvpRankTimerRewardTable.initData()
        pvpFightRewardTable.initData()
        pvpShopTable.initData()
#        drawRewardManager.initData()
#        openServerTable.initData()
