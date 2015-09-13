from managers.database_manager import db_Manager

__author__ = 'Mike'
class PickUpInfo:
    def __init__(self,data):
        self.fromNum = data[0]
        self.toNum = data[1]
        self.step = data[2]

class PickUpPlayersTable:
    def __init__(self):
        self.tableData = []

    def initData(self):
        self.tableData.clear()
        cmd ="select fromNum,toNum,step from table_pick_player  ORDER BY fromNum DESC"
        data = db_Manager.excuteQuery(cmd)
        for oneData in data:
            item = PickUpInfo(oneData)
            self.tableData.append(item)

    def pickUpNum(self,selfNum):
        topNum = 3
        if selfNum < 11:
            topNum = 10
        count = 7 #
        findNums = []
        for pickUpInfo in self.tableData:
            fromNum = pickUpInfo.fromNum
            toNum = pickUpInfo.toNum
            step = pickUpInfo.step
            if selfNum > fromNum and selfNum <= toNum:
                while count > 0 and selfNum > fromNum:
                    newNum = selfNum - step
                    if newNum > 0:
                        findNums.append(newNum)
                        selfNum = newNum
                        count -= 1
                    else:
                        count = 0
                        break



        for index in range(1,topNum + 1):
            if not index in findNums:
                findNums.append(index)
        return  findNums

pickUpPlayersTable = PickUpPlayersTable()