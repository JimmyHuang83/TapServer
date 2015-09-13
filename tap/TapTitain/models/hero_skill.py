import datetime
from const_tables.hero_skill_table import heroSkillTableManager
from models.game_tools import GameTools

__author__ = 'Mike'
class HeroSkillData:
    def __init__(self,data):
        self.skillID = data[0]
        self.skillLevel = data[1]
        if data[2] == None or data[2] =="" or data[2] == " ":
            yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
            self.last_use_time = GameTools.datetime2string(yesterday)
        else:
            self.last_use_time = data[2]

    def IsEffectNow(self):
        if self.skillLevel == 0:
            return False
        lastUseTime = GameTools.string2datetime(self.last_use_time)
        skillConstInfo = heroSkillTableManager.getHeroSkill(self.skillID,self.skillLevel)
        effectTime = skillConstInfo.duration
        if effectTime == 0:
            effectTime += 10
        effectTime += 10
        t = datetime.timedelta(seconds = effectTime)
        return lastUseTime + t > datetime.datetime.now()
