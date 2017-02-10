import botocore, re, sys # Boto3 is based on botocore, error handling is done with botocore, re = regular expressions

# Import the right tkinter version for the proper Python version in use.
if sys.version_info.major == 2: # Python 2.x
    from Tkinter import *  # import TK
elif sys.version_info.major == 3: # Python 3.x 
    from tkinter import *  # import TK
else:
    print("Failed to import tkinter. Please verify your Python installation")
    exit()

from tools import *

# Draw the upload GUI screen
class uploadGuiClass(object):
    def __init__(self, master, iamClient):
        self.master = master
        self.iamClient = iamClient
        self.master.title("Upload SSL Cert")
        
        self.utilities = Utilities()
        self.message = Message()
        
        # Label for cert paste boxes
        self.certNameLbl = Label(self.master, text="Certificate Name:")
        self.certPrivateLbl = Label(self.master, text="Paste the Private Key")
        self.certPublicLbl = Label(self.master, text="Paste the Public Key")
        self.certBundleLbl = Label(self.master, text="Paste the Bundle/Chain Key")

        # Cert input boxes
        self.certNameTxt = Entry(self.master, width=24)
        self.certPrivateTxt = Text(self.master, height=12)
        self.certPublicTxt = Text(self.master, height=12)
        self.certBundleTxt = Text(self.master, height=12)

        # Upload cert buttons
        self.uploadCertInput = Button(self.master, text="Upload Cert", command=self.uploadCert)
        
        # Cloudfront variable
        self.cloudfront = IntVar()

        # Upload to CloudFront option
        self.certCloudfrontCbx = Checkbutton(self.master, text="Check if uploading to CloudFront", variable=self.cloudfront)
        
        # Pack all elements
        self.certNameLbl.pack()
        self.certNameTxt.pack()
        self.certCloudfrontCbx.pack()
        self.certPrivateLbl.pack()
        self.certPrivateTxt.pack()
        self.certPublicLbl.pack()
        self.certPublicTxt.pack()
        self.certBundleLbl.pack()
        self.certBundleTxt.pack()        
        self.uploadCertInput.pack()

        # Cert validation error list
        self.certValError = []

        # REGEX to match name according to AWS specifications:
        # The regex pattern for this parameter is a string of characters consisting of
        # upper and lowercase alphanumeric characters with no spaces.
        # You can also include any of the following characters: =,.@-

    def certNameKeyupCallback(self, keyup):
        print(str(keyup))
        for c in str(keyup):
            print("evaluating " + c)
            # If the character does not match the regular expression,
            # returns None
            match = self.utilities.matchRegex(c)
            print(match)
            if match is None:
                #self.certNameKeyupLbl.config(fg='red')
                print("Invalid character: " + c)
                self.certNameKeyupLbl = "Invalid character found: " + c
                    #("Invalid character: " + c)
            else:
                print("Name is valid")
                #self.certNameKeyupLbl.config(fg='green')
                self.certNameKeyupLbl = "Name is valid"

    def validateCerts(self):
        
        # Clear the cerValError variable
        self.certValError = []

        # Get cert name
        name = self.certNameTxt.get().strip()

        # If no cert name specified, return false
        if not name:
            self.message.error('Cert Name Required', 'Please enter a certificate name!')
            return False
        #
        else:
            # Check each letter in name to see if it contains any illegal characters
            for c in name:
                # If the character does not match the regular expression,
                # returns None
                match = self.utilities.matchRegex(c)
                if match is None:
                    self.message.error('Invalid character in cert name: ' + c + ' at index ' + str(name.index(c)),'The certificate name may contain any characters consisting of upper and lowercase alphanumeric characters only with no spaces.\nYou can also include any of the following characters: \n=\tEqual sign\n,\tComma\n.\tDot\n@\tAt sign\n-\tHyphen\n_\tUnderscore')
                    return False

        #elif str()

        # Get the cert contents
        private = self.certPrivateTxt.get("1.0",END).strip()
        public = self.certPublicTxt.get("1.0",END).strip()
        bundle = self.certBundleTxt.get("1.0",END).strip()
        
        # Cert validation string
        valPrivateL1 = '-----BEGIN PRIVATE KEY-----'
        valPrivateL2 = '-----END PRIVATE KEY-----'
        valPrivateL1a = '-----BEGIN RSA PRIVATE KEY-----'
        valPrivateL2a = '-----END RSA PRIVATE KEY-----' 

        valPublicL1 = '-----BEGIN CERTIFICATE-----'
        valPublicL2 = '-----END CERTIFICATE-----'

        # Get the first and last line of the private key
        if private:
            privateL1 = private.splitlines()[0]
            privateL2 = private.splitlines()
            privateL2 = privateL2[len(privateL2) - 1]
            
            # If the first and last line of the private cert don't match the validation string
            # insert a 'private' in the certValError list.
            
            if privateL1 == valPrivateL1 and privateL2 == valPrivateL2:
                a = 0 # Do nothing
            elif privateL1 == valPrivateL1a and privateL2 == valPrivateL2a:
                a = 0 # Do nothing
            else:
                self.certValError.append('private')

        # Get the first and last line of the public key
        if public:
            publicL1 = public.splitlines()[0]
            publicL2 = public.splitlines()
            publicL2 = publicL2[len(publicL2) - 1]

        # If the first and last line of the public cert don't match the validation string
        # insert a 'public' in the certValError list.
            if not publicL1 == valPublicL1 or not publicL2 == valPublicL2:
                self.certValError.append('public')
        
        # Get the first and last line of the bundle
        if bundle:
            bundleL1 = bundle.splitlines()[0]
            bundleL2 = bundle.splitlines()
            bundleL2 = bundleL2[len(bundleL2) - 1]
            
        # If the first and last line of the bundle cert don't match the validation string
        # insert a 'bundle' in the certValError list.
            if not bundleL1 == valPublicL1 or not bundleL2 == valPublicL2:
                self.certValError.append('bundle')

        # Put together the error message for invalid certs
        error_msg = "The following certs are invalid! Please try again!\n"

        # Check if there are any cert errors
        if 'private' in self.certValError:
            error_msg += '\nPrivate Certificate'

        if 'public' in self.certValError:
            error_msg += '\nPublic Certificate'

        if 'bundle' in self.certValError:
            error_msg += '\nChain Certificate'
        
        # If there are any certs errors, generate a pop up with the error message and return false
        if self.certValError:
            self.message.error('Invalid Certs', error_msg)
            return False
        else:
            # If the private or public (or both) certs are blank, generate a pop up and return false
            if not private or not public:
                self.message.error('Invalid Certs', 'Please include both private and public certs in order to continue')
                return False

    # Code to upload certificate
    def uploadCert(self): # Upload certificate
        # Validate of all certs are valid. If they aren't, stop processing!
        # If certs are valid, continue
        # The check does not let the code run as it returns None if everything is valid
        
        if self.validateCerts() == False:
            print("\n\nValidation Failed!\n\n")
            return False

        # Getting input form GUI form
        SSLName = self.certNameTxt.get()
        SSLPrivateKey = self.certPrivateTxt.get("1.0",END).strip()
        SSLPublicKey = self.certPublicTxt.get("1.0",END).strip()
        SSLCABundle = self.certBundleTxt.get("1.0",END).strip()

        # Check if cloudfront was checked or not; if checked, SSL will be uploaded to Cloud Front
        if self.cloudfront.get() == 1:
            CFPath = "/cloudfront/" + SSLName + '/'
        else:
            CFPath = "/"

        # Try to catch any errors when uploading SSL
        try:
            if SSLCABundle:
                self.iamClient.upload_server_certificate(
                    Path = CFPath,
                    ServerCertificateName = SSLName,
                    CertificateBody = SSLPublicKey,
                    PrivateKey = SSLPrivateKey,
                    CertificateChain = SSLCABundle
                )
            else:
                self.iamClient.upload_server_certificate(
                    Path=CFPath,
                    ServerCertificateName=SSLName,
                    CertificateBody=SSLPublicKey,
                    PrivateKey=SSLPrivateKey
                )

            # Display successful message
            self.message.info("Success", "SSL Certificate Successfully Uploaded!")

            # Close window after SSL has been uploaded
            self.master.destroy()

        except botocore.exceptions.ClientError as e:
            print(e)
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                self.message.error("Certificate already exists", str(e) + "\n\nPlease enter a different name.")
            elif e.response['Error']['Code'] == "KeyPairMismatch":
                self.message.error("Keys mismatch", e)
            elif e.response['Error']['Code'] == "MalformedCertificate":
                if "Unable to parse certificate" in str(e.response['Error']['Message']):
                    self.message.error("Invalid public certificate", "The public certificate is invalid\n\n" + str(e))
                elif "Unable to parse private key" in str(e.response['Error']['Message']):
                    self.message.error("Invalid private certificate", "The private certificate is invalid\n\n" + str(e))
                else:
                    self.message.error("Check the certificate", e)
            else:
                self.message.error("Other alert", e)
        except:
            self.message.error("Failed to upload SSL", "Failed to upload SSL due to: " + str(sys.exc_info()[1]))
