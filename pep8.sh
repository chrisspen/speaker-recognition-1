#!/bin/bash
pylint --version
pylint --rcfile=pylint.rc --ignore=gmmset.py speaker_recognition setup.py
