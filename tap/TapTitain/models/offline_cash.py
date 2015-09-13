import datetime
from const_tables.const_value import ConstValue
from const_tables.level_table import levelTable

__author__ = 'Mike'
class OfflineCash:
    @staticmethod
    def calculateOfflineCash(level,time):
        levelInfo = levelTable.getItem(level)
        offlineGold = levelInfo.offlinegold
        max_time = 12 * 60 * 60         # 12h
        if time > max_time:
            time = max_time
        seconds = int(time)

        if seconds < 5 * 60:
            return 0

        minitus = int(seconds / 60)
        offlineCash = offlineGold * minitus

        return int(offlineCash)


