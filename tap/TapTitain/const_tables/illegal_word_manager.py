from managers.database_manager import db_Manager

__author__ = 'Mike'
class IllegalWordManager:
    def __init__(self):
        self.tableData = []

    def initTable(self):
        self.tableData.clear()
        tableName = "table_illegal_word"
        fields = "illegal_world"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
             self.tableData.append(oneData[0])

    def ContainIllegalWord(self,verifyString):
        if ';' in verifyString:
            return True
        for illegalWorld in self.tableData:
            if illegalWorld in verifyString:
                return  True


        return False

illegalWordManager = IllegalWordManager()