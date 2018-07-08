#!/usr/bin/python
# -*- coding: utf-8 -*-
import msgpack
import os
from items import *
env_dist = os.environ


def unpack_profiles():
    with open(env_dist.get('GOBIN') + "/ss-server/datas", "rb") as f:
        buf = f.read()
        unpacker = msgpack.unpackb(buf, raw=False)
        print(unpacker)

def pack_profiles(profiles):

