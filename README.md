=====
Parser for ACT data files
=====

This is a python script that will translate one or more ACT data files from
a fixed-width field format to a more useful CSV format.

The script takes no arguments; everything is hard-coded in parseACT.py near
the beginning of the script.

There are two lookup tables:

  * lookup_essay_comments.py: translates from comment codes to the descriptive test

  * lookup_college.py: translates from college codes to the institution name.

In the directory named Documentation is the documentation that I could find on the
web explaining how the files are formatted.

I hope someone else finds it useful.
