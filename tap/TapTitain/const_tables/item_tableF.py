from managers.database_manager import db_Manager

__author__ = 'Mike'
class Item():
    def __init__(self,data):
        self.id = data[0]
        self.bodyid = data[1]
        self.needlevel = data[2]
        self.quliaty = data[3]
        self.cansale = data[4]
        self.caletype = data[5]
        self.buftype = data[6]
        self.buffValue = data[7]


class ItemTable:
    def __init__(self):
        self.tableData = {}

    def initTable(self):
        self.tableData.clear()
        tableName = "table_items"
        fields = "id,bodyid,needlevel,quliaty,cansale,saletype,EffType,value"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = Item(oneData)
            self.tableData[item.id] = item

    def getItemConstInfo(self,itemID):
        return self.tableData.get(itemID,None)

itemTable = ItemTable()