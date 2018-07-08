#!/usr/bin/python
# -*- coding: utf-8 -*-
import msgpack
# import fcntl
import os
env_dist = os.environ

def unpack_profiles():
    with open(env_dist.get('GOBIN') + "/ss-server/datas", "rb") as f:
        buf = f.read()
        unpacker = msgpack.unpackb(buf, raw=False)
        print(unpacker)

def pack_profiles(package):
    with open(env_dist.get('GOBIN') + "/ss-server/datas", "wb") as f:
        # fcntl.flock(f, fcntl.LOCK_EX)
        buf = msgpack.packb(package.Profiles, use_bin_type=True)
        f.write(buf)
        # fcntl.flock(f, fcntl.LOCK_UN)