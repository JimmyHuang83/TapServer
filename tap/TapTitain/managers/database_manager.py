import datetime
import pymysql
from config import serverConfigManager

__author__ = 'Mike'
class DBManager:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.last_conn_time = datetime.datetime.now()


    def checkDBStatus(self):
        if datetime.datetime.now() > self.last_conn_time + datetime.timedelta(minutes=30):
            self.last_conn_time = datetime.datetime.now()
            try:
                self.closeDB()
                self.openDB()
            except BaseException as e:
                print('reopen db error',e)
                self.closeDB()
                return False
        return True

    def openDB(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,  user='taptitan',  passwd='taptitan123321',  db=serverConfigManager.getDBName(),charset="utf8")
        self.cur = self.conn.cursor()
        print("openDB!")

    def closeDB(self):
        if self.cur != None:
            try:
                self.cur.close()
            finally:
                print('cur.close exception!!!')
        if self.conn != None:
            try:
                self.conn.close()
            finally:
                print('conn.close exception!!!')
            self.conn = None
            self.cur = None

    def excuteQuery(self,query):
        self.checkDBStatus()
        try:
            self.cur.execute(query)
        except BaseException as e:
            print('BaseException %s' % e)
            self.openDB()
        self.conn.commit()
        datas = self.cur.fetchall()
        return datas


    def selectDataFromTable(self, tableName, fields, conditions=None):
        query = ''
        if conditions == None:
            query = 'select %s from %s '%(fields,tableName)
        else:
            query = 'select %s from %s where %s'%(fields,tableName,conditions)
        print('query:',query)
        return self.excuteQuery(query)

    def insertIntoTable(self,tableName,fields,values,conditions = None):
        query = 'insert into  %s ('%(tableName)
        for i in range(len(fields)):
            if i < len(fields) - 1:
                query = '%s `%s`,'%(query,fields[i])
            else:
                query = '%s `%s`) '%(query,fields[i])

        query = '%s values( '%query
        for i in range(len(values)):
            if i < len(values) - 1:
                query = '%s \'%s\','%(query,values[i])
            else:
                query = '%s \'%s\') '%(query,values[i])

        if not conditions == None:
            query +=' where ' + conditions
        print('query,',query)
        self.excuteQuery(query)

    def updateDataAtTable(self,tableName,fields,values,conditions = None):
        if values == None or len(values) == 0:
            print('updateDataAtTable---> values == None or len(values) == 0')
            return
        if not len(fields) == len(values):
            print('updateDataAtTaBLE values length not match fields!!!')
        query = 'update %s set '%(tableName)
        for i in range(len(fields)):
            filed = fields[i]
            value = values[i]
            query  = "%s `%s` = '%s'" %(query,filed,value)
            if not i == len(fields) -1:
                query  = '%s %s' %(query,',')
        if not conditions == None:
            query +=" where  %s" %conditions
        print(query)
        self.excuteQuery(query)

    # def replaceIntoTable(self,tableName,fields,values,conditions = None):
    #     query = 'replace %s set '%(tableName)
    #     for i in range(len(fields)):
    #         filed = fields[i]
    #         value = values[i]
    #         query  = "%s %s = '%s'" %(query,filed,value)
    #         if not i == len(fields) -1:
    #             query  = '%s %s' %(query,',')
    #     if not conditions == None:
    #         query +=" where  %s" %conditions
    #     print(query)
    #
    #
    #     print('query,'+query)
    #     self.excuteQuery(query)

db_Manager = DBManager()