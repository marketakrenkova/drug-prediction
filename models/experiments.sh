#!/bin/bash

# ./kg_model.py -m rotate -s best_pipeline3 -e 50 -emb 2000 -o adam -lr 0.002 -b 512 -nn 11 -d interactions --not_train
# ./kg_model.py -m rotate -s best_pipeline3 -e 50 -emb 2500 -o adam -lr 0.005 -b 512 -nn 21 -d drugbank --not_train
./kg_model.py -m rotate -s best_pipeline3 -e 50 -emb 1500 -o adam -lr 0.006 -b 512 -nn 15 -d hetionet --not_train
./kg_model.py -m rotate -s best_pipeline3 -e 50 -emb 2500 -o adam -lr 0.005 -b 512 -nn 3 -d biokg --not_train
# ./kg_model.py -m complex -s best_pipeline3 -e 50 -emb 3000 -o adam -lr 0.007 -b 512 -nn 41 -d interactions --not_train
# ./kg_model.py -m complex -s best_pipeline3 -e 50 -emb 2000 -o adam -lr 0.004 -b 512 -nn 47 -d drugbank --not_train


