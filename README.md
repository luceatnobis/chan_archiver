chan_archiver
==============
This is a program which archives 4chan threads in both content as well as HTML. I was dissatisfied with earlier attempts and other people's programs and missed a functionality to archive the actual posts.

This program uses Python as well as Twisted and currently only runs with Python 2.7. For the moment you will need the treq library as well as txsocksx for socks proxy/tor support.

For the moment there will not be a unit test for the download routine. Mostly because the twisted web stuff is abstracted beyond my level of autism. Fuck this shit.
