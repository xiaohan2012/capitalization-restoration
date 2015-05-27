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

Run the following for more

    >>> python capitalization_restoration.py --help


