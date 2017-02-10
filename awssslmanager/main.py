##########################################################################################################
## AWS SSL Manager
## Authors:
## Aleks Daranutsa
## Petru Vicol
##
##
## Version: 0.3.5 ALPHA
##
## Versions definitions:
## x.y.z STAGE
## x - Major Release ready for STAGE testers
## y - Incremeant when an issue has been resolved from Issues Tracker
## z - minor updates: cleaned up code, removed unnecessary comments/code
##
## STAGES:
## Alpha - Users that want the freshest and newest features, isn't afraid of bugs, and reports them fast
## Beta - Users that want new features and don't mind a bug or two
## Stable - Tested more avvanced people and ready for public use
###########################################################################################################

# Import modules
import boto3, botocore, os, sys  # Boto3 is based on botocore, error handling is done with botocore

# Import the right tkinter version for the proper Python version in use.
if sys.version_info.major == 2: # Python 2.x
    from Tkinter import *  # import TK
    import tkMessageBox as messagebox
elif sys.version_info.major == 3: # Python 3.x 
    from tkinter import *  # import TK
    from tkinter import messagebox  # messagebox has to be explicitly imported
else:
    print("Failed to import tkinter. Please verify your Python installation")
    exit()

from uploadGuiClass import *  # import the main window class that draws the main GUI screen
from configureProfile import *
from tools import *

class MainTk(object):
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        
        # Initialize the message box class
        self.utilities = Utilities()
        self.message = Message()    
    
        # Get the profiles list form credentials file
        self.gatherProfiles()

        self.master.title("AWS SSL Manager")

        # List holder for SSLs, allow single select mode
        self.certsList = Listbox(self.master, selectmode="single", width=50)

        # Button that triggeres the function to change the AWS profile
        self.appIdButton = Button(self.master, text="Refresh", command=self.refreshBtn)

        # Button to show message box with selected SSL
        self.showInfoButton = Button(self.master, text="Show SSL Info", command=self.showSSLInfo)
        self.deleteSSLButton = Button(self.master, text="Delete SSL", command=self.deleteSSL)
        self.uploadSSLButton = Button(self.master, text="Upload SSL", command=self.uploadSSLWindow)
        self.manageProfile = Button(self.master, text="Manage Profile", command=self.manageProfilesWindow)
        # Option/list profiles
        self.profile = StringVar()
        self.profile.set('Select a profile')

        self.optionsMenu = OptionMenu(self.master, self.profile, *self.profiles)

        # Added listener to call/run the self.refreshBtn function on OptionMenu change (when profile is selected)
        # New feature to auto-refresh rather than manually clicking the Refresh button
        self.profile.trace("w", self.refreshBtn)
        
        # Pack all elements
        self.optionsMenu.pack()
        self.appIdButton.pack()
        self.certsList.pack()
        self.showInfoButton.pack()
        self.deleteSSLButton.pack()
        self.uploadSSLButton.pack()

        self.iamClient = ''
        
    # Functions
    # Get a list of all profiles found in credentials file
    def gatherProfiles(self):
        credentialsArray = []
        while True:
            try:
                with open(os.path.expanduser("~/.aws/config"), "r") as openFile:
                    credentialsArray = [line.rstrip() for line in openFile]
                break
            except IOError:
                break
        lineNum = 0
        self.profiles = ["Configure a profile"] # option to add new profile
        if credentialsArray.__len__() >= 0:
            for line in credentialsArray:
                if (line.startswith("[")) and ("]" in line):
                    profile = line.replace("]", "")
                    profile = profile.replace("[", "")
                    profile = profile.replace("profile ", "")
                    profile = profile.rstrip("\n")
                    self.profiles.append(profile)
                lineNum += 1

    def updateOptionsMenu(self):
        self.profile.set('Select a profile')
        # Delete all options from menu
        self.optionsMenu["menu"].delete(0, "end")
        for profile in self.profiles:
            self.optionsMenu["menu"].add_command(label=profile,
                             command=lambda value=profile:
                             self.profile.set(value))
    def uploadSSLWindow(self):
        if self.iamClient == '':
            self.message.error("No Profile Set","Cannot upload a cert without a profile. Please select a profile first")
            return False
        self.newWindow = Toplevel(self.master)
        self.app = uploadGuiClass(self.newWindow, self.iamClient)
        self.newWindow.wait_window()
        #Refresh the SSL list
        self.getSSLList()

    def manageProfilesWindow(self):
        self.newWindow = Toplevel(self.master)
        self.app = manageProfiles(self.newWindow)

    def configureProfileWindow(self):
        self.newWindow = Toplevel(self.master)
        self.app = masterClass(self.newWindow)
        self.newWindow.wait_window()

    # Accept *args which is a way of telling to accept any variables/arguments passed to function
    # trace method send 4 arguments to function; this is a workaround/exception catch
    def refreshBtn(self, *args):
        # Added if statement to ignore default option
        if self.profile.get() == "Select a profile":
            return
        # sets the boto profile
        self.setBotoProfile()

        # Refresh the SSL list
        self.getSSLList()

    # Function to delete SSL
    def deleteSSL(self):
        resposnse = messagebox.askyesno(title="Do you want to continue?",
                                        message="Are you sure that you want to delete " + self.certsList.get(ACTIVE))
        if resposnse == True:
            try:
                self.iamClient.delete_server_certificate(ServerCertificateName=self.certsList.get(ACTIVE))
                self.message.info("Deleting SSL", "SSL deleted")
                self.getSSLList()
            except:
                self.message.error("Something happened", "There was an error\n" + str(sys.exc_info()[0]))

    # Function to set the AWS profile from input box
    def setBotoProfile(self):
        if self.profile.get() == "Select a profile":
            self.message.error("No profile selected", "A profile was not selected, please select a profile and try again!")
            return
        elif self.profile.get() == "Configure a profile":
            self.configureProfileWindow()
            self.gatherProfiles()
            self.updateOptionsMenu()
            return
        while True:
            try:
                self.iamClient = boto3.Session(profile_name=str(self.profile.get())).client('iam',
                                                                                            region_name='us-east-1',
                                                                                            endpoint_url="https://iam.amazonaws.com")
                # Generate new list after the AWS profile has been changed
                # "while True" is an infinite loop, "break" solves this problem. It will allow to run just once
                break
            # Catch error if profle was not found
            except botocore.exceptions.ProfileNotFound as e:
                # Raise error message
                self.message.error("Error: Profile not found",
                              "It seems that user " + self.profile.get() + " has not been set up yet.\n" + str(e))
                break
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'AccessDenied':
                    self.message.error("Access Denied", e)
                elif e.response['Error']['Code'] == 'InvalidClientTokenId':
                    self.message.error("Invalid Access Key Pair", e)
                break

    # Function to empty the list and re-populate it
    def getSSLList(self):
        self.certsList.delete(0, END)
        try:
            certificates = self.iamClient.list_server_certificates()
            for cert in certificates["ServerCertificateMetadataList"]:
                self.certsList.insert(END, cert["ServerCertificateName"])
        except AttributeError:
            # The profile is empty and iamClient is empty is return
            return False
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InvalidClientTokenId':
                self.message.error("Invalid profile", "The security token included in the request is invalid.\nAccess Key and Secret Access Key deactivated or removed.")
            return  False

    # Simple function that alerts and displays the selected SSL from the list
    def showSSLInfo(self):
        # Error handling for response. If the profile isn't set, then iamClient will be empty and throw an AttributeError
        try:
            response = self.iamClient.get_server_certificate(ServerCertificateName=self.certsList.get(ACTIVE))[
                "ServerCertificate"]["ServerCertificateMetadata"]
            self.message.info("List certs", "Certificate Name: " + response[
                "ServerCertificateName"] + "\n" + "Expiration Date: " + self.utilities.convertDate(
                str(response["Expiration"])) + "\n" + "Upload Date: " + self.utilities.convertDate(str(response["UploadDate"])))
        except AttributeError:
            self.message.info("Info: No Profile Set", "Unable to display the SSL Cert as the profile hasn't been set")

# Displays and runs the main window
def main(): 
    root = Tk()
    app = MainTk(root)
    root.mainloop()

if __name__ == '__main__':
    main()
