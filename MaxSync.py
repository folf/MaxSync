#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

SourceDirPath = "/data/data1" 
BackupDirPath = "/media" 


# Don't need to change anything below this line 

import Tkinter, tkFileDialog, tkMessageBox
import subprocess
import os

class simpleapp_tk(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        
        # We only need the Source and Destination directory
        self.varSource = Tkinter.StringVar()
        self.varSource.set("SourceDir")
        self.varDestination = Tkinter.StringVar()
        self.varDestination.set("DestinationDir")
        
        # Setup buttons on the left for doing the actions
        button = Tkinter.Button(self, text=u"1: Select Source Directory!",
                                command=self.askdirectorySource, width=25)
        button.grid(column=0, row=0, sticky='EW')

        button = Tkinter.Button(self, text=u"2: Select Destination Directory!",
                                command=self.askdirectoryDestination, width=25)
        button.grid(column=0, row=1, sticky='EW')

        button = Tkinter.Button(self, text=u"3: Backup your data!",
                                command=self.backupdata, width=25)
        button.grid(column=0, row=2, sticky='EW')

        
        #  Labels with the names of the directories
        SourceDir = Tkinter.Label(self,textvariable=self.varSource,
                                  anchor="w")
        SourceDir.grid(column=1,row=0,sticky='EW')

        DestinationDir = Tkinter.Label(self,textvariable=self.varDestination,
                                       anchor="w")
        DestinationDir.grid(column=1,row=1,sticky='EW')

        # trying to also make a text box with output
        self.var_textbox = Tkinter.Text(self, height=10)
        self.var_textbox.grid(column=0, row=3, columnspan=2)

    def askdirectorySource(self):
        """Returns a selected directory name."""
        if self.varSource.get() == "SourceDir" :
            self.varSource.set(SourceDirPath)
        self.chosen_dir = tkFileDialog.askdirectory(initialdir=self.varSource.get())
        self.varSource.set(self.chosen_dir)
        self.var_textbox.insert(Tkinter.END, "\n"+self.chosen_dir+" selected as source directory\n")
        
        

    def askdirectoryDestination(self):
        """Returns a selected directory name."""
        if self.varDestination.get() == "DestinationDir" :
            self.varDestination.set(BackupDirPath)
        self.chosen_dir = tkFileDialog.askdirectory(initialdir=self.varDestination.get())
        self.varDestination.set(self.chosen_dir+"/")
        self.var_textbox.insert(Tkinter.END, "\n"+self.chosen_dir+" selected as backup directory\n")

        
    def backupdata(self):
        print "You requested the backup routine"
        self.option_add('*font', 'Helvetica -14')
        self.option_add("*Dialog.msg.wrapLength", "10i")

        # Check to see if the directories were set for something else
        if self.varSource.get() == "SourceDir" :
            tkMessageBox.showwarning("Warning!",  "First set the source directory!")
        elif self.varDestination.get() == "DestinationDir" :
            tkMessageBox.showwarning("Warning!",  "Also remember to set the  destination directory!")
        # OK good to go
        else:
            result = tkMessageBox.askyesno("Ready to backup!!",
                                           "You will now synchronize your folder\n\n%s\n\ninto your backup folder:\n\n%s"
                                           %(os.path.basename(self.varSource.get()),self.varDestination.get()))
            if result :
                print "You have accepted to backup"
                self.DiskUsage = Tkinter.StringVar()
                DiskUsage = os.popen('du -hs "%s"'%(self.varSource.get())).read()
                tkMessageBox.showinfo("First notification",
                                      "Your job size is :\n"
                                      +DiskUsage+
                                      "\n this could take a while, please be patient.")
                var_rsync_command = subprocess.Popen(["rsync", "-ahv", self.varSource.get(), self.varDestination.get()], stdout=subprocess.PIPE)
                # Trying to make the textbox update all the time
                for line in iter(var_rsync_command.stdout.readline,''):
                    self.var_textbox.insert(Tkinter.END, line)
                    self.var_textbox.update()
                    self.var_textbox.yview(Tkinter.END)
                #
                tkMessageBox.showinfo("Backup complete","The rsync job has finished")

            else:
                print "You declined to backup your data"


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('MaxSync - Backup your data')
    app.mainloop()
