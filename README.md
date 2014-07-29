osu! Beatmaps
================
Website
---------
A website for browsing and downloading beatmaps.

###Requirement###
- ``django`` the framework. (install via pip)
- ``debug_toolbar`` for debugging. (install via pip)
- ``MySQL-python`` if MySQL support is needed. (install via pip)

Crawler
--------
A crawler that fetch beatmaps from osu! official website.

###Requirement###
- ``requests`` for HTTP requests. (install via pip)
- ``pyquery`` for HTML parsing. (install via pip)

Daemon
-------
A deamon that detects new beatmaps and download them.

###Requirement###
- ``crawler`` the crawler menthioned above.
- ``redis`` for queuing.
