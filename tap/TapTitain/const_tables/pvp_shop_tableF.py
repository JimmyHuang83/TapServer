__author__ = 'Mike'
from const_tables.item_tableF import  itemTable
from models.message import MessageTools, MessData, ErrorCode
from managers.database_manager import db_Manager
class PVPShopItem:
    def __init__(self,data):
        self.id = data[0]
        self.buy_item_id = data[1]  # reference item table id
        self.cost_type = data[2]
        self.cost_value = data[3]
        self.jump_ad = data[4]
        self.jump_time = data[5]



class PvpShopTable:
    def __init__(self):
        self.tableData = {}

    def initData(self):
        self.tableData.clear()
        tableName = "table_pvp_shop"
        fields = "id,buy_item_id,cost_type,cost_value,jump_ad,jump_time"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = PVPShopItem(oneData)
            self.tableData[item.id] = item

    def getItemConstInfo(self,itemID):
        return self.tableData.get(itemID,None)

    def playerShop(self,playerInfo,shopID,value,itemInfo = None):
        if not shopID in self.tableData.keys():
            return ErrorCode.shopIDError
        pvpShopItem = self.tableData[shopID]
        if playerInfo.costResource(pvpShopItem.cost_type,pvpShopItem.cost_value):
            itemID = pvpShopItem.buy_item_id
            item = itemTable.getItemConstInfo(itemID)
            if item.bodyid == 8:# resource
                playerInfo.addResource(item.buftype,value)
        else:
            return ErrorCode.resourceNotEnough

pvpShopTable = PvpShopTable()