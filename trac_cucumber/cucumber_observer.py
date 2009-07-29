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
    story_directory = PathOption("cucumber", "story_directory")
    output_directory = PathOption("cucumber", "output_directory")

    def story_added(self, story_name, story):
        if self.story_added_callback:
            self.execute(self.story_added_callback,story_name,story)

    def story_edited(self, story_name, story):
        if self.story_edited_callback:
            self.execute(self.story_edited_callback,story_name,story)

    def execute(self,command,story_name,story):
        story_file_name = self.database.story_file_name(story_name)
        self.log.debug("Executing %s %s" % (command, story_file_name))
        proc = subprocess.Popen((command, story_file_name), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.story_directory)
        with open(self.database.output_file_name(story_name),"w") as out_file:
          out_file.write(proc.communicate()[0])
        #with open(os.path.join(self.output_directory,'error.txt'),"a") as err_file:
        #  err_file.write(proc.communicate()[1]+'\n')
            
