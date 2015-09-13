#coding:utf-8
__author__ = 'Mike'
import binascii
import base64
import pyDes

class DES:
    iv = '12a456c8'
    key = 'ksjdflk2jsdklsj1df'
    def __init__(self, iv, key):
        self.iv = iv
        self.key = key
    def encrypt(self, data):
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        d = k.encrypt(data)
        d = base64.b64encode(d)
        return d
    def decrypt(self, data):
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)

        data = base64.b64decode(data)
        d = k.decrypt(data)
        return d