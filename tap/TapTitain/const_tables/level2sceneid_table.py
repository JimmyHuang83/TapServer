from managers.database_manager import db_Manager

__author__ = 'Mike'
class SceneInfo_Const:
    def __init__(self,data):
        self.num = data[0]
        self.sceneids = []
        self.sceneids.append(data[1])
        self.sceneids.append(data[2])
        self.sceneids.append(data[3])
        self.sceneids.append(data[4])
        self.sceneids.append(data[5])
        self.sceneids.append(data[6])
        self.sceneids.append(data[7])
        self.sceneids.append(data[8])
        self.sceneids.append(data[9])
        self.sceneids.append(data[10])



class Level2SceneManager():
    def __init__(self):
        self.tableData = {}

    def initData(self):
        self.tableData.clear()
        tableName = "table_level2scene"
        fields = "num,scene0,scene1,scene2,scene3,scene4,scene5,scene6,scene7,scene8,scene9"
        data = db_Manager.selectDataFromTable(tableName,fields)
        for infoData in data:
            info = SceneInfo_Const(infoData)
            self.tableData[info.num] = info


    def getScene(self,num,group):
        sceneid = self.tableData[num].sceneids[group]
        print("getScene num %s,group %s---->sceneid %s",(num,group,sceneid))
        return  sceneid

level2sceneManager = Level2SceneManager()
