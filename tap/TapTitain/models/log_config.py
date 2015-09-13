import datetime
import logging
import os
from tornado import options
from managers.player_data_manager import playerDataManager

__author__ = 'Mike'
class LogConfing:
    year = 0
    month = 0
    day = 0
    @staticmethod
    def initConfig():

        if LogConfing.year == datetime.datetime.now().year or LogConfing.month == datetime.datetime.now().month or LogConfing.day == datetime.datetime.now().day:
            return
        LogConfing.year = datetime.datetime.now().year
        LogConfing.month = datetime.datetime.now().month
        LogConfing.day = datetime.datetime.now().day

        log_path = ''
        if os.name!='nt':
            options.logging = "debug"
            log_path = "../logs/server_log@%s@%s-%s-%s.log"%(playerDataManager.server_id,LogConfing.year,LogConfing.month,LogConfing.day)
            options.log_file_prefix = log_path
        else:
            options.logging = "debug"
            log_path =  "E:/log/server_log@%s@%s-%s-%s.log"%(playerDataManager.server_id,datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
            options.log_file_prefix = log_path

        log = logging.getLogger("tornado.access")
        handler = logging.handlers.RotatingFileHandler(log_path,maxBytes = 1000000,backupCount=20)
        log.addHandler(handler)
        log.info('server start')