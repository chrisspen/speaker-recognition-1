#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: __init__.py
# Date: Sat Nov 29 21:42:15 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import sys

import numpy as np

try:
    from . import BOB as MFCC
except Exception as e:
    print(e, file=sys.stderr)
    print("Warning: failed to import Bob, will use a slower version of MFCC instead.", file=sys.stderr)
    from . import MFCC
from . import LPC


def get_extractor(extract_func, **kwargs):

    def f(tup):
        return extract_func(*tup, **kwargs)

    return f


def mix_feature(tup):
    mfcc = MFCC.extract(tup)
    lpc = LPC.extract(tup)
    if not np.any(mfcc):
        print("ERROR.. failed to extract mfcc feature:", len(tup[1]), file=sys.stderr)
    return np.concatenate((mfcc, lpc), axis=1)
