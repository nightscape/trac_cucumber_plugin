from interfaces import *
from trac.config import Option, PathOption
import os
import subprocess

class CommandCucumberObserver(Component):
    implements(ICucumberObserver)

    story_added_callback = Option("cucumber", "story_added_callback")
    story_edited_callback = Option("cucumber", "story_edited_callback")
    story_directory = PathOption("cucumber", "story_directory")
    output_directory = PathOption("cucumber", "output_directory")

    def story_added(self, story_name, story):
        if self.story_added_callback:
            self.log.debug("Executing %s %s" % (self.story_added_callback, story_name))
            self.execute(self.story_added_callback,story_name,story)

    def story_edited(self, story_name, story):
        if self.story_edited_callback:
            self.log.debug("Executing %s %s" % (self.story_edited_callback, story_name))
            self.execute(self.story_edited_callback,story_name,story)

    def execute(self,command,story_name,story):
        subprocess.Popen((command, story_name+'.feature'), executable=command,  stdout=open(os.path.join(self.output_directory,'output.txt'),"w"), stderr=open(os.path.join(self.output_directory,'error.txt'),"w"), shell=False, cwd=self.story_directory, env=None)
