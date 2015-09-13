import tornado
from managers.const_table_manager import ConstTableManager

__author__ = 'Mike'
class ConfigHandler(tornado.web.RequestHandler):
    def get(self):
        ConstTableManager.loadConstTable()
        print('config table reload!!')
        self.write('config table reload!!')