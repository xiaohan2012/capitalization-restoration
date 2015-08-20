#! /bin/bash

for path in data/request_example_data/*.json; do
	echo $path
	data=$(cat $path)
	python capitalization_restoration_web.py --json_string "${data}"
	echo -e "\n"
done

# # data=$(cat data/request_example_data/example_data.json)
# # # data=$(cat data/request_example_data/6788E2B8AE48C327A33DA66CCE962ADE.json)
# # # data=$(cat data/request_example_data/199C8BB69F17FEA871D45CC08B43CE91.json)
# # data=$(cat data/request_example_data/8AC66B1DCD4E138D49B36BE6DB6019E3.json)
# # # data=$(cat data/request_example_data/85D853A8165AE3E8C312BBCF3B8B8EFC.json)
# # # data=$(cat data/request_example_data/4ABBA038CB08B29A0EE204DFEE9C7660.json)
# # # data=$(cat data/request_example_data/89F45109E7576F0AD4FE40095C8AD0D4.json)

# python capitalization_restoration_web.py --json_string "${data}"

# echo -e "\n"
