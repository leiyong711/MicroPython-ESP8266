# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: MicroPython-ESP8266
# author: "Lei Yong" 
# creation time: 2017/10/18 10:29
# Email: leiyong711@163.com

"""
              ┏┓   ┏┓
             ┏┛┻━━━┛┻┓
             ┃       ┃
             ┃ ┳┛  ┗┳  ┃
             ┃    ┻    ┃
             ┗━┓      ┏━┛
              ┃       ┗━━━┓
              ┃  神兽保佑  ┣┓
              ┃　永无BUG！ ┏┛
              ┗┓┓┏━┳┓┏┛
               ┃┫┫ ┃┫┫
               ┗┻┛ ┗┻┛
"""
from simple import MQTTClient
from machine import Pin, I2C, Timer, RTC
# import machine

import ssd1306
import time
# import micropython
# import esp
import dht
import ujson as json
import urequests as requests

i2c = I2C(scl=Pin(14), sda=Pin(2), freq=100000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)


def home(t=11):
    display.fill(0)
    display.text('--home--', 20, 1)
    display.text('view', 14, 11)
    display.text('relay', 14, 21)
    display.text('setting', 14, 31)
    display.text('|', 1, t)
    display.show()
    return t


def view(t=0):
    a = [11, 21, 31, 41, 51]
    if t > 4:
        t = 0
    elif t < 0:
        t = 4
    display.fill(0)
    display.text('--view--', 20, 1)
    display.text('key1:%s' % Pin(0, Pin.IN).value(), 14, 11)
    display.text('key1:%s' % Pin(12, Pin.IN).value(), 14, 21)
    display.text('key1:%s' % Pin(4, Pin.IN).value(), 14, 31)
    display.text('key1:%s' % Pin(5, Pin.IN).value(), 14, 41)
    display.text('key1:%s' % Pin(5, Pin.IN).value(), 14, 51)
    display.text('|', 1, a[t])
    display.show()
    return t


class mqtt:
    def __init__(self, client_id='', username='', password=''):
        self.server = "183.230.40.39"
        self.client_id = "产品id"
        self.username = '用户id'
        self.password = 'apikey'
        self.topic = b"TurnipRobot" # 随意名字
        self.mqttClient = MQTTClient(self.client_id, self.server, 6002, self.username, self.password)
        self.dht11 = dht.DHT11(Pin(14))
        self.pid = 0  # publish count
        self.num = 0

    def isPin(self, pin='-1'):
        if int(pin) in (0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16):
            return int(pin)
        else:
            return -1

    def pubData(self, kc):
        # self.dht11.measure()
        value = {'datastreams': [{"id": "hello", "datapoints": [{"value": kc}]}]}  # 你自己的数据流
        jdata = json.dumps(value)
        jlen = len(jdata)
        bdata = bytearray(jlen + 3)
        bdata[0] = 1  # publish data in type of json
        bdata[1] = int(jlen / 256)  # data lenght
        bdata[2] = jlen % 256  # data lenght
        bdata[3:jlen + 4] = jdata.encode('ascii')  # json data
        # print(bdata)
        # print('publish data', str(self.pid + 1))
        self.mqttClient.publish('$dp', bdata)
        self.pid += 1

    def putt(self, t):
        # num = rtc.datetime()[6]
        # if num == 100: num = 0
        self.pubData(66)

    def sub_callback(self, topic, msg):
        print((topic, msg))
        cmd = (eval(bytes.decode(msg)))
        print(type(cmd))
        print(cmd)
        # cmd = msg.decode('ascii').split(" ")

        print(cmd[0])
        # try:
        print(8888888)
        if cmd[0] == 'pin':
            print(999999)
            if cmd[0] == 'pin' and self.isPin(cmd[1]) >= 0:
                value = Pin(int(cmd[1])).value()
                if cmd[2] == 'on':
                    value = 1
                elif cmd[2] == 'off':
                    value = 0
                elif cmd[2] == 'toggle':
                    value = 0 if value == 1 else 1

                pin = Pin(int(cmd[1]), Pin.OUT)  # , value=(1 if cmd[2] == 'on' else 0))
                pin.value(value)
                print('%s完毕' % cmd[1])
            else:
                print('Pin number outof range.')
        # except:
        elif cmd[0]['key'] == '+':
            print(self.num)
            print(5666)
            self.num += 1
            self.num = view(self.num)
            print(self.num)
        elif cmd[0]['key'] == '-':
            self.num -= 1
            self.num = view(self.num)
            print(self.num)

    def connect(self):
        self.mqttClient.set_callback(self.sub_callback)
        self.mqttClient.connect()
        tim = Timer(1)
        tim.init(period=3000, mode=Timer.PERIODIC, callback=self.putt)
        self.mqttClient.subscribe(self.topic)
        print("连接到 %s, 订阅 %s 主题." % (self.server, self.topic))

        try:
            while 1:
                # self.mqttClient.wait_msg()
                self.mqttClient.check_msg()
        finally:
            # self.mqttClient.unsubscribe(self.topic)
            self.mqttClient.disconnect()
            print('mqtt closed')
            tim.deinit()


view(0)
mq = mqtt(client_id='', username='', password='')  # 依次为产品id，用户id，apikey
mq.connect()

