from managers.database_manager import db_Manager

__author__ = 'Mike'
class HeroInfo:
    def __init__(self,data):
        self.heroID = data[0]
        self.atkInterval = data[1]
        self.dps = data[2]
        self.propmodify = float(data[3])
        skillstr = data[4]
        skills_str = skillstr.split(',')
        self.skillsid =[]
        if skills_str != "0":
            for skillIDStr in skills_str:
                skillID = int(skillIDStr)
                self.skillsid.append(skillID)
        self.upgradeCostModify = float(data[5])
        self.costType = int(data[6])
        self.costValue = int(data[7])
        self.max_hp = int(data[8])
        self.sub_hp = int(data[9])
        self.add_hp = int(data[10])
        self.awakeCost = int(data[11])

class HeroTable:
    def __init__(self):
        self.tableData = {}

    def initTable(self):
        self.tableData.clear()
        tableName = "table_hero"
        fields = "id,atkinterval,dps,propmodify,skills,upgrade_cost_modify," \
                 "cost_type,cost_value,hp,sub_hp,add_hp,awake_cost"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = HeroInfo(oneData)
            self.tableData[item.heroID] = item

    def GetHeroInfoByid(self,heroid):
        return  self.tableData[heroid]

    def getPartnersCount(self):
        tableRowNum = len(self.tableData)
        return  tableRowNum -1

heroTable = HeroTable()