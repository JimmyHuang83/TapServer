#coding:utf-8
import pyDes, random
from distutils.core import setup

from models.message_encrypt import DES
import urllib.parse
from managers.player_data_manager import playerDataManager
from models.account_cdkey import AccountCDkeyModel

def des_encode():
    data = '{"udid":"a1fdadceef38c9c2040a2199b1d41e67","token":null}'
    des = DES('12345678','1234567812345678')
    encryptdata = des.encrypt(data.encode('utf-8'))
    print(encryptdata)
# test = "d/YtlYXbDKgdDWfXR/OCoqgfsz89G8T0yBC0N6Tztah7fZMBm8rFMjdWVG+b2obI/95auqG1UBmeL6/l45JxIg=="
#
# decryptdata = des.decrypt(test)
# print (decryptdata)
#
# aaaa =  urllib.parse.urlencode('%C4%A7%CA%DE')
# print(aaaa)
import random
# for index in range(10):
#
#     print(index)

def reset_player_login_gifts_status():
    player = playerDataManager.loginUseUidd('3a8ec7756bb03c49c97c9ad1a92a6e8f06922799')
    player.recharge_get_gifts_status['1'] = 0
    player.recharge_get_gifts_status['2'] = 0
    player.recharge_get_gifts_status['3'] = 0
    player.saveData2DB()

def create_account_active_cdkey():
    count = -1
    AccountCDkeyobj = AccountCDkeyModel()
    for i in range(count+1):
        str = ''
        for j in range(12):
            str +=  random.choice('0123456789')
        str += random.choice('abcdefghijkmnpqrstuvwxyz')
        AccountCDkeyobj.cdkey = str
        AccountCDkeyobj.create()

# create_account_active_cdkey()

