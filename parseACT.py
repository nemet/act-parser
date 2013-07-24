#!/usr/bin/python
"""
Quick script to parse ACT score files in the fix-width field format that they came in.
I wrote this so that my sister, who is a guidance counselor, could use the data that
they paid for.

You have to hard code the location of the source files. By default it will look for
./data/*.txt, relative to the location of this script. You can override the directory
and/or extension that it looks for. This can be overridden by changing DIR and EXT
below. Or you can hard code an explicit list of files by uncommenting the comment line
that starts with #FILES =

The output will be named output.csv and will put in the same directory as the
source files. This can be overridden by changing DIR and OUT_FILE below.

Created by nemet on 6/4/13 9:58 PM
"""
# imports
import csv
import glob
import os
import sys
from lookup_college import COLLEGES
from output_fields import FIELDS
from lookup_essay_comments import ESSAY_COMMENTS

# constants
__author__ = 'nemet'
DIR = 'data'  # The directory containing the ACT files, relative to this script
EXT = '.txt'  # The extension of the ACT files
OUT_FILE = 'output.csv'  # The file to write for output

FILES = glob.glob(DIR + "/*" + EXT)
# Or if you want to explicitly indicate the file name, do a line like this:
#FILES = ['data/2012-09-10.txt', 'data/2012-11.txt', 'data/2012-12.txt']


def make_header():
    """
    Create the header line from FIELDS
    Return as a list fit for a csv.writer
    """
    row = []
    for i in FIELDS:
        row.append(i[0])
    return row

# classes
class ACTLine:
    """
    Parses one row of input from an ACT data file and outputs it into
    a csv row as defined by FIELDS.
    """
    def __init__(self, line):
        self.line = line
        self.row = []
        self.parse_line()
        self.fix_columns()
        return
    def parse_line(self):
        """
        Convert the string in line to the fixed width fields
        indicated by FIELDS
        Strip them of leading spaces, too.
        """
        for f in FIELDS:
            begin = f[1] - 1
            end = f[2]
            self.row.append(self.line[begin:end].strip())
        for i in range(17,21):
            self.row[i] = self.lookup_essay_comment(self.row[i])
        return
    def fix_columns(self):
        """
        Do lookups or formatting changes for specific rows
        """
        i = 0
        for f in FIELDS:
            # Lookup the essay comments
            if 'Comment On Essay' in f[0]:
                self.row[i] = self.lookup_essay_comment(self.row[i])
            # Lookup the college codes
            if 'College Choices' in f[0]:
                self.row[i] = self.lookup_college(self.row[i])
            i += 1
        return
    def lookup_essay_comment(self, key):
        try:
            return ESSAY_COMMENTS[key]
        except KeyError:
            return key
    def lookup_college(self, code, colleges=COLLEGES):
        try:
            return colleges[code]
        except KeyError:
            return code

def main():
    # Open the out file for writing as a csv writer.
    outfile = open(os.path.join(DIR, OUT_FILE), "wb")
    writer = csv.writer(outfile)

    # Write the header to the CSV file
    writer.writerow(make_header())

    # Open each file, read each line, parse it, and write
    # the result to the output file.
    for textfile in FILES:
        f = open(textfile, "rb")
        for line in f:
            act_line = ACTLine(line)
            writer.writerow(act_line.row)
        f.close()

if __name__ == '__main__':
    status = main()
    sys.exit(status)