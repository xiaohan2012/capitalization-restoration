# Introduction

Restore the capitalize of news titles. For example, the original one(incorrectly capitalized) is *DreamWorks Animation zone to open in motiongate Dubai*.

The correctly capitalized one is *DreamWorks Animation zone to open in motiongate Dubai*.

We want to restore to the above.

# Usage

## Python call

	>>> from cap_restore import DefaultRestorer
	>>> restorer=DefaultRestorer()
	>>> s = u"Kingdom's Tourism and Hospitality Sector to Draw Huge Investments".split()
	>>> docpath = "/group/home/puls/Shared/capitalization-recovery/10/www.zawya.com.rssfeeds.tourism/E85D3090167053EFB118C243D9747FAC"
	>>> print " ".join(restorer.restore(s, docpath=docpath))
	Kingdom's Tourism and hospitality sector to draw huge investments

## Command line

First, open the web service:

    >>> python capitalization_restoration_service.py

Second, 

    >>> python capitalization_restoration_web.py --help


## Demo

For Curl:

    >>> ./curl_cmd_demo.sh

For Shell:

    >>> ./py_cmd_demo.sh


## How to add new features

1. Modify the `feature_extractor.py` and `feature_template.py`
2. Retrain the data
3. Update the model in `models/`

## Links

- [Monit(service supervision tool)](https://mmonit.com/monit/)


## Running Monit

Before running `monit`, paths setting should be fixed.

Two things should be done:

1. Ensure the `pid` directory in `cap_restore.sh` is writable
2. Ensure the "check process" part in `monitrc` has the correct path information


Then, run the following to start monitoring

    >>> monit -c /path/to/monitrc # one sample is shiped under this directory

