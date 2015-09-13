import datetime
import logging
import os
from tornado import options
from config import Configration

__author__ = 'Mike'
log_path = ''
if os.name!='nt':
    options.logging = "debug"
    log_path = "../logs/test_log@%s@%s-%s-%s.log"%(Configration.serverid,datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
    options.log_file_prefix = log_path
else:
    options.logging = "debug"
    log_path =  "E:/log/test_log.txt"
    options.log_file_prefix = log_path

log = logging.getLogger("taptitan")
log.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(log_path,maxBytes = 1000000,backupCount=20)
log.addHandler(handler)
log.info('server start....')
logging.debug('server start!111!!')