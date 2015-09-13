__author__ = 'Mike'

d = {}
d[1] = 123456
d[0] = 546546456
d[60] = 658494
d[3] = 1321231
# aa = filter(lambda x:x%60, d)
# print(aa)

playerDic = dict( (k,v) for k,v in d.items() if k % 60 == 0)
for a in playerDic.values():
    print(a)

