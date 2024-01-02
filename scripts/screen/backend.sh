#!/usr/bin/env bash

source ${CONDA_PREFIX:-/data/dima/.miniconda3}/etc/profile.d/conda.sh
conda activate annot8
python manage.py $@

