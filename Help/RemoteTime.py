#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'remoteTime'
__author__ = 'ngc7293'
__mtime__ = '2020/4/28'
"""

import time


def RemoteTime(s):
    try:
        time_s = time.strptime(s, "%Y-%m-%d")
        return int(time.mktime(time_s))

    except:
        return None


def checkTime(s: str) -> bool:
    now_time = int(time.time())
    if RemoteTime(s) is not None and RemoteTime(s) < now_time:
        return False
    else:
        return True


def NowTime():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


def FuTime():
    return time.strftime("%Y-%m-%d", time.localtime(time.time() + 10000000))


if __name__ == '__main__':
    print(FuTime())
