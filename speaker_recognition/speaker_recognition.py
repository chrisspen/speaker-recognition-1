#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: speaker-recognition.py
# Date: Sun Feb 22 22:36:46 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>
from __future__ import print_function

import argparse
import sys
import glob
import os
import itertools

# import scipy.io.wavfile as wavfile

# sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gui'))
from .gui.interface import ModelInterface
from .gui.utils import read_wav
# from .gui.filters.silence import remove_silence

UBM_LABEL = '_ubm'


def get_args():
    desc = "Speaker Recognition Command Line Tool"
    epilog = """
Wav files in each input directory will be labeled as the basename of the directory.
Note that wildcard inputs should be *quoted*, and they will be sent to glob.glob module.

Examples:
    Train (enroll a list of person named person*, and mary, with wav files under corresponding directories):
    ./speaker-recognition.py -t enroll -i "./bob/ ./mary/ ./person*" -m model.out

    Predict (predict the speaker of all wav files):
    ./speaker-recognition.py -t predict -i "./*.wav" -m model.out
"""
    parser = argparse.ArgumentParser(description=desc, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-t', '--task', help='Task to do. Either "enroll" or "predict"', required=True)

    parser.add_argument('-i', '--input', help='Input Files(to predict) or Directories(to enroll)', required=True)

    parser.add_argument('-m', '--model', help='Model file to save(in enroll) or use(in predict)', required=True)

    ret = parser.parse_args()
    return ret


def task_enroll(input_dirs, output_model):
    m = ModelInterface()
    if isinstance(input_dirs, str):
        input_dirs = input_dirs.strip().split()
    input_dirs = [os.path.expanduser(k) for k in input_dirs]
    dirs = itertools.chain(*(glob.glob(d) for d in input_dirs))
    dirs = [d for d in dirs if os.path.isdir(d)]
    files = []
    if not dirs:
        print("No valid directory found!")
        sys.exit(1)
    training_stats = []
    total_dirs = len(dirs)
    for i, d in enumerate(dirs):
        print('Processing directory %i of %i...' % (i+1, total_dirs))
        label = os.path.basename(d.rstrip('/'))

        wavs = glob.glob(d + '/*.wav')
        if not wavs:
            print("No wav file found in {0}".format(d))
            continue
        print("Label '{0}' has files: {1}".format(label, ', '.join(wavs)))
        total_len = 0
        total_wavs = len(wavs)
        for j, wav in enumerate(wavs):
            fs, signal = read_wav(wav)
            print("   Processing directory {} of {}, file {} of {}: '{}' has frequency={} and length={}"\
                .format(i+1, total_dirs, j+1, total_wavs, wav, fs, len(signal)))
            total_len += len(signal)
            m.enroll(label, fs, signal)
            m.enroll(UBM_LABEL, fs, signal)
        training_stats.append((label, total_len))
    print("--------------------------------------------")
    for label, total_len in training_stats:
        print("Total length of training data for '{}' is {}".format(label, total_len))
    print("For best accuracy, please make sure all labels have similar amount of training data!")

    m.train()
    m.dump(output_model)


def task_predict(input_files, input_model):
    m = ModelInterface.load(input_model)
    if isinstance(input_files, str):
        input_files = input_files.strip().split()
    input_files = [os.path.expanduser(k) for k in input_files]
    results = []
    total_files = len(input_files)
    for i, f in enumerate(input_files):
        print('Predicting file %s: %i of %i...' % (f, i+1, total_files))
        fs, signal = read_wav(f)
        # scores = m.predict_scores(fs, signal)
        best = m.predict(fs, signal)
        print('Prediction:', best)
        results.append(best)
        # y_scores = dict(zip(m.gmmset.y, scores))
        # print(f, '->')
        # for label, score in sorted(y_scores.items(), key=lambda o: o[1], reverse=True):
            # print(score, label)
            # results.append((f, label, score))
    return results


if __name__ == '__main__':
    global args
    args = get_args()

    task = args.task
    if task == 'enroll':
        task_enroll(args.input, args.model)
    elif task == 'predict':
        task_predict(args.input, args.model)
