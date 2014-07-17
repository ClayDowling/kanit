#!/usr/bin/python
#
# Iterate over a planning directory and produce necessary reports

import re
import sys
import os
import task

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

def pedestrian(arg, dirname, fnames):
    """
    Walk me Amadeus.  Callback function for os.path.walk which will
    correctly generate the kanban board statistics and appropriate
    output files

    @param[in] arg  Blind argument
    @param[in] dirname  Directory currently occupied
    @param[in] fnames   List of files in this path.  del any members
                        which are directories and should not be
                        descended.
    """

    tasks = []
    status = {}
    points = {}
    boardpoints = 0

    # Knock out housekeeping folders
    if 'backlog' in fnames:
        idx = fnames.index('backlog')
        del fnames[idx]
    if 'archive' in fnames:
        idx = fnames.index('archive')
        del fnames[idx]

    # Add tasks to the list
    for fname in fnames:
        (base, ext) = os.path.splitext(fname)
        if ext == '.txt':
            t = task.Task()
            t.fromFile(os.path.join(dirname, fname))
            tasks.append(t)

    for t in tasks:
        boardpoints = boardpoints + t.points
        if t.status in status:
            status[t.status].append(t)
            points[t.status] = points[t.status] + t.points
        else:
            status[t.status] = [t]
            points[t.status] = t.points

    title = '%s board' % dirname

    outname = os.path.join(dirname, 'index.html')
    fp = open(outname, 'w')

    fp.write("""
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="kanban.css" />
        <title>%s</title>
    </head>
    <body>
        <h1 class="boardtitle">%s</h1>
        <div class="boardpoints">%d</div>
    """ % (title, title, boardpoints))

    keys = status.keys()
    keys.sort()
    for k in keys:
        fp.write("""
            <div class="statuscolumn">
                <span class="statusname">%s</span>
                <span class="statuspoints">%d</span>
                <ul>
        """ % (k, points[k]))

        v = status[k]
        for t in v:
            fp.write( '     <li><a href="%s">%s</a> [%d]' \
                    % (t.textfile, t.title, t.points))
            if len(t.assigned) > 0:
                fp.write( ' - %s' % ','.join(t.assigned))
            fp.write( '</li>')

        fp.write( """
        </ul>
        </div>
        """)

    fp.write( """
    </body>
    </html>
    """)

    fp.close()

def main():

    paths = sys.argv[1:]

    if len(paths) == 0:
        paths = ['.']

    for path in paths:
        os.path.walk(path, pedestrian, None)

if __name__ == "__main__":
    main()
