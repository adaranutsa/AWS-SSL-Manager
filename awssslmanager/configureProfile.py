# -*- coding: utf-8 -*-
import boto3, botocore, re, os, sys  # Boto3 is based on botocore, error handling is done with botocore, re = regular expressions

# Import the right tkinter version for the proper Python version in use.
if sys.version_info.major == 2: # Python 2.x
    from Tkinter import *  # import TK
elif sys.version_info.major == 3: # Python 3.x 
    from tkinter import *  # import TK
else:
    print("Failed to import tkinter. Please verify your Python installation")
    exit()

# Draw the Configure a profile GUI screen
class masterClass(object):
    def __init__(self, master):
        self.master = master

        self.regions = [{'region': 'us-east-1', 'name': 'US East (N. Virginia)'},
                        {'region': 'us-east-2', 'name': 'US East (Ohio)'},
                        {'region': 'us-west-1', 'name': 'US West (N. California)'},
                        {'region': 'us-west-2', 'name': 'US West (Oregon)'},
                        {'region': 'ca-central-1', 'name': 'Canada (Central)'},
                        {'region': 'ap-south-1', 'name': 'Asia Pacific (Mumbai)'},
                        {'region': 'ap-northeast-2', 'name': 'Asia Pacific (Seoul)'},
                        {'region': 'ap-southeast-1', 'name': 'Asia Pacific (Singapore)'},
                        {'region': 'ap-southeast-2', 'name': 'Asia Pacific (Sydney)'},
                        {'region': 'ap-northeast-1', 'name': 'Asia Pacific (Tokyo)'},
                        {'region': 'eu-central-1', 'name': 'EU (Frankfurt)'},
                        {'region': 'eu-west-1', 'name': 'EU (Ireland)'},
                        {'region': 'eu-west-2', 'name': 'EU (London)'},
                        {'region': 'sa-east-1', 'name': 'South America (São Paulo)'}]

        self.drawConfigureGui()  # Draw the Configure a profile GUI
        self.updateOptionsMenu()
        # Pack all elements
        self.profileNameLbl.grid(column=1, row=1)
        self.AccessKeyLbl.grid(column=1, row=2)
        self.SecretAccessKeyLbl.grid(column=1,row=3)
        self.RegionLbl.grid(column=1,row=4)
        self.profileNameTxt.grid(column=2,row=1)
        self.accessKeyTxt.grid(column=2,row=2)
        self.secretKeyTxt.grid(column=2,row=3)
        self.optionsMenu.grid(column=2, row=4)

        self.confiProfile.grid(column=2,row=5)


        self.region.set("Select a region")



        # REGEX to match name according to AWS specifications:
        # The regex pattern for this parameter is a string of characters consisting of
        # upper and lowercase alphanumeric characters with no spaces.
        # You can also include any of the following characters: =,.@-
        self.nameRegex = re.compile("[a-zA-Z0-9=,.@_-]+")

    def drawConfigureGui(self):  # Draw the upload GUI window
        self.master.title("Configure a profile")

        # Label for cert paste boxes
        self.profileNameLbl = Label(self.master,  text="Profile Name:")
        self.AccessKeyLbl = Label(self.master,  text="Access Key:")
        self.SecretAccessKeyLbl = Label(self.master,  text="Secret Access Key")
        self.RegionLbl = Label(self.master,  text="Default region (optional but highly recommended)")


        # Input/entry boxes
        self.profileNameTxt = Entry(self.master, width=24)
        self.accessKeyTxt = Entry(self.master, width=24)
        self.secretKeyTxt = Entry(self.master, width=24)

        # Buttons
        self.confiProfile = Button(self.master, text="Configure profile", command=self.writeToFile)

        # Others
        self.region = StringVar()
        self.optionsMenu = OptionMenu(self.master, self.region, *self.regions)

    def writeToFile(self):
        if not os.path.exists(os.path.expanduser("~/.aws/")):
            os.makedirs(os.path.expanduser("~/.aws/"))
        while True:
            # look up region in array based on name
            for region in self.regions:
                if region['name'] == self.region.get():
                    self.region.set(region['region'])
            try:
                with open(os.path.expanduser("~/.aws/config"), "a+") as openFile:
                    openFile.write("[profile " + self.profileNameTxt.get() + "]\n")
                    openFile.write("aws_access_key_id = " + self.accessKeyTxt.get() + "\n")
                    openFile.write("aws_secret_access_key = " + self.secretKeyTxt.get() + "\n")
                    openFile.write("region = " + self.region.get() + "\n")
                break
            except IOError:
                break
        self.master.destroy()

    # Work around as OptionMenu does not support listing dictionary arrays
    def updateOptionsMenu(self):
        self.region.set('Select a region')
        # Delete all options from menu
        self.optionsMenu["menu"].delete(0, "end")
        for region in self.regions:
            self.optionsMenu["menu"].add_command(label=region['name'],
                             command=lambda value=region['name']:
                             self.region.set(value))
