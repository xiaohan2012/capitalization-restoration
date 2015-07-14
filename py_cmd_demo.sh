#! /bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo "Using sentence string..."
python capitalization_restoration_web.py -s "Kingdom € Tourism and Hospitality Sector to Draw Huge Investments" --docpath "${DIR}/data/test"
echo -e "\n"

### USe this one ###
echo "Using tokens..."
python capitalization_restoration_web.py -s "Kingdom|€|Tourism|and|Hospitality|Sector|to|Draw|Huge|Investments" --docpath "${DIR}/data/test"
echo -e "\n"

echo "Using tokens + pos..."
python capitalization_restoration_web.py -s "Kingdom|€|Tourism|and|Hospitality|Sector|to|Draw|Huge|Investments" --pos 'NNP|:|VBP|CC|NNP|NNP|TO|NNP|NNP|NNP'  --docpath "${DIR}/data/test"
echo -e "\n"
