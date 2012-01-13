try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from fixed_width_parser import iterparse_lines
from fixed_width_parser.utils import iterskip, iterchunks

def remove_lines_up_to(text, test):
    while True:
        try:
            line, rest = text.split('\n', 1)
        except ValueError:
            return ''

        if test(line):
            return '\n'.join([line, rest])
        else:
            text = rest

def extract_docket_text(page):
    docket = remove_lines_up_to(page, is_heading)
    docket = docket.rsplit('</PRE>')[0] # Yuck..
    return docket

def is_heading(line):
    return 'B E L L   C O U N T Y' in line

def iterparse_fromstring(text, fields):
    return iterparse(StringIO(text), fields)

def iterparse(fh, fields):
    """Iteratively parse a bell county court docket"""
    # fields = [[Field(*field) for field in row] for row in fields]
    lines = (line.rstrip('\n') for line in fh)

    next(lines) # skip first line "TITLE: DOCKET2C.HTM."
    # skip all heading lines and the following 4 lines.
    data_lines = iterskip(lines, is_heading, 4)
    for result in iterparse_lines(data_lines, fields):
        yield result