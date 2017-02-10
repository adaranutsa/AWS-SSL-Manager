from setuptools import setup
import sys, os, platform

os_type = platform.linux_distribution()[0]

def install_tk_debian():
    print("System Type: Debian")
    print("Installing python-tk (Tkinter)")
    os.system('sudo apt-get install -y python-tk')

def install_tk_redhat():
    print("System Type: Redhat")
    print("Installed tkinter")
    os.system('sudo yum install -y tkinter')


if sys.version_info.major == 2:
    try:
        import Tkinter
    except ImportError:
        # If debian based
        if os_type == 'LinuxMint' or os_type == 'Debian':
            install_tk_debian()
        # If redhat based
        elif os_type == 'Fedora':
            install_tk_redhat()
        # Unknown Platform Type
        else:
            print("\n\n Python Version: 2\n\nUnknown Platform. Please install Tkinter before running awssslmanager\n\n")

elif sys.version_info.major == 3:
    try:
        import tkinter
    except ImportError:
        # If debian based
        if os_type == 'LinuxMint' or os_type == 'Debian':
            install_tk_debian()
        # If redhat based
        elif os_type == 'Fedora':
            install_tk_redhat()
        # Unknown Platform Type
        else:
            print("\n\n Python Version: 3\n\nUnknown Platform. Please install Tkinter before running awssslmanager\n\n")

else:
    print("Something happened with checking the system version. Please verify your Python installation and try again")
    exit()

setup(name="awssslmanager",
      version='0.3.11',
      description="AWS SSL Certificate Manager",
      long_description=open('README.md').read(),
      author="Aleks Daranutsa & Petru Vicol",
      packages=['awssslmanager'],
      package_dir={'awssslmanager': 'awssslmanager'},
      package_data={'awssslmanager': ['*.py','tools/*.py']},
      scripts=['awssslmanager/scripts/awssslmanager'],
      classifiers=[
        'Intended Audience :: AWS Engineers',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Environment :: GUI',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: User Interfaces'],
      install_requires=[
          "botocore",
          "boto3"
      ]
)
