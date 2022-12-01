#!/bin/bash

cat $CONDENSER_CONFIG | envsubst > config.json
python direct_subset.py
