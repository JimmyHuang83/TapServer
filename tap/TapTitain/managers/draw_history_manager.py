__author__ = 'Mike'

class DrawInfo:
    def __init__(self,data):
        self.name = data[0]
        self.itemid = data[1]
        self.value = data[2]

class DrawHistoryManager:
    def __init__(self):
        self.history = []

    def pushIntoHistory(self,name,resourceAndVlue):
        drawInfo  = DrawInfo((name,resourceAndVlue.itemid,resourceAndVlue.value))
        self.history.append(drawInfo)
        if len(self.history) > 3:
            del  self.history[0]

    def getDrawHistory(self):
        return  self.history


drawHistoryManager = DrawHistoryManager()
