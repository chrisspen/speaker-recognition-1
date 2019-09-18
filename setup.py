from __future__ import print_function, absolute_import
import os

from setuptools import setup, find_packages

import speaker_recognition

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(CURRENT_DIR, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except TypeError:
    with open(os.path.join(CURRENT_DIR, 'README.md')) as f:
        long_description = f.read()


def get_reqs(*fns):
    lst = []
    for fn in fns:
        for package in open(os.path.join(CURRENT_DIR, fn)).readlines():
            package = package.strip()
            if not package:
                continue
            lst.append(package.strip())
    return lst


setup(
    name="speaker-recognition",
    version=speaker_recognition.__version__,
    packages=find_packages(),
    author="Chris Spencer",
    author_email="chrisspen@gmail.com",
    description="Recognizes a speaker name from an audio stream.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="BSD",
    url="https://github.com/chrisspen/speaker-recognition",
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # 'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False,
    install_requires=get_reqs('requirements.txt'),
    # tests_require=get_reqs('requirements-test.txt'),
)
