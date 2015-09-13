from managers.database_manager import db_Manager

__author__ = 'Mike'
class HeroSkill:
    def __init__(self,data):
        self.table_hero_skill_id = data[0]
        self.skill_level = data[1]
        self.unlock_level = data[2]
        self.upcost = int(data[3])
        self.type = data[4]
        self.cd = data[5]
        self.duration = data[6]
        self.trigglerate = data[7]
        self.applytimes =data[8]
        self.applytarget = data[9]
        self.applaytargetnum = data[10]
        self.effecttype0 = data[11]
        self.effectvalue0 = data[12]
        self.bufvalue = data[13]
        self.spawnnewid = data[14]

class HeroSkillManager:
    def __init__(self):
        self.tables = {}


    def initData(self):
        self.tables.clear()
        tableName = "table_hero_skill"
        fields = "skillid,skill_level,unlock_level,upcost,type,cd,duration,trigglerate,applytimes,applytarget,ApplyTargetNum,effecttype0,effectvalue0,buffvalue0,spawnnewid"
        data = db_Manager.selectDataFromTable(tableName,fields)
        for skillData in data:
            heroSkill = HeroSkill(skillData)
            self.tables[(heroSkill.table_hero_skill_id,heroSkill.skill_level)] = heroSkill

    def getHeroSkill(self,skillid,level):

        return  self.tables[(skillid,level)]

heroSkillTableManager = HeroSkillManager()