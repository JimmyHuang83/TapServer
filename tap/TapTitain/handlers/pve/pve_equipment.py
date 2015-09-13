#coding=utf-8
import tornado.web
import tornado.gen
from const_tables.buff_table import buffTable
from const_tables.eqp_deputbuff_table import eqpDeputBuffsTableManager
from const_tables.gloabl_base_table import gloabalBase
from const_tables.item_tableF import itemTable
from const_tables.level_table import levelTable
from const_tables.scene import SceneTable
from const_tables.scene_loot_equiplist_table import sceneLootEquipTable
from managers.player_data_manager import playerDataManager
from models.equipment import EquipMent
from models.game_enum import ResourceType
from models.message import MessageTools, MessData, ErrorCode

__author__ = 'Mike'

# 掉落或者买装备
class GamePlayLootEquipmentHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)
        self._process(dictData)

    def _process(self, params):
        token = params.get('token')                 # 玩家token
        level = params.get('level')                 # 玩家当前关卡
        equipment = params.get('equipment')        # 装备信息
        isbuy = params.get('isbuy')                 # 是否通过购买
        luck_type = params.get('luck_type',0)      # 幸运类型
        reveialNum = params.get("reveial_num",0)    # 重生次数
        upgradeCost = 0

        player = playerDataManager.getPlayerByToken(token)          # 通过token获取玩家信息
        returnData = MessData()

        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)           # 未登陆
        else:
            # 玩家connect id检测
            connect_id = params.get('connect_id', '')      # 玩家连接id
            ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
            if ck_connectid[0] is False:
                returnData = MessData(ck_connectid[1])
                self.write(MessageTools.encode(returnData))
                self.finish()
                return

            plevel = player.game_level                              # 玩家关卡
            realReveialNum = player.getSkillInfo(7).skillLevel      # 玩家重生次数

            # 玩家重生次数验证
            if realReveialNum + 1 < reveialNum or reveialNum +1 < realReveialNum:
                    returnData = MessData(ErrorCode.verifyEquipmentLevel)

            # 玩家关卡验证
            elif not self.verifyLevel(level,plevel,reveialNum != realReveialNum):
                returnData = MessData(ErrorCode.levelNotMatch)

            # 通过
            else:
                m_level = level
                levelInfo = levelTable.getItem(level)               # 关卡信息
                costRevial = 0
                if isbuy == 1:                                      # 购买花费的重生币数量
                    costRevial = levelInfo.drawEquipCost
                # if m_level % 5 != 0 and isbuy == 0:
                #     returnData = MessData(ErrorCode.verifyEquipmentLevel)

                # elif level <= player.lootEquipLevel:
                #     returnData = MessData(ErrorCode.verifyEquipmentLevellow)
                # elif realReveialNum + 1 < reveialNum or reveialNum +1 < realReveialNum:
                #     returnData = MessData(ErrorCode.verifyEquipmentLevel)

                # 消耗重生币验证
                if player.revial >= costRevial:
                    if isbuy == 0:
                        player.lootEquipLevel = level

                    reveialNum = player.getSkillInfo(7).skillLevel
                    groupID = (player.player_id + reveialNum) % 10
                    sceneid = SceneTable.getSceneidByLevel(m_level,groupID)
                    equipmentid = equipment.get('equipmentid')
                    equipment['game_level'] = m_level
                    equipment['upgradeCost'] = upgradeCost
                    isLuck = False
                    newEquipment = EquipMent(equipment)

                    if player.getEquipmentByID(equipmentid):
                        returnData = MessData(ErrorCode.equipmentid_exist)
                        self.write(MessageTools.encode(returnData))
                        self.finish()
                        return

                    # 大奖 小奖验证
                    if luck_type == 1 or luck_type == 2:
                        isLuck = True
                    sceneInfo = player.scenesInfo[sceneid]
                    print ("====================================================")
                    print ('luck_type:%d, big_luck_num:%d, small_luck_num:%d' %(luck_type, sceneInfo.big_luck_num, sceneInfo.small_luck_num))
                    print ("====================================================")
                    if luck_type == 1 and sceneInfo.big_luck_num != 1:
                        returnData = MessData(ErrorCode.notLuckNumNow)

                    elif luck_type == 2 and sceneInfo.small_luck_num != 1:
                        returnData = MessData(ErrorCode.notLuckNumNow)

                    # 场景装备验证
                    elif sceneLootEquipTable.verifyEquipment(sceneid,equipmentid,level,isLuck):
                        # 装备buffType验证
                        if self.verifyBuffType(newEquipment):
                            # 装备buff验证
                            if self.verifyBuffValue(newEquipment):
                                sceneConstInfo = sceneLootEquipTable.getSceneConstInfo(sceneid)
                                error = player.addEquipment(newEquipment)

                                # 装备添加失败
                                if error != None:
                                    returnData = MessData(error)

                                # 重置保底值
                                else:
                                    if luck_type == 1 or luck_type == 3:
                                        sceneInfo.big_luck_num = sceneConstInfo.big_luck_num
                                        if sceneInfo.small_luck_num > 1:
                                            sceneInfo.small_luck_num -= 1
                                    elif luck_type == 2 or luck_type == 4:
                                        sceneInfo.small_luck_num = sceneConstInfo.small_luck_num
                                        if sceneInfo.big_luck_num > 1:
                                            sceneInfo.big_luck_num -= 1
                                    else:
                                        sceneInfo.big_luck_num -= 1
                                        sceneInfo.small_luck_num -= 1

                            else:
                                returnData = MessData(ErrorCode.verifyEquipmentBuffError)
                        else:
                            returnData = MessData(ErrorCode.verifyEquipmentBufftypeError)

                    else:
                        returnData = MessData(ErrorCode.verifyEquipment)
                    player.costResource(ResourceType.revial,costRevial)
                else:
                    returnData = MessData(ErrorCode.resourceNotEnough)
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            player.updatePVPBuffs()
            playerDataManager.checkNeedSave2DB(player.player_id)

    def verifyLevel(self,level,plevel,isReveial):
        return True

    def verifyBuffType(self,newEquipment):
        buffs = newEquipment.bufList
        deputBuffs = eqpDeputBuffsTableManager.GetDeputBuffList()
        for equipmentBuf in buffs:
            buffType = equipmentBuf.bufType
            buffValue = equipmentBuf.bufValue
            equipmentConstInfo = itemTable.getItemConstInfo(newEquipment.equipmentid)

            if equipmentBuf == buffs[0]:
                #main buff
                if equipmentBuf.bufType != equipmentConstInfo.buftype:
                    return False
            else:
                if equipmentBuf.bufType not in deputBuffs:
                    return False

        return  True

    def verifyBuffValue(self,newEquipment):
        buffs = newEquipment.bufList
        for buff in buffs:
            buffType = buff.bufType
            buffValue = buff.bufValue

            buffConstInfo = buffTable.getBuffConstInfo(buffType)
            levelModify = buffConstInfo.levelModify
            buffBaseValue = buffConstInfo.baseValue
            lootLevel = newEquipment.game_level
            buffConstMaxModify = gloabalBase.getValue("equipment_buff_maxrate")
            buffConstMaxModify += 20 #rong cuo
            maxValue = ( buffBaseValue + lootLevel * levelModify)  * buffConstMaxModify

            if buff != buffs[0]:
                deputyPropertyModify = buffConstInfo.discount
                maxValue *= deputyPropertyModify / 100
            if buffValue > maxValue:
                return False

        return True


class EquipEquipmentHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        token = dictData.get('token')
        id = dictData.get('id')
        pos = dictData.get('pos')
        returnData = MessData()

        # 玩家token检测
        player = playerDataManager.getPlayerByToken(token)
        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 玩家connect id检测
        connect_id = dictData.get('connect_id', '')    # 玩家连接id
        ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
        if ck_connectid[0] is False:
            returnData = MessData(ck_connectid[1])
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 获取装备信息
        equipMent = player.getEquipmentByID(id)
        if equipMent == None:
            returnData = MessData(ErrorCode.upgradeEqp_notHaveEqp)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 穿戴装备
        player.wearEquipment(from_pos=equipMent.pos,to_pos=pos)
        player.updatePVPBuffs()

        str = MessageTools.encode(returnData)
        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)


class TakeOffEquipmentHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        token = dictData.get('token')
        player = playerDataManager.getPlayerByToken(token)
        returnData = MessData()
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

            id = dictData.get('id')
            pos = dictData.get('from_pos')
            errorCode = player.takeOffEquipment(pos,id)
            if errorCode != None:
                returnData = MessData(errorCode)
            else:
                player.updatePVPBuffs()
        str = MessageTools.encode(returnData)

        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)


class SaleEquipmentHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        bodyData = self.request.body
        dictData = MessageTools.decode(bodyData)

        token = dictData.get('token')                               # 玩家token
        id = dictData.get('id',0)                                   # 装备ID
        use_gem = dictData.get('use_gem',0)                         # 消耗钻石数量
        saleNum = dictData.get('saleNum',0)                         # 分解装备获取的重生币
        returnData = MessData()

        # 玩家token检测
        player = playerDataManager.getPlayerByToken(token)
        if player == None:
            returnData = MessData(ErrorCode.tokenOutData)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 玩家connect id检测
        connect_id = dictData.get('connect_id', '')    # 玩家连接id
        ck_connectid = playerDataManager.check_connect_id(obj=player, post_connect_id=connect_id)
        if ck_connectid[0] is False:
            returnData = MessData(ck_connectid[1])
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 获取装备信息
        equipMent = player.getEquipmentByID(id)
        if equipMent == None:
            returnData = MessData(ErrorCode.upgradeEqp_notHaveEqp)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        levelConstInfo = levelTable.getItem(equipMent.game_level)   # 关卡掉了信息
        recValue = levelConstInfo.recycle                           # 分解基础价值
        upgradeValue = equipMent.upgradeCost                        # 升级价值
        totalValue = recValue + upgradeValue

        # 10倍价格容错检测
        if saleNum > totalValue * 10:
            returnData = MessData(ErrorCode.eqpSaleValueBig)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        # 钻石检测
        if not player.gems >= use_gem:
            returnData = MessData(ErrorCode.resourceNotEnough)
            self.write(MessageTools.encode(returnData))
            self.finish()
            return

        player.costResource(ResourceType.gems,use_gem)          # 扣除消耗
        player.delEquipment(equipMent)                          # 删除装备
        player.addResource(ResourceType.revial,saleNum)         # 增加复活币
        player.updatePVPBuffs()                                 # 修改pvpbuff

        str = MessageTools.encode(returnData)
        self.write(str)
        self.finish()
        if player != None:
            playerDataManager.checkNeedSave2DB(player.player_id)







