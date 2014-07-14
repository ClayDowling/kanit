#!/usr/bin/python
#
# Iterate over a planning directory and produce necessary reports

import re
import sys
import os

def get_title(buff):
    """
    Retrieve the title from a text buffer.  The title is the first line
    following a ReStructured Text title indicator (======).

    @param[in] buff     Text buffer containing the task file

    @return string      Text of the title
    """

    match = re.search('===*\n(.*)\n', buff, re.MULTILINE)
    if match == None:
        return 'No title'

    return match.group(1)

def get_status(buff):
    """
    Retrieve the task status from a text buffer.  This is set with the RST
    field :status:  If no value is found, "Not Started" is returned as a
    default

    @param[in] buff     Text buffer containing the task file
    """

    match = re.search(':status:\s*(.+)', buff, re.MULTILINE)
    if match == None:
        return 'Unknown'

    return match.group(1)

def get_points(buff):
    """
    Retrieve the number of points assigned to this task.  This is set with 
    the RST field :points:  If no value is found, 0 is returned as a default.

    @param[in] buff     Text buffer containing the task file

    @return int     Integer value for points
    """

    match = re.search(':points:\s*(\d+)', buff, re.MULTILINE)
    if match == None:
        return 0

    value = 0
    try:
        value = int(match.group(1))
    except:
        value = 0

    return value

def main():

    files = sys.argv[1:]
    title = {}
    status = {}
    points = {}
    slist = {}
    totalpoints = 0
    statuspoints = {}

    for f in files:
        fp = open(f, 'r')
        buff = fp.read()
        title[f] = get_title(buff)
        s = get_status(buff)
        if not s in slist:
            slist[s] = [f]
        else:
            slist[s].append(f)

        status[f] = s
        
        taskpoints = get_points(buff)
        points[f] = taskpoints
        totalpoints = totalpoints + taskpoints

        if not s in statuspoints:
            statuspoints[s] = taskpoints
        else:
            statuspoints[s] = statuspoints[s] + taskpoints

    print """
    <html>
    <head>
      <link rel="stylesheet" type="text/css" href="kanit.css" />
      <title>Kanban Board</title>
    </head>
    <body>

    <h1 class="boardname">Kanban Board</h1>

    <p class="boardpoints">%d points</p>
    """ % totalpoints

    slen = len(slist)
    swidth = 90 / slen
    for s in slist.keys():
        print '<div class="statuscolumn" style="width: %d%%; float: left;">' % swidth
        print '<p class="status"><span class="statusname">%s</span> <span class="statuspoints">[%d]</span></p>' % (s, statuspoints[s])
        print '<ul class="statusitem">'
        for f in slist[s]:
            (root, ext) = os.path.splitext(f)
            htmlfile = root + '.html'
            os.system("rst2html %s > %s" % (f, htmlfile))
            print '<li><a href="%s">%s</a> [%d]</li>' % (htmlfile, title[f], points[f])
        print "</ul>"
        print "</div>"

    print """
    </body>
    </html>
    """

if __name__ == "__main__":
    main()
