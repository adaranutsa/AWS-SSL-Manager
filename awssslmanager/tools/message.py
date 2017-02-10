# Import modules
import sys

# Import the right tkinter version for the proper Python version in use.
if sys.version_info.major == 2: # Python 2.x
    import tkMessageBox as messagebox
elif sys.version_info.major == 3: # Python 3.x 
    from tkinter import messagebox  # messagebox has to be explicitly imported
else:
    print("Failed to import tkinter messagebox. Please verify your Python installation")
    exit()

class Message(object):
    # Display an error box pop up
    def error(self, title, message):
        messagebox.showerror(title, message)

    # Display an info box pop up
    def info(self, title, message):
        messagebox.showinfo(title, message)

    # Display a warning box pop up
    def warning(self, title, message):
        messagebox.showwarning(title, message)
