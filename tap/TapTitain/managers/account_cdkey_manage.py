from managers.database_manager import db_Manager
from models.account_cdkey import AccountCDkeyModel

__author__ = 'Ryan'

def get_cdkey(cdkey):
    tableName = "table_account_cdkey"
    fields = "`id`, `cdkey`, `is_use`, `usedtime`, `use_udid`"
    data = db_Manager.selectDataFromTable(tableName,fields, "cdkey='%s'" %cdkey)

    if data:
        obj = AccountCDkeyModel()
        obj.id = data[0][0]
        obj.cdkey = data[0][1]
        obj.is_use = bool(data[0][2])
        obj.usedtime = data[0][3]
        obj.use_udid = data[0][4]
        return obj
    else:
        return False




