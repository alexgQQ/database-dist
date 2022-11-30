#!/bin/bash

# Could use envsubt but would need to install it everywhere
sed -i "s/DB_USER/$DB_USER/" config.json
sed -i "s/DB_PASSWORD/$DB_PASSWORD/" config.json
sed -i "s/DB_HOST/$DB_HOST/" config.json
sed -i "s/DB_DATABASE/$DB_DATABASE/" config.json

python direct_subset.py
