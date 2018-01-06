"""
Yomiko Comics Reader
(c) 2016 Kyubi Systems: www.kyubi.co.uk
"""

import re
import os.path
from pyparsing import nestedExpr

# separate doujin filenames into titles and characteristic tags


def split_tags(data):
    # simple-minded routine to split filename string into tags

    # crop filename extension
    data = os.path.splitext(os.path.basename(data))[0]

    # substitute all brackets with pipes
    data = re.sub(r'[]([){}]', '|', data)

    # split by pipes, dropping empty entries
    tags = re.split(r'|', data)
    tags = filter(None, tags)

    # Strip whitespace from tags
    tags = [t.strip() for t in tags]

    # return list of tags
    return tags


def split_title_tags(data):
    # Parse input archive filename
    # Return title as string, bracketed elements as tag list
    # Will need to test against Unicode input

    # crop filename extension
    data = os.path.splitext(os.path.basename(data))[0]

    # substitute left parens with round bracket
    data = re.sub(r'[{[]', '(', data)

    # substitute underscores
    data = data.replace('_', ' ')

    # substitute right parens with round bracket
    data = re.sub(r'[]}]', ')', data)

    # Suppress bracketed sections to extract title
    # Will need to catch exceptions here
    title = nestedExpr('(', ')').suppress().transformString(data)

    # Remove whitespace
    title = title.strip()

    # Remove title from input string
    data = data.replace(title, '')

    # Split by remaining round brackets
    tags = re.split(r'(|)', data)

    # Strip whitespace from tags
    tags = [t.strip() for t in tags]

    # Drop empty entries
    tags = filter(None, tags)

    # Return title string and tag list
    return title, tags
