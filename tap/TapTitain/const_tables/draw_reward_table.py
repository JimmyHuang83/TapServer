from const_tables.item_tableF import itemTable
from const_tables.level_table import levelTable
from managers.database_manager import db_Manager

import random
from models.game_enum import ResourceType

__author__ = 'Mike'

class ResourceAndVlue:
    def __init__(self,data):
        self.itemid = data[0]
        self.value = data[1]

class DrawReward:
    def __init__(self,data):
        self.id = data[0]
        self.itemid = data[1]
        self.weight = data[2]
        self.from_num = int(data[3])
        self.to_num = data[4]
        self.super = data[5]

    def randomValue(self, level):
        value = random.randint(self.from_num,self.to_num)
        level_info = levelTable.getItem(level)
        draw = itemTable.getItemConstInfo(self.itemid)
        if draw.buftype ==  ResourceType.cash:
            value *= level_info.monstercoins*draw.buffValue
        elif draw.buftype == ResourceType.revial:
            value *= level_info.recycle*draw.buffValue
        elif draw.buftype == ResourceType.awake_spell:
            value *= draw.buffValue
        return ResourceAndVlue((self.itemid,value))

class DrawRewardManager:
    def __init__(self):
        self.tables = []
        self.weightSum = 0

    def initData(self):
        self.tables.clear()
        self.weightSum = 0
        tableName = "table_draw_reward"
        fields = "id,itemid,weight,from_num,to_num,super"
        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = DrawReward(oneData)
            self.tables.append(item)
            self.weightSum += item.weight

    def supderDraw(self, level):
        weightSum = 0
        for drawReward in self.tables:
            if drawReward.super == 1:
                weightSum += drawReward.weight
        randNum = random.randint(1,weightSum)

        sum = 0
        for drawReward in self.tables:
            if drawReward.super == 1:
                sum += drawReward.weight
                if sum >= randNum:
                    return  drawReward.randomValue(level)

    def draw1Reward(self, level):
        rewards = []
        weightSum = self.weightSum
        randNum = random.randint(1,weightSum)

        sum = 0
        for drawReward in self.tables:
            sum += drawReward.weight
            if sum >= randNum:
                rewards.append(drawReward.randomValue(level))
                return rewards

    def draw10Reward(self, level):
        rewards = []
        rewards.append(self.supderDraw(level))
        for index in range(9):
            rewards.append(self.draw1Reward(level)[0])
        return rewards


drawRewardManager = DrawRewardManager()