from managers.database_manager import db_Manager

__author__ = 'Ryan'

class AccountCDkeyModel:
    def __init__(self):
        self.id = 0
        self.cdkey = ''
        self.is_use = False
        self.usedtime = None
        self.use_udid = ''

    def save(self):
        tableName = "table_account_cdkey"
        fields = []
        fields.append('is_use')
        fields.append('usedtime')
        fields.append('use_udid')
        values = []
        values.append(int(self.is_use))
        values.append(self.usedtime)
        values.append(self.use_udid)
        conditions = "id = %d" %self.id

        try:
            db_Manager.updateDataAtTable(tableName,fields,values,conditions)
            return True
        except:
            return False

    def create(self):
        tableName = "table_account_cdkey"
        query = 'insert into  %s (`cdkey`) values(\'%s\')'  %(tableName, self.cdkey)
        try:
            db_Manager.excuteQuery(query)
            return True
        except:
            return False