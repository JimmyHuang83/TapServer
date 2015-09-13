__author__ = 'Mike'
class AnouncementType:
    firstPay = 1001 #'shou chong li bao')
    monthVIP = 1002 #'gui bin yue ka')
    loginGift = 1003    #'deng lu li bao')
    unlockGemsPartner = 1004    #'mai zuanshi xiao huo ban')

    got3eqpset = 2001   #'ji qi 3 jian tao yi shang')
    eqpQltyUpgrade = 2002   #'zhuangbei pinzhi shengji')

    topPvpLeader = 3001#'wanjia huode PVP leader Top 1')








class Announcement:
    def __init__(self,data):

        self.playerid = ''
        self.type = ''
        self.parameter1 = ''
        self.parameter2 = ''
        self.parameter3 = ''

        self.parameters = []
        self.parameters.append(self.playerid)
        self.parameters.append(self.type)
        self.parameters.append(self.parameter1)
        self.parameters.append(self.parameter2)
        self.parameters.append(self.parameter3)

        self.announcement_id = 0

        for index in range(len(data)) :
            if index < len(self.parameters):
                self.parameters[index] = data[index]
            else:
                print(' index beyond parameters length, in Announcement model')




class ReportAnnouncement:
    def __init__(self):
        pass







reportAnnouncement = ()














