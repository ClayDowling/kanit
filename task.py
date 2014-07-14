class Task:

    def __init__(self, buff=None):
        self.title = ''
        self.points = 0
        self.status = ''
        self.assigned = []
        self.textfile = ''
        self.htmlfile = ''

        if buff != None:
            self.setBuffer(buff)


    def setBuffer(self, buff):
        """
        Assign a text buffer to this task.  Populate properties based on
        what is contained in the text buffer.

        @param[in] buff     Text buffer
        """"

        self.buff = buff

        self.title = self._get_title()
        self.points = self._get_points()
        self.status = self._get_status()
        self.assigned = self._get_assigned()

    def fromFile(fname):
        """
        Populate a task from the contents of a file.  This will also
        automatically set the text file name and the html file name.
        By default these are the basename and the basename with the 
        extension replaced by '.html'

        If custom file nameing is desired, the textfile and htmlfile
        properties should be set explicitly.

        @param[in] fname    Filename to read from.
        """
        f = open(fname, 'r')
        buff = fp.read()
        self.setBuffer(buff)

        # Automatically set file name information
        self.textfile = os.path.basename(fname)
        (root, ext) = os.path.splitext(self.textfile)
        self.htmlfile = root + '.html'

    def _get_property(name):
        """
        Return a task property stored in a ReStructuredText field.

        @param[in] name     Name of the field to hunt, lacking the 
                            surrounding ':' characters.
        @param[in] buff     The raw text buffer containing the task

        @return string      String value of the field, or blank if not
                            present.
        """

        expr = ':%s:\s*(.*)' % name
        match = re.search(expr, self.buff, re.MULTILINE)
        if match == None:
            return ''

        return match.group(1)

    def _get_title(self):
        """
        Retrieve the tasks' title from the text buffer.

        @param[in] buff     Text buffer containing the text of the task file.

        @return string      Title of the task or 'Unknown' if there is 
                            no title information available.
        """

        title = ''

        match = re.search("==+\s*\n(.*)", self.buffer, re.MULTILINE)
        if match == None:
            lines = self.buffer.split('\n')
            title = lines[0]
        else:
            title = match.group(1)

        if title == '':
            return 'Unknown'

    def _get_status(self):
        """
        Retrieve the title from the internal text buffer.  This will be
        either the ReStructuredText title (assuming ==== for the top level
        header), or if the title is not present the first line of the file.

        @return string      Assigned status for this task.
        """
        _status = self._get_property('status')
        if _status == '':
            _status = 'Unknown'

        return _status

    def _get_assigned(self):
        """
        Retrieve the list of people assigned to this task, as indicated by
        the :assigned: field.  If more than one person is assigned to this
        task the names should be separated by commas.

        @return list    List of assigned people, or an empty list if there
                        is nobody assigned to this task.
        """
        rawassigned = self._get_property('assigned')
        assigned = []
        if len(rawassigned) > 0:
            if ',' is in rawassigned:
                assigned = [name.strip() for name in rawassigned.split(',')]
            else:
                assigned = [rawassigned]

        return assigned

    def _get_points(self):
        """
        Retrieve the assigned points for this task, as indicated by the
        :points: field.  If the value is non-numeric or missing, the assigned
        value will be 0.

        @return integer     Integer value of the points.
        """
        spoints = self._get_property('points')
        points = 0
        if spoints != '':
            try:
                points = int(spoints)
            except:
                points = 0

        return points
