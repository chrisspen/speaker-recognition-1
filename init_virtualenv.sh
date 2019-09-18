#!/bin/bash
PYTHONV=3.6
VENV=./.cenv$PYTHONV
[ -d $VENV ] && rm -Rf $VENV
#virtualenv -p python3.6 .env
#. .env/bin/activate
#pip install -U pip
#pip install -U wheel
#pip install -r requirements-test.txt

#!/bin/bash
#TODO:fix once bob/numpy support Python3.7?
#time conda create --name .cenv37 --override-channels \
  #-c https://www.idiap.ch/software/bob/conda -c defaults \
  #python=3.7 bob
#conda activate .cenv37
time conda create --prefix $VENV --override-channels -c https://www.idiap.ch/software/bob/conda -c defaults -y python=3.6 bob
conda activate $VENV
conda config --env --add channels defaults
conda config --env --add channels https://www.idiap.ch/software/bob/conda
#conda install bob.io.image bob.bio.base
conda install -y git pip
#conda install --file=requirements.txt
conda install -y bob.extension bob.blitz bob.core bob.io.base bob.math bob.sp bob.learn.activation bob.learn.linear bob.bio.spear
pip install -U pip
pip install -U wheel
pip install -r requirements.txt -r requirements-test.txt
#pip install -r /home/chris/git/speaker-recognition-1/requirements.txt
