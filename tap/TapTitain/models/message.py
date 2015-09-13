#coding=utf-8
import base64
import logging
from models.JsonX import MyEncoder, MyDecoder
from models.game_tools import GameTools
from models.message_encrypt import DES
import urllib.parse
__author__ = 'Mike'
class MessData():
    def __init__(self,errorCode = None):
        self.data = ''
        self.error = ''
        self.result = 0
        if errorCode != None:
            self.result = errorCode[0]
            self.error = errorCode[1]


class ErrorCode:
    #login server
    maintain = (1,"server maintain")

    #gameplay server
    #100+

    #login
    have_not_sign = (101,'have_not_sign')
    name_used = (102,'name_used')
    tokenOutData = (103,'tokenOutDate')
    dataError = (104,'dataError')
    underAttackNow = (105,'under attack now')
    name_illegal = (106,'name illegal')
    have_not_activate_cdkey = (107, 'have_not_activate_cdkey')              # 账号激活CDKEY不能为空
    activate_cdkey_error = (108, 'activate_cdkey_error')                    # 无效CDKEY
    connect_id_error = (109, 'connect_id_error')                             # 无效连接ID


    #equipment 200 +
    equipmentid_exist = (201,"equipment id exist")
    posHasEquipment = (202,"Has Equipment at the pos")
    takeoffFromPosIs10 = (203,"can take off equipment from pos 10")
    takeoff_pos10NotEmpyty = (204,"pos not empty")
    takeoff_frompos_empty = (205,"takeoff from pos empty")
    # equipment_pos10empty = (206,"equipment pos10 is empty")
    equipment_pos10empty = (206,"equipment id is null")
    equipment_pos10idnotmatch = (207,"equipment pos10 id not match")
    sale_equipment_error = (208,"pos 10 empty or id not match")
    verifyEquipment = (209,"this level do not loot the equipment")
    verifyEquipmentLevel = (210,"verifyEquipmentLevel %5 != 4,or reveial num not match")
    verifyEquipmentLevellow = (211,"this level already loot equipment")
    levelNotMatch = (212,'level not match')
    notLuckNumNow = (213,'luck_num != 0')
    equipmentUpgradeError = (214,'equipment Upgrade Error')
    verifyEquipmentBuffError = (215,"equipment buff value not match")
    verifyEquipmentBufftypeError = (216,"equipment buff type not match")
    # other
    logicError = (10000,'logic error')

    #pvp
    #300+
    resourceNotEnough = (300,'resource not enough')
    rankHadChanged = (301,'rankHadChanged')
    targetIsOnlineNow = (302,'target is online')
    underAttacByOthers = (303,'underAttackNow')
    pvpNOTUnlockNow = (304,'pvp not unlock now')
    cannotAttackYourself = (305,'cannot Attack Yourself')
    fightTargetNotMatch = (306,'fight Target Not Match')
    pvpVerifyError = (307,'pvp Verify Error')
    #pve
    # 400+
    coinOutOfRange = (401,"coin out range")
    monsterNotDie = (402,"monsterNotDie")
    levelandwaveLogicError = (403,"level and wave LogicError")

    #upgrade
    #500+
    notunlocknow = (501,'not unlock now')
    skillUpgradeError = (502,'skill Upgrade Error')
    upgradeEqp_notHaveEqp = (503,'not have this id upgrade eqp')
    toQltyTooBig = (504,"to quality too big")
    toQltyBuffVerifyERROR = (505,"BUFF error")
    eqpSaleValueBig = (506,"sale reveial too big")
    costNotMatch = (507,"cost Not Match")
    #use skill 600+
    skillincd = (601,' cd now')

    #shop 700+
    shopVerifyError = (701,'shop Verify Error')
    shopIDError = (702,'shopIDError')


    #opevent 800+
    opeventCumulativeRechargeTypeError = (801,'Opevent Cumulative Recharge Type Error')             # 累计充值类型错误
    opeventCumulativeRechargeStatusError = (802,'Opevent Cumulative Recharge Status Error')         # 累计充值状态错误(已被兑换)
    opeventCumulativeRechargeRewordsError = (803,'Opevent Cumulative Recharge Rewords Error')       # 累计充值奖励不存在
    opeventCumulativeRechargeCompletedError = (804,'Opevent Cumulative Recharge Completed Error')   # 累计充值未达到完成条件
    opeventLoginRewordsError = (805,'Opevent Login Rewords Error')                                    # 累计登录奖励不存在
    opeventLoginRewordsStatusError = (806,'Opevent Login Rewords Status Error')                      # 累积登录领取错误(已领取或跳跃领取)
    opeventLoginRewordsCompletedError = (807,'Opevent Login Rewords Completed Error')                # 累计登录未达到完成条件
    opeventLoginRewordsTypeError = (808,'Opevent Login Rewords Type Error')                          # 累计登录类型错误

    # gift 820+


    # tutorial
    tutorialStepError = (901,'Tutorial Step Error')                                                   # 新手引导步骤不存在

class MessageTools:
    log = logging.getLogger("tornado.access")
    iv = '1234567812345678'
    key = '12345678'


    @staticmethod
    def decode(data):#data byte[]
        des = DES('12345678','1234567812345678')
        encryptdata = None
        if type(data) != type(''):
            data = data.decode('utf-8')

        print("data:"+data)
        # data = data.encode('utf-8')
        try:
            encryptdata = des.decrypt(data)
        except:
            print('exception !!!!!!!!!!!!!!')
        sde_data = encryptdata.decode('utf-8')#to string
        #log here sde_data
        print(sde_data)
        # logging.info("receive data"+ sde_data)
        try:
            MessageTools.log.info("receive data"+ sde_data)
        except BaseException as e :
            pass
        receiveDic = MyDecoder().decode(sde_data)
        return receiveDic

    @staticmethod
    def encode(object,isencrypt = True):
        jsonStr = MyEncoder().encode(object)
        #log here jsonStr
        print(jsonStr)
        # logging.info("respond data"+ jsonStr)
        try:
            MessageTools.log.info("respond data"+ jsonStr)
        except BaseException as e :
            pass
        if isencrypt:
            timeBefore = GameTools.getDatetimeNow()
            bjson = jsonStr.encode(encoding= "utf8")
            des = DES('12345678','1234567812345678')
            encryptdata = des.encrypt(bjson)

            sss = encryptdata.decode('utf-8')
            timeAfter = GameTools.getDatetimeNow()
            alpha = timeAfter - timeBefore
            print('total seconds :%s' %alpha.total_seconds())
            sss = "1111%s"%jsonStr
        else:
            sss = "0000%s"%jsonStr
        return sss

