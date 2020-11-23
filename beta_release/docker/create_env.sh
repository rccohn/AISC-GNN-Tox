#!/bin/bash


pip install requests
pip install tensorflow==1.14
pip install torch==1.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

pip install --upgrade tensorboard
conda install -y -c conda-forge rdkit
pip install git+https://github.com/deepchem/deepchem


pip install numpy matplotlib
pip install scikit-learn
pip install jupyterlab
pip install dgl
pip install dgllife

bash 
