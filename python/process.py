from tkinter import filedialog
from tkinter import *

import os

from merge import merge_light_field

# parameters for light field capture
camera_name = 'SonyA7r1'
exposures = 3

root = Tk()
root.title("Merge HDR")
root.directory = filedialog.askdirectory()

merge_light_field(root.directory, camera_name, exposures)