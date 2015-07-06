#! /bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python capitalization_restoration_web.py -s "Kingdom € Tourism and Hospitality Sector to Draw Huge Investments" --docpath "${DIR}/data/test"
