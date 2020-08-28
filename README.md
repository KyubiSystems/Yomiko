Yomiko
======

<img src="http://www.tigris.org.uk/images/yomiko_readman.jpg">

**Comics/doujinshi reader application. Web-based, will work on desktop and tablet devices with swipe interface.**

Scans one or more directories of ZIP, CBZ, RAR or CBR archives and stores lists of images found. Generates thumbnails of individual pages, creates tags from parsing titles of ZIP files. Users can search by name/date/etc., filter archives by tags, or add tags of their own.

Requirements
------------

* See requirements.txt pip requirements file for a list of Python prerequisites.
* A database, SQLite3 by default.
* Pillow (Python Imaging Library fork) with libjpeg support for thumbnail generation.
* Command line 'unrar' for accessing RAR archives.
   - **Windows:** [scoop install unrar](http://scoop.sh)
   - **OSX:** [brew install unrar](http://brew.sh)

Yomiko runs on the _Flask_ Python web framework.

Planned 
-------

- [ ] Lazy loading on thumbnail pages to speed display
- [ ] 7zip support (requires xz install)
- [ ] Cloud storage on GDrive, Amazon S3?
- [ ] Interface with download site apps -- "More like this" button?

License
-------

Yomiko uses the **GPL Version 3.0 license**.