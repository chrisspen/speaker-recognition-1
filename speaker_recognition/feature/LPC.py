#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: LPC.py
# Date: Thu Mar 19 19:37:11 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import time

from numpy import *
import numpy as np
from scipy.io import wavfile
import scipy as sp #.linalg.solve_toeplitz

from .MFCC import hamming
from .utils import cached_func, diff_feature

def lpc2(signal, order):
    """Compute the Linear Prediction Coefficients.

    Return the order + 1 LPC coefficients for the signal. c = lpc(x, k) will
    find the k+1 coefficients of a k order linear filter:

      xp[n] = -c[1] * x[n-2] - ... - c[k-1] * x[n-k-1]

    Such as the sum of the squared-error e[i] = xp[i] - x[i] is minimized.

    Parameters
    ----------
    signal: array_like
        input signal
    order : int
        LPC order (the output will have order + 1 items)"""

    order = int(order)

    if signal.ndim > 1:
        raise ValueError("Array of rank > 1 not supported yet")
    if order > signal.size:
        raise ValueError("Input signal must have a lenght >= lpc order")

    if order > 0:
        p = order + 1
        r = np.zeros(p, signal.dtype)
        # Number of non zero values in autocorrelation one needs for p LPC
        # coefficients
        nx = np.min([p, signal.size])
        x = np.correlate(signal, signal, 'full')
        r[:nx] = x[signal.size-1:signal.size+order]
        phi = np.dot(sp.linalg.inv(sp.linalg.toeplitz(r[:-1])), -r[1:])
        return np.concatenate(([1.], phi)), None, None
    return np.ones(1, dtype=signal.dtype), None, None


class LPCExtractor:

    def __init__(self, fs, win_length_ms, win_shift_ms, n_lpc, pre_emphasis_coef):
        self.PRE_EMPH = pre_emphasis_coef
        self.n_lpc = n_lpc
        #self.n_lpcc = n_lpcc + 1

        self.FRAME_LEN = int(float(win_length_ms) / 1000 * fs)
        self.FRAME_SHIFT = int(float(win_shift_ms) / 1000 * fs)
        self.window = hamming(self.FRAME_LEN)

    def lpc_to_cc(self, lpc):
        lpcc = zeros(self.n_lpcc)
        lpcc[0] = lpc[0]
        for n in range(1, self.n_lpc):
            lpcc[n] = lpc[n]
            for l in range(0, n):
                lpcc[n] += lpc[l] * lpcc[n - l - 1] * (n - l) / (n + 1)
        for n in range(self.n_lpc, self.n_lpcc):
            lpcc[n] = 0
            for l in range(0, self.n_lpc):
                lpcc[n] += lpc[l] * lpcc[n - l - 1] * (n - l) / (n + 1)
        return -lpcc[1:]

    def lpcc(self, signal):
        #TODO
        # from scikits.talkbox.linpred import levinson_lpc
        # lpc = levinson_lpc.lpc(signal, self.n_lpc)[0]
        # return lpc[1:]
        lpc = lpc2(signal, self.n_lpc)[0]
        return lpc[1:]

    def extract(self, signal):
        frames = int((len(signal) - self.FRAME_LEN) / self.FRAME_SHIFT + 1)
        feature = []
        for f in range(frames):
            frame = signal[f * self.FRAME_SHIFT:f * self.FRAME_SHIFT + self.FRAME_LEN] * self.window
            frame[1:] -= frame[:-1] * self.PRE_EMPH
            feature.append(self.lpcc(frame))

        feature = array(feature)
        feature[isnan(feature)] = 0
        return feature


@cached_func
def get_lpc_extractor(fs, win_length_ms=32, win_shift_ms=16, n_lpc=15, pre_emphasis_coef=0.95):
    ret = LPCExtractor(fs, win_length_ms, win_shift_ms, n_lpc, pre_emphasis_coef)
    return ret


def extract(fs, signal=None, diff=False, **kwargs): # pylint: disable=function-redefined
    """accept two argument, or one as a tuple"""
    if signal is None:
        assert isinstance(fs, tuple)
        fs, signal = fs[0], fs[1]
    signal = cast['float'](signal)
    ret = get_lpc_extractor(fs, **kwargs).extract(signal)
    if diff:
        return diff_feature(ret)
    return ret


if __name__ == "__main__":
    extractor = LPCExtractor(8000)
    fs, signal = wavfile.read("../corpus.silence-removed/Style_Reading/f_001_03.wav")
    start = time.time()
    ret = extractor.extract(signal)
    print(len(ret))
    print(len(ret[0]))
    print(time.time() - start)
