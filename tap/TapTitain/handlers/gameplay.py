import datetime
import tornado.web
import json

from managers.database_manager import db_Manager

__author__ = 'Mike'


class GamePlayEnterBGHandler(tornado.web.RequestHandler):
    def get(self):
        i = {}
        args = self.request.arguments
        for a in args:
            i[a] = self.get_argument(a)

        ret = self._process(i)


        self.write(ret)

    def post(self):
        i = {}
        args = self.request.arguments
        for a in args:
            i[a] = self.get_argument(a)
        ret = self._process(i)
        self.write(ret)


    def _process(self, params):
        id = params['id']
        time_now = datetime.datetime.now()

        tableName = 'player_time'
        fileds = []
        fileds.append('udid')
        fileds.append('last_time')

        values = []
        values.append(id)
        values.append(TimeTools.datetime2string(time_now))
        db_Manager.replaceIntoTable(tableName,fileds,values)

        return 'ok'


class GamePlayEnterForWardHandler(tornado.web.RequestHandler):
    def get(self):
        i = {}
        args = self.request.arguments
        for a in args:
            i[a] = self.get_argument(a)

        ret = self._process(i)


        self.write(ret)

    def post(self):
        i = {}
        args = self.request.arguments
        for a in args:
            i[a] = self.get_argument(a)

        ret = self._process(i)

        self.write(ret)


    def _process(self,params):
        id = params['id']
        tableName = 'player_time'
        fileds = "last_time"
        condition = "udid = '%s'" % id
        data = db_Manager.selectDataFromTable(tableName, fileds,condition)

        last_time = ''
        time_now = time_now = datetime.datetime.now()
        time_now = TimeTools.datetime2string(time_now)
        if len(data) != 0:
            last_time = data[0][0]
        else:
            last_time = time_now

        ret = {}
        ret['time_now'] = time_now
        ret['last_time'] = last_time

        retJson = json.dumps(ret)
        return  retJson



class TimeTools:
    @staticmethod
    def datetime2string(datetime):
        mat = '%Y-%m-%d %H:%M:%S'
        return datetime.strftime(mat)