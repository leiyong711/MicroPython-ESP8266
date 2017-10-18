# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: MicroPython-ESP8266
# author: "Lei Yong" 
# creation time: 2017/10/18 10:23
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
#连接本地网络
def do_connect():
        import network
        sta_if = network.WLAN(network.STA_IF)
        ap_if = network.WLAN(network.AP_IF)
        if ap_if.active():
                ap_if.active(False)
        if not sta_if.isconnected():
                print('连接网络……')
        sta_if.active(True)
        sta_if.connect('你要连接的wifi名称', 'wifi密码') #wifi的SSID和密码
        while not sta_if.isconnected():
                pass
        print('网络配置', sta_if.ifconfig())
do_connect()
