__author__ = 'Mike'
class Partner:
    def __init__(self,data):
        self.partner_id = data[0]
        self.partner_level = data[1]
        self.hadBeenUnlocked = data[2]
        self.hp = data[3]
        self.sleep = data[4]
        self.order = data[5]


