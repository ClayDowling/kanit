#!/usr/bin/python
#
# Iterate over a planning directory and produce necessary reports

import re
import sys
import os
import task

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

    if dirname == '.':
        title = 'Kanban board'
    else:
        title = '%s board' % dirname

    outname = os.path.join(dirname, 'index.html')
    fp = open(outname, 'w')

    fp.write("""
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="kanit.css" />
        <title>%s</title>
    </head>
    <body>
        <h1 class="boardtitle">%s</h1>
        <div class="boardpoints">Board Points: %d</div>
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
