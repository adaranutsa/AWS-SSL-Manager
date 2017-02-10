import re

# Message box class
class Utilities(object):

    # Function to convert the date from "yyyy-MM-dd" to "MM-dd-yyyy"
    def convertDate(self, date):
        # Read the 10 characters only
        date = date[:10]
        date = date.split("-")
        return date[1] + "-" + date[2] + "-" + date[0]

    def matchRegex(self, string):
        temp = re.compile("[a-zA-Z0-9=,.@_-]+")
        return temp.match(string)
