import datetime
import threading
import time
import requests

__author__ = 'Mike'


class PvpRewardTimer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self);
        self.beforeEventMinutes = 1

    def run(self):
        timeNow = self.getTimeNow()
        minutes = timeNow.minute
        if minutes > 30:
            minutes -= 30
        span = 30 - minutes - self.beforeEventMinutes
        if span < 0:
            span = 0
        time.sleep(span * 60)

        urlList = []
        urlList.append('http://192.168.1.127:16001')
        urlList.append('http://54.169.92.200:16001')
        urlList.append('http://54.169.92.200:16002')

        cmd = '/timer_server/refreshPVPReward/'
        while True:
            timeNow = self.getTimeNow()
            if timeNow.hour >= 7 and timeNow.hour < 23:
                if timeNow.hour == 7 and timeNow.minute < 45:
                    pass
                else:
                    print('send reward now %s'%timeNow)
                    for url in urlList:
                        fullUrl = "%s%s"%(url,cmd)
                        self.sendMessage(fullUrl)

            time.sleep(30 * 60)

    def sendMessage(self,url):
        sendMessage = ''
        try:
            print("sendMessage url ->%s" % url)
            respond = requests.get(url)
            text = respond.content
            print('receive %s' % text)
        except BaseException as be:
            print("BaseException:%s"%be)


    def getTimeNow(self, tzInt=8):
        timeNow_UTC = datetime.datetime.utcnow()
        return timeNow_UTC + datetime.timedelta(hours=tzInt)
