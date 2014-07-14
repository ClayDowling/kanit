=====
KANIT
=====

Kanban board management system by Clay Dowling <clay@lazarusid.com>

Purpose
=======

A good task tracking system for a project is important if the project
has any complexity at all.  If you're a one-person project, a real
kanban board with post it notes is probably sufficient for the task.
Even if you're a multi-person project, as long as you all work in the
same space, the post it notes are probably sufficient.

That all goes to heck if you're a multi-person, multi-site project,
e.g. if you and your buddies are working on a skunkworks project
from your homes.  Even if you're a single person project, sometimes
you need the whiteboard where you're tracking progress to sketch out
an idea.

That's where Kanit comes in.  You manage your project by writing a
bunch of text files, all in the same folder, one for each task.  You
keep your task backlog in a separate folder, and move them into your
current sprint by copying the files into the task folder.  When the 
sprint is done, the files are moved into another folder and archived.

Stories
=======

First, a bit of terminology: when I say "story", that's interchangable
with "task."  Right now, Kanit only has one unit of measurement: the
file.  In future versions, you'll be able to establish parent-child
relationships between these files, so you can have a full hierarchy
of features, stories and tasks.  Or whatever you want to call them.  The
system just won't care.

To create a story, just create a text file (in the folder you're using
for your project management files).  Kanit assumes that these text files
are proper ReStructured Text files, which can be processed by the python
docutils suite.  You should give the text file a name that is 
descriptive of what it contains.

In the file, you should have a proper title, using '===' style bars
above and below.

Kanit will make use of two fields if they are available: status and points.

Status is the task's current status.  You can use whatever set of stati
is appropriate to your situation.  I use "Not Started," "In Process,"
and "Done," but your workflow might need to accomodate a QA team or 
signoff by a stakeholder.  The important thing is to establish a standard
for what you and your team should be using.



