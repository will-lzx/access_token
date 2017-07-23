# -*- coding: utf-8 -*-
# filename: basic.py
import urllib.parse
import urllib.request
import time
import json
from sql_help import *


def real_get_access_token():
    appId = "wxe2d133d468969a91"
    appSecret = "4fa59c6b06441dec0238fbf0df841c63"

    postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}".format(appId, appSecret))
    try:
        req = urllib.request.Request(postUrl)
        res = urllib.request.urlopen(req)
        urlResp = json.loads(res.read())

        accessToken = urlResp['access_token']
        leftTime = urlResp['expires_in']

        update_access_token(accessToken, leftTime)
    except Exception as ex:
        print(ex)


def real_get_jsapi_ticket(access_token):
    postUrl = ("https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi".format(access_token))

    try:
        req = urllib.request.Request(postUrl)
        res = urllib.request.urlopen(req)
        urlResp = json.loads(res.read())

        ticket = urlResp['ticket']
        leftTime = urlResp['expires_in']

        update_jsapi_ticket(ticket, leftTime)
    except Exception as ex:
        print(ex)


def update_access_token(token, leftTime):
    mysql = MySQL()
    mysql.exec_none_query('update access_token set token="{0}", expire_time={1} where id=1'.format(token, leftTime))


def update_jsapi_ticket(ticket, leftTime):
    mysql = MySQL()
    mysql.exec_none_query('update access_token set token="{0}", expire_time={1} where id=2'.format(ticket, leftTime))


def update_leftTime(leftTime):
    mysql = MySQL()
    mysql.exec_none_query('update access_token set expire_time={0} where id=1'.format(leftTime))


def update_ticket_leftTime(leftTime):
    mysql = MySQL()
    mysql.exec_none_query('update access_token set expire_time={0} where id=2'.format(leftTime))


def get_leftTime():
    mysql = MySQL()
    leftTime = int(mysql.exec_query('select expire_time from access_token where id=1')[0][0])
    return leftTime


def get_ticket_leftTime():
    mysql = MySQL()
    leftTime = int(mysql.exec_query('select expire_time from access_token where id=2')[0][0])
    return leftTime


def get_accecc_token():
    sql = 'select token from access_token where id=1'
    mysql = MySQL()
    access_token = mysql.exec_query(sql)[0][0]
    return access_token


def run():
    left = 1800
    internal_time = 30
    leftTime = get_leftTime()
    if leftTime > left:
        leftTime -= internal_time
        update_leftTime(leftTime)
    else:
        real_get_access_token()

    access_token = get_accecc_token()
    ticket_lefttime = get_ticket_leftTime()
    if ticket_lefttime > left:
        ticket_lefttime -= internal_time
        update_ticket_leftTime(ticket_lefttime)
    else:
        real_get_jsapi_ticket(access_token)


if __name__ == '__main__':
    run()
    print('')
