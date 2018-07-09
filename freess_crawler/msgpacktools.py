#!/usr/bin/env python
# -*- coding: utf-8 -*-
import msgpack
import json
import os
env_dist = os.environ
from ctypes import CDLL


def unpack_profiles():
    with open(env_dist.get('GOBIN') + "/ss-server/datas", "rb") as f:
        buf = f.read()
        unpacker = msgpack.unpackb(buf, raw=False)
        print(unpacker)


def pack_profiles(package):
    jsonStr = json.dumps(dict(package), ensure_ascii=False)
    print(jsonStr)
    lib = CDLL('./msgpacktool.so')
    lib.InsertProfiles(jsonStr)
