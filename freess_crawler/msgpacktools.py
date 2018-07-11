#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import msgpack
import json
import os
env_dist = os.environ
from ctypes import c_char_p, c_longlong, CDLL, Structure


class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]


def aesencrypt(content):
    lib = CDLL('/usr/lib/python3.6/site-packages/freess_crawler/msgpacktool.so')
    lib.AesEncrypt.restype = c_char_p
    lib.AesEncrypt.argtypes = [GoString]
    buf = bytes(content, encoding='utf8')
    msg = GoString(buf, len(buf))
    result = lib.AesEncrypt(msg)
    return str(result, encoding = "utf-8")


def unpack_profiles():
    with open(env_dist.get('GOBIN') + "/ss-server/datas", "rb") as f:
        buf = f.read()
        unpacker = msgpack.unpackb(buf, raw=False)
        print(unpacker)


def pack_profiles(package):
    jsonStr = json.dumps(dict(package), ensure_ascii=False)
    lib = CDLL('/usr/lib/python3.6/site-packages/freess_crawler/msgpacktool.so')
    lib.InsertProfiles.argtypes = [GoString]
    buf = bytes(jsonStr, encoding='utf8')
    msg = GoString(buf, len(buf))
    lib.InsertProfiles(msg)
