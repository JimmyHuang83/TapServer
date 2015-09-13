from const_tables.level2sceneid_table import level2sceneManager

__author__ = 'Mike'
class SceneTable :

    @staticmethod
    def getSceneidByLevel(levelid,groupid):
        num = (levelid -1) // 5
        return  level2sceneManager.getScene(num,groupid)

