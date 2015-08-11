#! /bin/bash

data=$(cat data/example_data.json)

python capitalization_restoration_web.py --json_string ${data}

echo -e "\n"
