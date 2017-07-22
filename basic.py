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

    req = urllib.request.Request(postUrl)
    res = urllib.request.urlopen(req)
    urlResp = json.loads(res.read())

    accessToken = urlResp['access_token']
    leftTime = urlResp['expires_in']

    update_access_token(accessToken, leftTime)


def update_access_token(token, leftTime):
    mysql = MySQL()
    mysql.exec_none_query('update access_token set token="{0}", expire_time={1} where id=1'.format(token, leftTime))


def update_leftTime(leftTime):
    mysql = MySQL()
    mysql.exec_none_query('update access_token set expire_time={0} where id=1'.format(leftTime))


def get_leftTime():
    mysql = MySQL()
    leftTime = int(mysql.exec_query('select expire_time from access_token where id=1')[0][0])
    return leftTime


def run():
    leftTime = get_leftTime()
    if leftTime > 1800:
        leftTime -= 30
        update_leftTime(leftTime)
    else:
        real_get_access_token()


if __name__ == '__main__':
    run()
    print('')
