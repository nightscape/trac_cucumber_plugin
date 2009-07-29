from interfaces import *
from trac.config import Option, PathOption, ExtensionOption
import os
import subprocess

class CommandCucumberObserver(Component):
    implements(ICucumberObserver)
    database = ExtensionOption('cucumber', 'database', ICucumberDatabase,
        'CucumberDatabase', """Name of the component implementing the cucumber story database""")

    story_added_callback = Option("cucumber", "story_added_callback")
    story_edited_callback = Option("cucumber", "story_edited_callback")

    def story_added(self, story_name, story):
        if self.story_added_callback:
            self.execute(self.story_added_callback,story_name,story)

    def story_edited(self, story_name, story):
        if self.story_edited_callback:
            self.execute(self.story_edited_callback,story_name,story)

    def execute(self,command,story_name,story):
        story_file_name = self.database.story_file_name(story_name)
        self.log.debug("Executing %s %s" % (command, story_file_name))
        proc = subprocess.Popen((command, story_file_name), stdout=subprocess.PIPE)
        with open(self.database.output_file_name(story_name),"w") as out_file:
          out_file.write(proc.communicate()[0])
            
