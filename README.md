Yomiko
======

**Comics/doujinshi reader application. Web-based, will work on desktop and tablet devices with swipe interface.**

Scans one or more directories of ZIP, CBR or RAR archives and stores lists of images found. Generates thumbnails of cover/first pages, creates tags from parsing titles of ZIP files. Users can search by name/date/etc., filter archives by tags, or add tags of their own.

Requirements
------------

* See Yomiko-reqs.txt pip requirements file for a list of Python prerequisites.
* A database, SQLite3 by default.
* Pillow (Python Imaging Library fork) with libjpeg support for thumbnail generation.

Yomiko runs on the _Flask_ Python web framework.

Options
-------

* "More Like this" to grab similar titles from download sites?
* Cloud storage on Amazon S3?