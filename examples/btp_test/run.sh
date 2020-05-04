#!/bin/sh

# Enable command echo
set -v

# Directory where this script is located
CURR_DIR=`pwd`

# Icarus main folder
ICARUS_DIR=${CURR_DIR}/../..

# Dir where plots will be saved 
PLOTS_DIR=${CURR_DIR}/plot_cache

# Config file
CONFIG_FILE=${CURR_DIR}/config.py

# FIle where results will be saved
RESULTS_FILE=${CURR_DIR}/results.pickle

# Add Icarus code to PYTHONPATH
export PYTHONPATH=${ICARUS_DIR}:$PYTHONPATH

# Run experiments
echo "Run experiments"
icarus run --results ${RESULTS_FILE} ${CONFIG_FILE}

# Plot results
#echo "Plot results"
python3 ${CURR_DIR}/plot_cachepolicy.py --results ${RESULTS_FILE} --output ${PLOTS_DIR} ${CONFIG_FILE} 
