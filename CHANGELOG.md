### Versions and Stages ###
* Version increments, format, and meaning: __`x.y.z`__
    * __X__ - Major release
    * __Y__ - Minor release; increment when an Issue is resolved from Issues Tracker
    * __Z__ - Minor release; cleaned up code: Comments, unnecessary code, redundant code, etc
* Stages:
    * __ALPHA__ - Closed testing, user is not afraid of bugs, wants the newest features, submits bug reports
    * __Beta__ - Opt-in users, user does not mind a bug or two, wants new features before major releases
    * __Stable__ - Public use, bug-free experience, stable release

### Changelog ###
* #### 0.4
    * Beta public release
* #### 0.3.13
    * Added error handling when creating boto3 session to handle invalid credentials. It seems that it is being handled by the getSSLList function. Resolved issue #20
    * Added "Update on Option Menu update"; Profiles will now be loaded when you select the profile from OptionMenu, thus, not requiring to click "Refresh"
        * BUG: You have to move the mouse on the window for it to refresh
* #### 0.3.12
    * Fixed logic to detect Cloud Front checkbox
    * Fixed CloudFront path (added / forward slash)
    * Removed `onvalue` and `offvalue` from checkbox as these are set by default
* #### 0.3.11
    * Fixed issue 8 for Linux only - Check for and install dependencies.
    * Created a start script to be able to run `awssslmanager` to start the program after building and installing it.
    * Moved the changelog to its own CHANGELOG.md file
    * Added quick start building, installation, and running instructions to README.md

* #### 0.3.10
    * Fixed issue 10 - Changed to option menu instead of user input for AWS Profiles
    * Moved the code files to an awssslmanager package directory and renamed the package directory to tools.
    * Created a setup.py file to build the package and install dependencies
    * Switched try/except to if statement that checks python version when import tkinter
    * Fixed the attribute error on SSL Upload
    * Cleaned up and commented out unneeded code

* #### 0.3.9
    * Fixed issue 12 - Refresh the list automatically after a profile is created/set
    * Fixed issue 16 - Set the profile endpoint for IAM
    * Fixed issue 17 - Changed MsgBox class to Utilities class
    * Added the package directory along with the Utilities class file
    * Moved the message boxes to their own Message class inside package/message
    * Fixed private key validation to actually validate the certificate
    * Moved the regex function inside the utilities class

* #### 0.3.5
    * New Feature: User can now configure a profile from within the program
    * A new window is created/drawn when user selects `Create a profile` option
    * Credentials are stored in `~/.aws/config`

* #### 0.3.4
    * Moved away from class inheritance to class composition
    * Recreated the Tkinter window creation to use Frames
    * Tkinter window creation method was changed to allow for easier addition of windows in the future
    * The info, warning, and error message boxes were moved to their own MsgBox class to allow for reusage in other classes without instantiating the main class.

* #### 0.3.3
    * Corrected spelling
    * Program now loads profiles from the `~/.aws/credentials` file and displays it as Options Menu
    * Created configure window for configuring a user (not functional yet)
    
* #### 0.3.2
    * Fixed the Regex to allow hyphens in the certificate name
    * Added private key validation for different private key first and last lines

* #### 0.3.1
    * Create a second window for uploading SSL
    * Added upload SSL feature with enhanced error checking
    * Added delete SSL feature
    
* #### 0.2.x
    * Populate list with SSLs from IAM
    * Show info about SSL
        * SSL Name
        * Expiration Date
        * Upload Date
        
* #### 0.1.x
    * Initial run of the program
    * Configured GUI and fields
    * Experimented setting boto3 profiles
