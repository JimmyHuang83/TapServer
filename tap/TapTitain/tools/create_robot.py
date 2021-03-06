#coding=utf-8
import random
import static
from managers.database_manager import db_Manager
from managers.player_data_manager import playerDataManager
import main
from models.game_tools import GameTools
from managers.rank_manger import rankManager
namelist = [
    '扎菲拉', '塔克特','柯尔特','希多','修','亚修','阿萨','路克','爱德华','史提尔',
    '修特','理查德','拉萨鲁','特雷兹','贝罗克','马克','彼特','艾力扎','索尔','泰兰斯',
    '埃罗斯','杰伊斯','达尔','莱纳','卡欧','基多','诺亚','埃米尔','琉特','辛格','塔米尔',
    '埃尔文','罗恩','帕尼修','阿隆','雷伊斯','里德尔','雷诺斯','克雷斯','哈酷','艾伦',
    '艾斯特','凯洛','罗尼','尤里安','盖乌斯','巴帝','雷文','凯渊','艾迪','菲路斯',
    '迪恩','弗林','卡南','C·','D·','H·','K·','Z·','阿尔法','纳茨瓦','阿卡曼',
    '桑德拉','富兰克','米恩','耶卡','罗兰德','斯坦因','罗威尔','盖尔','哈里发','兰格雷',
    '齐利亚','哈忒斯','米拉','凡尼尔','哈维','雷','李','林克尔','维特','怀斯曼',
    '格鲁曼','哈谢尔','维兰','奥迪那','布莱特','玛雷古','特瓦克','迪兰达','奎特',
    '凯尔','琉特','艾菲德','奥托尔','布达拉','里恩','皮埃尔','布朗','桑提斯','奥尔森'
    ,'托特普','瓦伦汀','柏德','加兰多','巴鲁玛','艾维尔','费特','奥兰多','修格','希卡',
    '夏玛尔','贝尔茨','卡秋莎','露西亚','露比','蕾拉','蕾娜','爱莎','艾娃','伊莉丝',
    '芙兰达','雪莉','薇薇安','梅莉亚','蕾雅','爱丽泽','露娜','玛丽安','安娜','梅露蒂'
    ,'芙蕾雅','葛蕾丝','艾西亚','拉米亚','瓦裘蕾','莉亚拉','维尼亚','卓雅','朵莉丝',
    '莉莎','莉诺卡','瓦尔妮','妮妙','亚里亚','艾雯','琉娜','法拉','安洁莉','雪拉',
    '西芙','凯珞','夏露露','梅尔特','拉兹蒂','莎亚','塞拉菲','迪莉亚','菲妮尔','卡莲',
    '可可亚','库洛艾','卡铃','克莉丝','芙铃','拉彼斯','帕蒂','超导','铁血','午夜','变量',
    '异形','致命','荆棘','惊雷','末日','君临的','寂寞','闪电','超兵','暴风','空虚',
    '死神','傲雪','大刀','惆怅','风霜','机车','恶魔','漆黑','苍白','正宗','逆天','暗夜',
    '风中','钻石','太阳','绝望','银光','子夜','夜雾','毁灭','天雷','贵族','空白','银河',
    '红莲','无尽','逆光','夕阳','冷眸','光翼','热血','寒冰','暖暖的','神奇','甜甜',
    '摩卡','玉米','枫糖','红茶','拿铁','焦糖','蜂蜜','牛奶','可可','月夜','月光','毛毛',
    '幽蓝','梦幻','甜饼','夏天的','四季的','冬天的','做梦的','椰子','魔法','初音','天使',
    '微笑','梦见','冰山','精灵','电波','音乐','迷糊','纯白','绯色','淡紫','翠绿','迷你',
    '华丽','雪花','星痕','乐园','迷梦','雨季','哀伤','奇迹','月影','水晶','雨夜','吸吮',
    '死神','最强的','善良的','勇猛的','不要命的','愤怒的','拥抱','加农','加特林','火箭炮',
    '左轮','神样','战士','骑士','公爵','斗士','终结者','超人','大师','突击者','特工',
    '利刃','大老板','草上飞','流云','封印','锋翼','灵魂','修罗','夜叉','笛声','斩月',
    '白狼','使者','天空','星辰','欧尼酱','镜像','地平线','假面','棺木','法则','坦克',
    '羊驼','飞鹰','饭团','糖糖','雪糕','咖啡','巧克力','饼干','果冻','花开','荷包蛋',
    '冰沙','奶酪','慕斯','奶茶','棉花糖','布丁','罐头','兔兔','奶糖','菠萝','甜橙','小辣椒',
    '蘑菇','协奏曲','蚂蚁','小狐狸','喵喵','肉团团','茉莉','泡泡','茶会','夜蝶','人偶',
    '交响曲','夜铃','嘟嘟','花朵','甜心','小毛球','眼镜','舞者','旋律','幽灵','蝴蝶','杀猪刀',
    '大葱','微笑','骷髅','精灵'
]

db_Manager.openDB()
main.init_game_data()
count = 1
while count:
    udid = ''
    for i in range(2):
        udid += random.choice('abcdefghkmnpqrstuvwxyz')

    for i in range(6):
        udid += random.choice('0123456789')

    name = ''
    for i in range(2):
        name += random.choice(namelist)

    if random.choice([True, False]):
        if random.choice([True, False]):
            name += '.'
        name += random.choice('ABCDEFGHIJKLMOPQRSTUVWXYZ')

    if not playerDataManager.isSign(udid):
        if playerDataManager.isNameUsed(name):
            continue
        else:
            playerDataManager.createAccount(udid,name)
            player = playerDataManager.loginUseUidd(udid)
            player.server_date_time = GameTools.getDateTimeNowString()

        player.cash = 10000000
        player.skillUpgrade(0,static.pvp_level_limit)
        player.saveData2DB()
        rankManager.addRank(player.player_id)
    else:
        continue

    count -= 1