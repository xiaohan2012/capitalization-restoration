#! /bin/bash

for path in data/request_example_data/*.json; do
	echo $path
	data=$(cat $path)
	python capitalization_restoration_web.py --json_string "${data}"
	echo -e "\n"
done
