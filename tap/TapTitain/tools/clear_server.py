#coding=utf-8
from managers.database_manager import db_Manager

db_Manager.openDB()
print ("===================================")

sql = "UPDATE `id_info` SET `player_max_id`='0', `rank_max_id`='0'"
db_Manager.excuteQuery(sql)
print ('id_info clear success')

sql = "UPDATE `table_account_cdkey` SET `is_use`='0', `usedtime`=NULL, `use_udid`=''"
db_Manager.excuteQuery(sql)
print ('table_account_cdkey clear success')

sql = "TRUNCATE TABLE `player_equip`"
db_Manager.excuteQuery(sql)
print ('player_equip clear success')

sql = "TRUNCATE TABLE `player_fight_result`"
db_Manager.excuteQuery(sql)
print ('player_fight_result clear success')

sql = "TRUNCATE TABLE `player_messages`"
db_Manager.excuteQuery(sql)
print ('player_messages clear success')

sql = "TRUNCATE TABLE `player_partner`"
db_Manager.excuteQuery(sql)
print ('player_partner clear success')

sql = "TRUNCATE TABLE `player_pvp_buffs`"
db_Manager.excuteQuery(sql)
print ('player_pvp_buffs clear success')

sql = "TRUNCATE TABLE `player_ranking`"
db_Manager.excuteQuery(sql)
print ('player_ranking clear success')

sql = "TRUNCATE TABLE `player_scene`"
db_Manager.excuteQuery(sql)
print ('player_scene clear success')

sql = "TRUNCATE TABLE `player_selected_partner`"
db_Manager.excuteQuery(sql)
print ('player_selected_partner clear success')

sql = "TRUNCATE TABLE `player_skill`"
db_Manager.excuteQuery(sql)
print ('player_skill clear success')

sql = "DELETE FROM `player_base_info`"
db_Manager.excuteQuery(sql)
print ('player_base_info clear success')

print ("===================================")