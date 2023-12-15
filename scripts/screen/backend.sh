#!/usr/bin/env bash

source /data/dima/.miniconda3/etc/profile.d/conda.sh
conda activate annot8
python manage.py $1

