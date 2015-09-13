import datetime

__author__ = 'Mike'
class GameTools:
    default_mat = '%Y-%m-%d %H:%M:%S'
    TIME_ZONE = 8
    @staticmethod
    def datetime2string(datetime,mat = default_mat):
        return datetime.strftime(mat)


    @staticmethod
    def string2datetime(strtime, mat = default_mat):
        return datetime.datetime.strptime(strtime,mat)



    @staticmethod
    def getDatetimeNow(tz = 8):
        timeNow_UTC = datetime.datetime.utcnow()
        return timeNow_UTC + datetime.timedelta(hours = tz)

    @staticmethod
    def getDateTimeNowString():
        timeNow = GameTools.getDatetimeNow()
        timeNowStr = GameTools.datetime2string(timeNow)
        return timeNowStr