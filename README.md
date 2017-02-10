# README #

### AWS SSL Manager

* GUI SSL Manager for AWS
* Features:
    * List all SSLs stored in IAM
    * Upload new SSLs
    * Delete SSL
    * Show SSL Info
        * Certificate Name
        * Expiration Date
        * Upload Date

* Version: 0.4 BETA

## How do I get set up?

#### Known Supported platforms
* ##### *UNIX
    * Clone or down this repository to your local machine
    * Build and install the package. This will resolve any dependencies that are needed.
        * `sudo python setup.py install` - Build and install the package
    * Run the program from commandline using the following command from anywhere on your machine
        * `awssslmanager` - This will launch AWS SSL Manager
* ##### Windows
    * Download the `.exe` file
    * Run `.exe` file


#### Summary
> The purpose of this program is to allow and help users List, Upload, Delete, and Update SSLs stored in IAM in an AWS account. This eliminates the need to write long AWS CLI commands and provide an easy and hassle free, point-and-click experience to manage SSLs.
>
> Since IAM is global, specifying the region is not required.
> > ###### __NOTE:__
> > Specifying a default region is strongly recommended.
> > We recommend setting the region the environment is hosted as the default region.
>
> This program features/provides local error checking to reduce the number of API calls.
> Uploading SSLs offers the option to upload SSL to CloudFront as well.

#### Configurations
* AWS profile configuration
    * 3 ways of configuring AWS profiles:
        * AWS CLI
            * `pip install awscli` - Install AWS CLI
            * `aws configure --profile <proilename>` - Configure a profile
        * Configure a profile using the in-app profile configurator
            * Select `Create a profile` from the option menu
            * Configure profile
            * Click `Configure profile`
        * Configure manually by editing `~/.aws/config` file
            * See for [Boto3 docs](http://boto3.readthedocs.io/en/latest/guide/configuration.html#aws-config-file) for details
#### Dependencies
* The following libraries must be installed (otherwise will be installed by the `setup.py` script):
    * `boto3` - AWS SDK for Python
    * `re` - Regular Expressions
    * `tkinter` - Tkinter UI